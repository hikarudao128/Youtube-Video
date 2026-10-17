"""Bản dựng 2 (tiếng Anh): đọc liền từng chương, chuyển cảnh mượt, phụ đề khớp từng từ.

Khác bản 1 (lam_video.py):
- Giọng đọc tạo cho CẢ CHƯƠNG một lần (trôi chảy, không ngắt từng cảnh), tốc độ +10%.
- Mốc chuyển cảnh lấy từ thời điểm từng từ (WordBoundary) mà edge-tts trả về.
- Chuyển cảnh hòa tan 1 giây đặt giữa hai câu; chuyển động máy đều (không dừng ở chỗ cắt);
  dựng chuyển động ở 4K rồi thu về 1080p để lia/zoom không bị giật.
- Phụ đề theo từng cụm từ, đúng thời điểm đọc.

Chạy:  python3 lam_video_v2.py [-j 6]
Kết quả: out/ChiPheo_EN_v2.mp4, out/ChiPheo_EN_v2.srt
"""
import argparse
import asyncio
import difflib
import os
import re
import ssl
from concurrent.futures import ThreadPoolExecutor

import lam_video as L

HERE = L.HERE
WORK = os.path.join(HERE, "work_v2")
OUT = L.OUT
NAME = "ChiPheo_EN_v2"
VOICE = "en-US-AndrewMultilingualNeural"
RATE = "+10%"
XF = 1.0            # hòa tan giữa các cảnh (giây)
LEAD = 0.6          # lặng đầu video
CH_GAP = 0.9        # lặng giữa hai chương
TAIL = 2.0          # giữ khung cuối
CUT_EARLY = 0.12    # cắt cảnh sớm hơn từ đầu tiên một chút
FPS = 30


def norm(w):
    return re.sub(r"[^0-9a-zà-ỹđ]", "", w.lower())


