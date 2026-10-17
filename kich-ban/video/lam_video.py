"""Dựng video Chí Phèo từ ảnh phân cảnh + giọng người kể.

- Giọng kể: edge-tts (vi-VN-NamMinhNeural), chỉ một người kể từ đầu đến cuối.
- Chuyển động: Ken Burns (tiến / lùi / lia ngang / lia dọc, rung máy) theo cột "Máy"
  trong CHI_PHEO_PHAN_CANH.md.
- Chuyển cảnh: hòa tan giữa các cảnh, mờ qua màn đen khi sang chương mới.
- Phụ đề tiếng Việt đốt vào hình + xuất file .srt riêng.

Chạy:  python3 lam_video.py            (toàn bộ)
       python3 lam_video.py --chi-am   (chỉ tạo giọng đọc)
Kết quả: out/ChiPheo.mp4, out/ChiPheo.srt
"""
import argparse
import asyncio
import os
import re
import ssl
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCENES = os.path.join(ROOT, "tao-hinh", "phan-canh")
SHOTLIST = os.path.join(ROOT, "CHI_PHEO_PHAN_CANH.md")
NARRATION = os.path.join(HERE, "LOI_KE.txt")
WORK = os.path.join(HERE, "work")
OUT = os.path.join(HERE, "out")

VOICE = "vi-VN-NamMinhNeural"
RATE = "-4%"
FPS = 30
W, H = 1920, 1080
XF = 0.6          # thời lượng chuyển cảnh (giây)
LEAD = 0.45       # lặng trước lời kể của mỗi cảnh
TAIL = 0.55       # lặng sau lời kể
GAP = 0.7         # khoảng ngừng cho dấu " / "
SR = 48000
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
SUFFIX = ""
PHONETIC = {}

LANGS = {
    "vi": dict(narration="LOI_KE.txt", voice="vi-VN-NamMinhNeural", rate="-4%",
               work="work", suffix="", phonetic={}),
    # Bản tiếng Anh: giọng Mỹ, tên tiếng Việt đọc theo phiên âm (phụ đề vẫn giữ chữ gốc).
    "en": dict(narration="LOI_KE_EN.txt", voice="en-US-AndrewNeural", rate="+0%",
               work="work_en", suffix="_EN", phonetic={
                   "Chí Phèo": "Chee Feh-oh", "Chí": "Chee", "Bá Kiến": "Bah Kee-en",
                   "Kiến": "Kee-en", "Bà Ba": "Bah Bah", "Bá": "Bah", "Lý Cường": "Lee Kuh-ung",
                   "Thị Nở": "Tee Nuh", "Vũ Đại": "Voo Dye", "Nam Cao": "Nahm Cow",
                   "Tảo": "Tao", "sào": "sow"}),
}


def to_speech(text):
    """Thay tên riêng bằng phiên âm trước khi đưa cho giọng đọc (khóa dài thay trước)."""
    for k in sorted(PHONETIC, key=len, reverse=True):
        text = re.sub(rf"(?<!\w){re.escape(k)}(?!\w)", PHONETIC[k], text)
    return text


