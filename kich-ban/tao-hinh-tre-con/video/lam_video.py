"""Dựng video tiếng Anh "Trẻ con không được ăn thịt chó" từ ảnh phân cảnh + giọng đọc.

- Lời dẫn lấy từ dòng "Lời dẫn:" trong ../phan-canh-prompt/chuong_*.md (cùng số cảnh với ảnh).
- Giọng đọc edge-tts: người kể đọc liền từng đoạn (nhiều cảnh một lần, mốc cảnh lấy từ
  WordBoundary); lời thoại "[NHÂN VẬT]: ..." đọc bằng giọng riêng của nhân vật đó.
- Tên tiếng Việt đọc theo phiên âm, phụ đề vẫn giữ chữ gốc.
- Chuyển động Ken Burns đều, hòa tan giữa các cảnh, mờ qua màn đen khi sang chương mới.
- Chữ trên màn hình (tên phim, con số) vẽ bằng ffmpeg, không nhờ AI vẽ chữ.

Chạy:  python3 lam_video.py [-j 4]
Kết quả: out/TreConKhongDuocAnThitCho_EN.mp4 và .srt
"""
import argparse
import asyncio
import difflib
import glob
import os
import re
import ssl
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCENES = os.path.join(ROOT, "phan-canh")
SCENE_GLOB = os.path.join(ROOT, "phan-canh-prompt", "chuong_*.md")
WORK = os.path.join(HERE, "work")
OUT = os.path.join(HERE, "out")
NAME = "TreConKhongDuocAnThitCho_EN"

FPS = 30
XF = 1.0            # hòa tan giữa các cảnh (giây)
LEAD = 0.6          # lặng đầu video
CH_GAP = 0.9        # lặng giữa hai chương
LINE_GAP = 0.25     # lặng giữa hai lượt thoại
TAIL = 2.5          # giữ khung cuối
CUT_EARLY = 0.12    # cắt cảnh sớm hơn từ đầu tiên một chút
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"

# giọng: (tên giọng, tốc độ, cao độ)
VOICES = {
    "NARRATOR": ("en-US-AndrewMultilingualNeural", "+8%", "+0Hz"),
    "FATHER": ("en-US-ChristopherNeural", "+4%", "-4Hz"),
    "MOTHER": ("en-US-MichelleNeural", "-4%", "-2Hz"),
    "MỤ VỤ": ("en-US-AriaNeural", "+0%", "-6Hz"),
    "NEIGHBOR": ("en-US-RogerNeural", "-6%", "-8Hz"),
    "CU CON": ("en-US-AnaNeural", "+0%", "+6Hz"),
    "CU NHỠ": ("en-US-AnaNeural", "+0%", "-6Hz"),
    "CU NHỚN": ("en-US-AnaNeural", "+4%", "-14Hz"),
}
PHONETIC = {
    "Nam Cao": "Nahm Cow", "hắn": "hun", "thị": "tee",
    "Cái Gái": "Kai Guy", "cái Gái": "Kai Guy",
    "cu Nhớn": "koo Nyun", "Cu Nhớn": "Koo Nyun", "cu Nhỡ": "koo Nyuh", "Cu Nhỡ": "Koo Nyuh",
    "cu Con": "koo Kon", "Cu Con": "Koo Kon", "Mụ Vụ": "Moo Voo", "mụ Vụ": "Moo Voo",
    "rượu": "ruh-oo", "đồng": "dong", "xóc đĩa": "sock dee-ah",
    "Nồi xáo": "Noy sow", "tiết canh": "tee-et kahn",
}
# chữ hiện trên một số cảnh (hiện dần sau ~0.8 giây)
OVERLAYS = {
    "1.14": "10 TREES. SOLD TWICE.",
    "2.16": "REMEMBER THE FENCE.",
    "3.5": "1 DOG = 15 DAYS OF RICE",
    "4.2": "4 MEN. 1 DOG.",
    "6.2": "×2",
}
TITLE_SCENE = "0.7"
CAMS = ["push", "pan trái sang phải", "pull", "pan phải sang trái", "push", "tilt xuống"]


