"""Ghép ảnh phân cảnh thành các trang storyboard, mỗi trang 4 cảnh (lưới 2x2).

Dưới mỗi ảnh: số cảnh, thời gian, và dòng "Lời dẫn:" lấy từ
phan-canh-prompt/chuong_*.md. Xuất ra storyboard/storyboard_XX.jpg.

Chạy:  python3 ghep_storyboard.py
"""
import glob
import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCENES_DIR = os.path.join(HERE, "phan-canh")
OUT_DIR = os.path.join(HERE, "storyboard")
SCENE_GLOB = os.path.join(HERE, "phan-canh-prompt", "chuong_*.md")
TITLE = "TRẺ CON KHÔNG ĐƯỢC ĂN THỊT CHÓ · STORYBOARD"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (243, 238, 223)
INK = (40, 34, 28)
RED = (179, 38, 30)
GREY = (110, 100, 90)
CELL_W, CELL_H = 960, 540
CAP_H = 160
MAX_LINES = 4
GAP = 30
MARGIN = 40
HEADER = 80
PAGE_W = MARGIN * 2 + CELL_W * 2 + GAP
PAGE_H = HEADER + MARGIN + (CELL_H + CAP_H) * 2 + GAP + MARGIN

CHAPTERS = {
    "0": "Mở đầu", "1": "Mười gốc chuối", "2": "Con chó ở bờ rào", "3": "Đi chợ về",
    "4": "Bữa nhậu", "5": "Cái mâm", "6": "Kết",
}


def clean(s):
    s = re.sub(r"\*\([^)]*\)\*", " ", s)          # ghi chú diễn xuất *(ngừng…)*
    s = re.sub(r"\*+", "", s)
    s = s.replace('"', "")
    s = re.sub(r"\s{2,}", " ", s).strip()
    # bỏ lượt thoại rỗng như "· [CHÍ]:" còn lại sau khi xóa ghi chú diễn xuất
    s = re.sub(r"\s*·?\s*\[[^\]]+\]:\s*(?=·|$)", "", s).strip(" ·")
    return s


def load_shotlist():
    """{ '0.1': {'time': '0:00–0:05', 'tag': '', 'text': '...'} }"""
    info = {}
    for path in sorted(glob.glob(SCENE_GLOB)):
        text = open(path, encoding="utf-8").read()
        for p in re.split(r"^#### CẢNH ", text, flags=re.M)[1:]:
            m = re.match(r"(\d+\.\d+)\s*·\s*([\d:–-]+)", p)
            if not m:
                continue
            hit = re.search(r"^Lời dẫn:\s*(.*)$", p, re.M)
            body = clean(hit.group(1)) if hit else ""
            info[m.group(1)] = {"time": m.group(2), "tag": "", "text": body}
    return info


def wrap_px(d, text, font, max_w):
    """Ngắt dòng theo độ rộng pixel thật của chữ."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(img):
    img = img.convert("RGB")
    r = min(CELL_W / img.width, CELL_H / img.height)
    img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    cell = Image.new("RGB", (CELL_W, CELL_H), (225, 219, 204))
    cell.paste(img, ((CELL_W - img.width) // 2, (CELL_H - img.height) // 2))
    return cell


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    info = load_shotlist()
    ids = sorted(info, key=lambda s: tuple(map(int, s.split("."))))
    f_head = ImageFont.truetype(FONT_B, 30)
    f_page = ImageFont.truetype(FONT, 26)
    f_id = ImageFont.truetype(FONT_B, 28)
    f_time = ImageFont.truetype(FONT, 22)
    f_txt = ImageFont.truetype(FONT, 22)
    pages = [ids[i:i + 4] for i in range(0, len(ids), 4)]
    missing = []
    for pi, page in enumerate(pages, 1):
        im = Image.new("RGB", (PAGE_W, PAGE_H), BG)
        d = ImageDraw.Draw(im)
        chaps = sorted({s.split(".")[0] for s in page}, key=int)
        d.text((MARGIN, 24), TITLE, font=f_head, fill=RED)
        sub = " / ".join(f"Chương {c}: {CHAPTERS[c]}" for c in chaps)
        d.text((MARGIN + d.textlength(TITLE, font=f_head) + 30, 30), sub, font=f_page, fill=INK)
        pg = f"Trang {pi}/{len(pages)}"
        d.text((PAGE_W - MARGIN - d.textlength(pg, font=f_page), 30), pg, font=f_page, fill=GREY)
        d.line((MARGIN, HEADER, PAGE_W - MARGIN, HEADER), fill=INK, width=3)
        for k, sid in enumerate(page):
            x = MARGIN + (k % 2) * (CELL_W + GAP)
            y = HEADER + MARGIN + (k // 2) * (CELL_H + CAP_H + GAP)
            path = os.path.join(SCENES_DIR, f"canh_{sid.replace('.', '_')}.png")
            if os.path.exists(path):
                im.paste(fit(Image.open(path)), (x, y))
            else:
                missing.append(sid)
                d.rectangle((x, y, x + CELL_W, y + CELL_H), fill=(210, 204, 190))
                msg = "Chưa có ảnh"
                d.text((x + CELL_W / 2 - d.textlength(msg, font=f_id) / 2, y + CELL_H / 2 - 16),
                       msg, font=f_id, fill=GREY)
            d.rectangle((x, y, x + CELL_W, y + CELL_H), outline=INK, width=3)
            meta = info[sid]
            cy = y + CELL_H + 12
            label = f"CẢNH {sid}"
            d.text((x, cy), label, font=f_id, fill=RED)
            d.text((x + d.textlength(label, font=f_id) + 18, cy + 5), meta["time"], font=f_time, fill=GREY)
            wrapped = wrap_px(d, meta["tag"] + meta["text"], f_txt, CELL_W - 10)
            lines = wrapped[:MAX_LINES]
            if len(wrapped) > MAX_LINES:
                last = lines[-1].rstrip(" .,")
                while d.textlength(last + "…", font=f_txt) > CELL_W - 10:
                    last = last.rsplit(" ", 1)[0]
                lines[-1] = last + "…"
            for li, l in enumerate(lines):
                d.text((x, cy + 42 + li * 27), l, font=f_txt, fill=INK)
        im.save(os.path.join(OUT_DIR, f"storyboard_{pi:02d}.jpg"), quality=90)
    print(f"{len(pages)} trang -> {OUT_DIR}; thiếu ảnh: {', '.join(missing) or 'không'}")


if __name__ == "__main__":
    main()