def sh(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Lỗi lệnh: {' '.join(cmd[:6])}…\n{r.stderr[-1500:]}")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def key(sid):
    return tuple(map(int, sid.split(".")))


def load_narration():
    items = []
    for line in open(NARRATION, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sid, text = line.split("|", 1)
        items.append((sid.strip(), text.strip()))
    return sorted(items, key=lambda x: key(x[0]))


def load_camera():
    """Đọc cột 'Máy' của từng cảnh để chọn kiểu chuyển động."""
    text = open(SHOTLIST, encoding="utf-8").read()
    cams = {}
    for p in re.split(r"^#### CẢNH ", text, flags=re.M)[1:]:
        sid = p.split()[0]
        m = re.search(r"\*\*Khung hình / Máy:\*\*([^\n]*)", p)
        cams[sid] = (m.group(1) if m else "").lower()
    return cams


# ---------------------------------------------------------------- giọng đọc
async def _tts(text, path):
    import edge_tts
    import edge_tts.communicate as comm
    # edge-tts tự gắn certifi; ở môi trường này phải tin CA của proxy (không tắt xác minh TLS)
    if os.path.exists(CA_BUNDLE):
        comm._SSL_CTX = ssl.create_default_context(cafile=CA_BUNDLE)
    c = edge_tts.Communicate(to_speech(text), VOICE, rate=RATE, proxy=os.environ.get("HTTPS_PROXY"))
    await c.save(path)


def make_voice(sid, text):
    """Tạo wav lời kể của một cảnh; trả về (đường dẫn, độ dài, [(đoạn, bắt đầu, kết thúc)])."""
    base = os.path.join(WORK, "voice", sid.replace(".", "_"))
    wav = base + ".wav"
    parts = [t.strip() for t in text.split(" / ") if t.strip()]
    seg_files = []
    for i, part in enumerate(parts):
        mp3 = f"{base}_{i}.mp3"
        if not os.path.exists(mp3) or os.path.getsize(mp3) == 0:
            for attempt in range(3):
                try:
                    asyncio.run(_tts(part, mp3))
                    break
                except Exception:
                    if attempt == 2:
                        raise
        seg_files.append(mp3)
    timings, t = [], 0.0
    inputs, filters = [], []
    for i, f in enumerate(seg_files):
        d = duration(f)
        timings.append((parts[i], t, t + d))
        t += d + (GAP if i < len(seg_files) - 1 else 0)
        inputs += ["-i", f]
        filters.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=mono[a{i}]")
    chain = ""
    for i in range(len(seg_files)):
        chain += f"[a{i}]"
        if i < len(seg_files) - 1:
            filters.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{GAP}[g{i}]")
            chain += f"[g{i}]"
    n = len(seg_files) * 2 - 1
    filters.append(f"{chain}concat=n={n}:v=0:a=1[out]")
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", wav])
    return wav, duration(wav), timings


# ---------------------------------------------------------------- hình động
def motion(cam, n):
    """Biểu thức zoompan (z, x, y) cho n khung hình."""
    p = f"(on/{max(n - 1, 1)})"
    ease = f"(0.5-0.5*cos(PI*{p}))"
    cx, cy = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    shake = "+6*sin(on*1.7)" if "rung" in cam else ""
    if "tilt" in cam:
        down = "xuống" in cam
        y = f"(ih-ih/zoom)*({ease})" if down else f"(ih-ih/zoom)*(1-{ease})"
        return "1.18", cx + shake, y
    if "pan" in cam and "push" not in cam:
        rtl = "phải sang trái" in cam
        x = f"(iw-iw/zoom)*(1-{ease})" if rtl else f"(iw-iw/zoom)*({ease})"
        return "1.15", x + shake, cy
    if "pull" in cam:
        return f"1.22-0.20*{ease}", cx + shake, cy
    if "static" in cam and "push" not in cam:
        return f"1.04+0.03*{ease}", cx + shake, cy
    return f"1.0+0.16*{ease}", cx + shake, cy          # mặc định: tiến vào chậm


def render_clip(sid, cam, length):
    out = os.path.join(WORK, "clips", sid.replace(".", "_") + ".mp4")
    img = os.path.join(SCENES, f"canh_{sid.replace('.', '_')}.png")
    n = int(round(length * FPS))
    z, x, y = motion(cam, n)
    vf = (f"scale=3200:1800:flags=lanczos,"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS}")
    if sid == "0.9":   # tên phim
        vf += (f",drawtext=fontfile={FONT}:text='CHÍ PHÈO':fontsize=150:fontcolor=0xB3261E:"
               f"x=(w-text_w)/2:y=(h-text_h)/2-60:alpha='min(1,max(0,(t-0.6)/0.8))',"
               f"drawtext=fontfile={FONT}:text='Nam Cao · 1941':fontsize=48:fontcolor=0x3B332B:"
               f"x=(w-text_w)/2:y=h/2+70:alpha='min(1,max(0,(t-1.2)/0.8))'")
    vf += ",format=yuv420p"
    sh(["ffmpeg", "-y", "-i", img, "-vf", vf, "-frames:v", str(n), "-r", str(FPS),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out])
    return out


def xfade_chain(files, lengths, kinds, out):
    """Nối clip bằng xfade; kinds[i] = kiểu chuyển vào clip i (i>=1). Trả về tổng độ dài."""
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


# ---------------------------------------------------------------- phụ đề
def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_cue(text, start, end, max_words=13):
    words = text.split()
    if len(words) <= max_words:
        return [(text, start, end)]
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or (w[-1] in ".?!:" and len(cur) >= 5):
            chunks.append(" ".join(cur))
            cur = []
    if cur:
        chunks.append(" ".join(cur))
    total = sum(len(c) for c in chunks)
    out, t = [], start
    for c in chunks:
        d = (end - start) * len(c) / total
        out.append((c, t, t + d))
        t += d
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chi-am", action="store_true")
    ap.add_argument("-j", type=int, default=4)
    ap.add_argument("--lang", choices=sorted(LANGS), default="vi")
    a = ap.parse_args()
    global NARRATION, WORK, VOICE, RATE, SUFFIX, PHONETIC
    cfg = LANGS[a.lang]
    NARRATION = os.path.join(HERE, cfg["narration"])
    WORK = os.path.join(HERE, cfg["work"])
    VOICE, RATE, SUFFIX, PHONETIC = cfg["voice"], cfg["rate"], cfg["suffix"], cfg["phonetic"]
    for d in ("voice", "clips", "chunks"):
        os.makedirs(os.path.join(WORK, d), exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    items = load_narration()
    cams = load_camera()
    print(f"{len(items)} cảnh. Tạo giọng đọc…", flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        voices = list(ex.map(lambda it: make_voice(*it), items))
    print(f"Giọng đọc: {sum(v[1] for v in voices) / 60:.1f} phút", flush=True)
    if a.chi_am:
        return

    lengths = [LEAD + v[1] + TAIL + XF for v in voices]
    lengths[-1] += 1.5
    chapters = [sid.split(".")[0] for sid, _ in items]
    kinds = ["fade"] + ["fadeblack" if chapters[i] != chapters[i - 1] else "fade"
                        for i in range(1, len(items))]

    print("Dựng chuyển động từng cảnh…", flush=True)
    with ThreadPoolExecutor(max_workers=a.j) as ex:
        clips = list(ex.map(lambda k: render_clip(items[k][0], cams.get(items[k][0], ""),
                                                  lengths[k]), range(len(items))))

    print("Nối cảnh + chuyển cảnh…", flush=True)
    size = 12
    chunk_files, chunk_lens, chunk_kinds = [], [], []
    for c, s in enumerate(range(0, len(clips), size)):
        f = os.path.join(WORK, "chunks", f"c{c:02d}.mp4")
        chunk_lens.append(xfade_chain(clips[s:s + size], lengths[s:s + size], kinds[s:s + size], f))
        chunk_files.append(f)
        chunk_kinds.append(kinds[s])
    video = os.path.join(WORK, "video_noaudio.mp4")
    total = xfade_chain(chunk_files, chunk_lens, chunk_kinds, video)

    print("Ghép âm thanh + phụ đề…", flush=True)
    audio_parts, cues, t = [], [], 0.0
    for k, (wav, d, timings) in enumerate(voices):
        slot = lengths[k] - (XF if k < len(voices) - 1 else 0)
        part = os.path.join(WORK, "voice", f"slot_{k:03d}.wav")
        sh(["ffmpeg", "-y", "-i", wav, "-af",
            f"adelay={int(LEAD * 1000)},apad=whole_dur={slot:.3f}", "-ar", str(SR), "-ac", "1", part])
        audio_parts.append(part)
        for text, s, e in timings:
            cues += split_cue(text, t + LEAD + s, t + LEAD + e)
        t += slot
    lst = os.path.join(WORK, "audio_list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in audio_parts)
    audio = os.path.join(WORK, "narration.wav")
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", audio])

    srt = os.path.join(OUT, f"ChiPheo{SUFFIX}.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for i, (text, s, e) in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{text}\n\n")

    final = os.path.join(OUT, f"ChiPheo{SUFFIX}.mp4")
    style = ("FontName=DejaVu Sans,FontSize=20,Bold=1,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=36")
    sh(["ffmpeg", "-y", "-i", video, "-i", audio,
        "-vf", f"subtitles={srt}:force_style='{style}'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-shortest", "-movflags", "+faststart", final])
    print(f"Xong: {final} ({total / 60:.1f} phút)")


if __name__ == "__main__":
    main()