async def _tts_chapter(text, mp3):
    import edge_tts
    import edge_tts.communicate as comm
    if os.path.exists(L.CA_BUNDLE):
        comm._SSL_CTX = ssl.create_default_context(cafile=L.CA_BUNDLE)
    c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(mp3, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    return words


def chapter_audio(cid, scenes):
    """scenes: [(sid, text)]. Trả về (wav, độ dài, tokens) với tokens = [(sid, chữ hiển thị, bắt đầu, kết thúc)]."""
    disp, speak = [], []
    for sid, text in scenes:
        t = text.replace(" / ", " ")
        d_words, s_words = t.split(), L.to_speech(t).split()
        if len(d_words) != len(s_words):      # phiên âm làm lệch số từ thì đọc nguyên văn
            s_words = d_words
        disp += [(sid, w) for w in d_words]
        speak += s_words
    mp3 = os.path.join(WORK, f"ch{cid}.mp3")
    wav = os.path.join(WORK, f"ch{cid}.wav")
    for attempt in range(3):
        try:
            words = asyncio.run(_tts_chapter(" ".join(speak), mp3))
            break
        except Exception:
            if attempt == 2:
                raise
    L.sh(["ffmpeg", "-y", "-i", mp3, "-ar", "48000", "-ac", "1", wav])
    dur = L.duration(wav)

    # gióng từng từ của văn bản với từng WordBoundary
    a = [norm(w) for w in speak]
    b = [norm(w[2]) for w in words]
    times = [None] * len(a)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = words[blk.b + k][:2]
    # từ không gióng được: nội suy giữa hai từ đã biết
    last = (0.0, 0.0)
    for i in range(len(times)):
        if times[i] is None:
            nxt = next((times[j] for j in range(i + 1, len(times)) if times[j]), (dur, dur))
            times[i] = (last[1], max(last[1], min(nxt[0], last[1] + 0.3)))
        last = times[i]
    tokens = [(sid, w, s, e) for (sid, w), (s, e) in zip(disp, times)]
    return wav, dur, tokens


def motion(cam, n):
    """Chuyển động đều (tuyến tính) để không bị khựng ở chỗ chuyển cảnh."""
    p = f"(on/{max(n - 1, 1)})"
    cx, cy = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    shake = "+10*sin(on*1.3)" if "rung" in cam else ""
    if "tilt" in cam:
        y = f"(ih-ih/zoom)*{p}" if "xuống" in cam else f"(ih-ih/zoom)*(1-{p})"
        return "1.16", cx + shake, y
    if "pan" in cam and "push" not in cam:
        x = f"(iw-iw/zoom)*(1-{p})" if "phải sang trái" in cam else f"(iw-iw/zoom)*{p}"
        return "1.14", x + shake, cy
    if "pull" in cam:
        return f"1.18-0.14*{p}", cx + shake, cy
    return f"1.03+0.12*{p}", cx + shake, cy


def render_clip(sid, cam, length):
    out = os.path.join(WORK, "clips", sid.replace(".", "_") + ".mp4")
    img = os.path.join(L.SCENES, f"canh_{sid.replace('.', '_')}.png")
    n = int(round(length * FPS))
    z, x, y = motion(cam, n)
    vf = (f"scale=5120:2880:flags=lanczos,"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=3840x2160:fps={FPS},"
          f"scale=1920:1080:flags=lanczos")
    if sid == "0.9":
        vf += (f",drawtext=fontfile={L.FONT}:text='CHÍ PHÈO':fontsize=150:fontcolor=0xB3261E:"
               f"x=(w-text_w)/2:y=(h-text_h)/2-60:alpha='min(1,max(0,(t-0.8)/0.8))',"
               f"drawtext=fontfile={L.FONT}:text='Nam Cao · 1941':fontsize=48:fontcolor=0x3B332B:"
               f"x=(w-text_w)/2:y=h/2+70:alpha='min(1,max(0,(t-1.3)/0.8))'")
    vf += ",format=yuv420p"
    L.sh(["ffmpeg", "-y", "-i", img, "-vf", vf, "-frames:v", str(n), "-r", str(FPS),
          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out])
    return out


def cues_from_tokens(tokens, max_words=8, max_len=3.4):
    cues, cur = [], []
    for tok in tokens:
        cur.append(tok)
        w = tok[1]
        if (w[-1] in ".?!" or len(cur) >= max_words or (w[-1] in ",:;" and len(cur) >= 5)
                or cur[-1][3] - cur[0][2] > max_len):
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)
    out = []
    for i, c in enumerate(cues):
        s, e = c[0][2], c[-1][3] + 0.2
        if i + 1 < len(cues):
            e = min(e, cues[i + 1][0][2] - 0.02)
        out.append((" ".join(t[1] for t in c), s, max(e, s + 0.5)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(os.path.join(WORK, "clips"), exist_ok=True)
    os.makedirs(os.path.join(WORK, "chunks"), exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    L.NARRATION = os.path.join(HERE, "LOI_KE_EN.txt")
    L.PHONETIC = L.LANGS["en"]["phonetic"]
    L.XF = XF
    items = L.load_narration()
    cams = L.load_camera()

    chapters = {}
    for sid, text in items:
        chapters.setdefault(sid.split(".")[0], []).append((sid, text))
    order = sorted(chapters, key=int)
    print(f"Tạo giọng đọc cho {len(order)} chương…", flush=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        res = dict(zip(order, ex.map(lambda c: chapter_audio(c, chapters[c]), order)))

    # dòng thời gian chung
    tokens_all, scene_start, audio_parts, t = [], {}, [], LEAD
    for c in order:
        wav, dur, toks = res[c]
        for sid, w, s, e in toks:
            tokens_all.append((sid, w, t + s, t + e))
            scene_start.setdefault(sid, t + s)
        audio_parts.append((wav, t))
        t += dur + CH_GAP
    total = t - CH_GAP + TAIL
    print(f"Giọng đọc: {(t - LEAD) / 60:.1f} phút", flush=True)

    sids = [sid for sid, _ in items]
    bounds = [0.0] + [scene_start[s] - CUT_EARLY for s in sids[1:]]
    lengths = []
    for i in range(len(sids)):
        end = bounds[i + 1] if i + 1 < len(sids) else total
        lengths.append(end - bounds[i] + XF * (0.5 if i == 0 or i == len(sids) - 1 else 1.0))
    kinds = ["fade"] + ["fadeblack" if sids[i].split(".")[0] != sids[i - 1].split(".")[0] else "fade"
                        for i in range(1, len(sids))]

    print("Dựng chuyển động từng cảnh…", flush=True)
    with ThreadPoolExecutor(max_workers=a.j) as ex:
        clips = list(ex.map(lambda k: render_clip(sids[k], cams.get(sids[k], ""), lengths[k]),
                            range(len(sids))))

    print("Nối cảnh…", flush=True)
    L.WORK = WORK
    size = 12
    cf, cl, ck = [], [], []
    for c, s in enumerate(range(0, len(clips), size)):
        f = os.path.join(WORK, "chunks", f"c{c:02d}.mp4")
        cl.append(L.xfade_chain(clips[s:s + size], lengths[s:s + size], kinds[s:s + size], f))
        cf.append(f)
        ck.append(kinds[s])
    video = os.path.join(WORK, "video_noaudio.mp4")
    vlen = L.xfade_chain(cf, cl, ck, video)
    # mỗi cảnh xuất hiện lùi XF/2 so với mốc (hòa tan đặt giữa hai câu) -> lùi âm thanh tương ứng
    shift = XF / 2

    print("Âm thanh + phụ đề…", flush=True)
    inputs, flt = [], []
    for k, (wav, start) in enumerate(audio_parts):
        inputs += ["-i", wav]
        flt.append(f"[{k}:a]adelay={int((start + shift) * 1000)}[a{k}]")
    flt.append("".join(f"[a{k}]" for k in range(len(audio_parts))) +
               f"amix=inputs={len(audio_parts)}:normalize=0,apad=whole_dur={vlen:.3f}[out]")
    audio = os.path.join(WORK, "narration.wav")
    L.sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
          "-ar", "48000", "-ac", "1", audio])

    srt = os.path.join(OUT, f"{NAME}.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for i, (text, s, e) in enumerate(cues_from_tokens(tokens_all), 1):
            f.write(f"{i}\n{L.srt_time(s + shift)} --> {L.srt_time(e + shift)}\n{text}\n\n")

    final = os.path.join(OUT, f"{NAME}.mp4")
    style = ("FontName=DejaVu Sans,FontSize=19,Bold=1,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=34")
    L.sh(["ffmpeg", "-y", "-i", video, "-i", audio,
          "-vf", f"subtitles={srt}:force_style='{style}'",
          "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
          "-shortest", "-movflags", "+faststart", final])
    print(f"Xong: {final} ({vlen / 60:.1f} phút)")


if __name__ == "__main__":
    main()