def sh(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Lỗi lệnh: {' '.join(cmd[:6])}…\n{r.stderr[-1500:]}")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_speech(text):
    for k in sorted(PHONETIC, key=len, reverse=True):
        text = re.sub(rf"(?<!\w){re.escape(k)}(?!\w)", PHONETIC[k], text)
    return text


def norm(w):
    return re.sub(r"[^0-9a-zà-ỹđ]", "", w.lower())


def load_scenes():
    """[(sid, [(speaker, text), ...])] theo thứ tự cảnh."""
    out = []
    for path in glob.glob(SCENE_GLOB):
        text = open(path, encoding="utf-8").read()
        for p in re.split(r"^#### CẢNH ", text, flags=re.M)[1:]:
            sid = re.match(r"(\d+\.\d+)", p).group(1)
            line = re.search(r"^Lời dẫn:\s*(.*)$", p, re.M).group(1).replace('"', "")
            parts = []
            for seg in line.split(" · "):
                m = re.match(r"\[([^\]]+)\]:\s*(.*)", seg.strip())
                spk, t = (m.group(1).strip(), m.group(2)) if m else ("NARRATOR", seg.strip())
                if t:
                    parts.append((spk, t))
            out.append((sid, parts))
    out.sort(key=lambda s: tuple(map(int, s[0].split("."))))
    return out


async def _tts(text, voice, mp3):
    import edge_tts
    import edge_tts.communicate as comm
    if os.path.exists(CA_BUNDLE):
        comm._SSL_CTX = ssl.create_default_context(cafile=CA_BUNDLE)
    name, rate, pitch = voice
    c = edge_tts.Communicate(text, name, rate=rate, pitch=pitch, boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(mp3, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    return words


def run_audio(k, spk, chunks):
    """Một lượt đọc liền: chunks = [(sid, text)]. Trả về (wav, dur, [(sid, text, start, end)])."""
    speak = [to_speech(t).split() for _, t in chunks]
    flat = [w for ws in speak for w in ws]
    mp3, wav = os.path.join(WORK, "tts", f"r{k:03d}.mp3"), os.path.join(WORK, "tts", f"r{k:03d}.wav")
    for attempt in range(4):
        try:
            words = asyncio.run(_tts(" ".join(flat), VOICES.get(spk, VOICES["NARRATOR"]), mp3))
            if words:
                break
        except Exception:
            if attempt == 3:
                raise
    sh(["ffmpeg", "-y", "-i", mp3, "-af", "silenceremove=start_periods=1:start_threshold=-50dB",
        "-ar", "48000", "-ac", "1", wav])
    lead_cut = duration(mp3) - duration(wav)
    dur = duration(wav)
    a, b = [norm(w) for w in flat], [norm(w[2]) for w in words]
    times = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for i in range(blk.size):
            s, e, _ = words[blk.b + i]
            times[blk.a + i] = (max(0.0, s - lead_cut), max(0.0, e - lead_cut))
    last = (0.0, 0.0)
    for i in range(len(times)):
        if times[i] is None:
            nxt = next((times[j] for j in range(i + 1, len(times)) if times[j]), (dur, dur))
            times[i] = (last[1], max(last[1], min(nxt[0], last[1] + 0.3)))
        last = times[i]
    dur = min(dur, times[-1][1] + 0.35)   # bỏ khoảng lặng thừa ở cuối lượt đọc
    res, i = [], 0
    for (sid, text), ws in zip(chunks, speak):
        res.append((sid, text, times[i][0], times[i + len(ws) - 1][1]))
        i += len(ws)
    return wav, dur, res


def motion(cam, n):
    p = f"(on/{max(n - 1, 1)})"
    cx, cy = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    if "tilt" in cam:
        return "1.14", cx, f"(ih-ih/zoom)*{p}"
    if "pan" in cam:
        x = f"(iw-iw/zoom)*(1-{p})" if "phải sang trái" in cam else f"(iw-iw/zoom)*{p}"
        return "1.12", x, cy
    if "pull" in cam:
        return f"1.16-0.13*{p}", cx, cy
    return f"1.03+0.11*{p}", cx, cy


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")


def render_clip(sid, cam, length):
    out = os.path.join(WORK, "clips", sid.replace(".", "_") + ".mp4")
    img = os.path.join(SCENES, f"canh_{sid.replace('.', '_')}.png")
    n = int(round(length * FPS))
    z, x, y = motion(cam, n)
    vf = (f"scale=3840:2160:flags=lanczos,"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1920x1080:fps={FPS}")
    if sid == TITLE_SCENE:
        vf += (f",drawbox=x=0:y=ih/2-170:w=iw:h=300:color=black@0.45:t=fill:enable='gte(t,1.2)',"
               f"drawtext=fontfile={FONT}:text='{esc('CHILDREN DON’T EAT DOG MEAT')}':fontsize=82:"
               f"fontcolor=0xF3EEDF:x=(w-text_w)/2:y=h/2-120:alpha='min(1,max(0,(t-1.4)/0.8))',"
               f"drawtext=fontfile={FONT}:text='{esc('Nam Cao · Trẻ con không được ăn thịt chó')}':"
               f"fontsize=42:fontcolor=0xE8B04A:x=(w-text_w)/2:y=h/2+20:alpha='min(1,max(0,(t-2.0)/0.8))'")
    if sid in OVERLAYS:
        vf += (f",drawtext=fontfile={FONT}:text='{esc(OVERLAYS[sid])}':fontsize=84:fontcolor=white:"
               f"borderw=6:bordercolor=black:x=(w-text_w)/2:y=h*0.16:"
               f"alpha='min(1,max(0,(t-0.8)/0.6))'")
    vf += ",format=yuv420p"
    sh(["ffmpeg", "-y", "-i", img, "-vf", vf, "-frames:v", str(n), "-r", str(FPS),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out])
    return out


def xfade_chain(files, lengths, kinds, out):
    if len(files) == 1:
        sh(["ffmpeg", "-y", "-i", files[0], "-c", "copy", out])
        return lengths[0]
    inputs = []
    for f in files:
        inputs += ["-i", f]
    flt, prev, acc = [], "[0:v]", lengths[0]
    for i in range(1, len(files)):
        lab = f"[v{i}]"
        flt.append(f"{prev}[{i}:v]xfade=transition={kinds[i]}:duration={XF}:offset={acc - XF:.3f}{lab}")
        prev, acc = lab, acc + lengths[i] - XF
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", prev,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out])
    return acc


def cues(text, s, e, max_words=9):
    """Chia một đoạn chữ thành cụm phụ đề, chia thời gian theo số ký tự."""
    words, groups, cur = text.split(), [], []
    for w in words:
        cur.append(w)
        if w[-1] in ".?!" or len(cur) >= max_words or (w[-1] in ",:;" and len(cur) >= 5):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    total = sum(len(" ".join(g)) for g in groups) or 1
    out, t = [], s
    for g in groups:
        g_txt = " ".join(g)
        d = (e - s) * len(g_txt) / total
        out.append((g_txt, t, t + d))
        t += d
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", type=int, default=4)
    a = ap.parse_args()
    for d in ("tts", "clips", "chunks"):
        os.makedirs(os.path.join(WORK, d), exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    scenes = load_scenes()
    # gom thành các lượt đọc: lời dẫn liền nhau trong một chương đọc một lần
    runs = []   # (chương, người nói, [(sid, text)])
    for sid, parts in scenes:
        ch = sid.split(".")[0]
        for spk, t in parts:
            if runs and runs[-1][0] == ch and runs[-1][1] == spk == "NARRATOR":
                runs[-1][2].append((sid, t))
            else:
                runs.append((ch, spk, [(sid, t)]))
    print(f"{len(scenes)} cảnh, {len(runs)} lượt đọc. Tạo giọng đọc…", flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(lambda k: run_audio(k, runs[k][1], runs[k][2]), range(len(runs))))

    # dòng thời gian
    t, audio_parts, scene_start, subs, prev_ch = LEAD, [], {}, [], None
    for (ch, spk, _), (wav, dur, chunks) in zip(runs, res):
        if prev_ch is not None:
            t += CH_GAP if ch != prev_ch else LINE_GAP
        audio_parts.append((wav, t))
        for sid, text, s, e in chunks:
            scene_start.setdefault(sid, t + s)
            subs += cues(text, t + s, t + e)
        t += dur
        prev_ch = ch
    total = t + TAIL
    print(f"Giọng đọc: {(t - LEAD) / 60:.1f} phút", flush=True)

    sids = [sid for sid, _ in scenes]
    bounds = [0.0] + [scene_start[s] - CUT_EARLY for s in sids[1:]]
    lengths = []
    for i in range(len(sids)):
        end = bounds[i + 1] if i + 1 < len(sids) else total
        lengths.append(end - bounds[i] + XF * (0.5 if i == 0 or i == len(sids) - 1 else 1.0))
    kinds = ["fade"] + ["fadeblack" if sids[i].split(".")[0] != sids[i - 1].split(".")[0] else "fade"
                        for i in range(1, len(sids))]

    print("Dựng chuyển động từng cảnh…", flush=True)
    with ThreadPoolExecutor(max_workers=a.j) as ex:
        clips = list(ex.map(lambda k: render_clip(sids[k], CAMS[k % len(CAMS)], lengths[k]),
                            range(len(sids))))

    print("Nối cảnh…", flush=True)
    size = 12
    cf, cl, ck = [], [], []
    for c, s in enumerate(range(0, len(clips), size)):
        f = os.path.join(WORK, "chunks", f"c{c:02d}.mp4")
        cl.append(xfade_chain(clips[s:s + size], lengths[s:s + size], kinds[s:s + size], f))
        cf.append(f)
        ck.append(kinds[s])
    video = os.path.join(WORK, "video_noaudio.mp4")
    vlen = xfade_chain(cf, cl, ck, video)
    shift = XF / 2   # mỗi cảnh hiện lùi XF/2 so với mốc -> lùi âm thanh tương ứng

    print("Âm thanh + phụ đề…", flush=True)
    # trộn theo từng nhóm 40 đoạn để lệnh ffmpeg không quá dài
    groups, gi = [], 0
    for s in range(0, len(audio_parts), 40):
        inputs, flt = [], []
        part = audio_parts[s:s + 40]
        for k, (wav, start) in enumerate(part):
            inputs += ["-i", wav]
            flt.append(f"[{k}:a]adelay={int((start + shift) * 1000)}[a{k}]")
        flt.append("".join(f"[a{k}]" for k in range(len(part))) +
                   f"amix=inputs={len(part)}:normalize=0,apad=whole_dur={vlen:.3f}[out]")
        g = os.path.join(WORK, f"mix{gi}.wav")
        sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
            "-ar", "48000", "-ac", "1", g])
        groups.append(g)
        gi += 1
    audio = os.path.join(WORK, "narration.wav")
    inputs = []
    for g in groups:
        inputs += ["-i", g]
    sh(["ffmpeg", "-y", *inputs, "-filter_complex",
        "".join(f"[{k}:a]" for k in range(len(groups))) +
        f"amix=inputs={len(groups)}:normalize=0,atrim=0:{vlen:.3f}[o]",
        "-map", "[o]", "-ar", "48000", "-ac", "1", audio])

    srt = os.path.join(OUT, f"{NAME}.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for i, (text, s, e) in enumerate(subs, 1):
            f.write(f"{i}\n{srt_time(s + shift)} --> {srt_time(e + shift + 0.15)}\n{text}\n\n")

    final = os.path.join(OUT, f"{NAME}.mp4")
    style = ("FontName=DejaVu Sans,FontSize=19,Bold=1,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=34")
    sh(["ffmpeg", "-y", "-i", video, "-i", audio,
        "-vf", f"subtitles={srt}:force_style='{style}'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
        "-shortest", "-movflags", "+faststart", final])
    print(f"Xong: {final} ({vlen / 60:.1f} phút)")


if __name__ == "__main__":
    main()
