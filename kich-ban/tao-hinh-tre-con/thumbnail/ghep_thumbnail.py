"""Gắn chữ lên nền thumbnail (nen_1.png, nen_2.png) -> thumbnail_1.png, thumbnail_2.png (1280x720, 16:9).

Nền do Codex vẽ (prompt_1.txt, prompt_2.txt), chữ gắn ở đây để không bị sai chính tả.
Chạy:  python3 ghep_thumbnail.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
W, H = 1280, 720
YELLOW = (255, 214, 64)
WHITE = (255, 255, 255)


def base(name):
    img = Image.open(os.path.join(HERE, name)).convert("RGB")
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


def shade(img, box, alpha=170, blur=40):
    """Làm tối một vùng (mép mờ) để chữ nổi lên."""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rectangle(box, fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, mask)


def text(img, xy, s, size, fill, anchor="la", stroke=10, max_w=None):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    while max_w and d.textlength(s, font=f) + 2 * stroke > max_w:
        size -= 2
        f = ImageFont.truetype(FONT, size)
    x, y = xy
    d.text((x + 6, y + 8), s, font=f, fill=(0, 0, 0), anchor=anchor, stroke_width=stroke,
           stroke_fill=(0, 0, 0))
    d.text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))


def thumb_1():
    img = base("nen_1.png")
    img = shade(img, (0, 560, W, H + 60), alpha=170)
    split = int(W * 0.435)   # đường chia hai nửa trong tranh nền
    text(img, (split / 2, H - 22), "4 MEN ATE.", 120, YELLOW, anchor="md", max_w=split - 40)
    text(img, ((split + W) / 2, H - 22), "5 CRIED.", 120, WHITE, anchor="md", max_w=W - split - 40)
    img.save(os.path.join(HERE, "thumbnail_1.png"))


def thumb_2():
    img = base("nen_2.png")
    img = shade(img, (0, 120, 640, 600), alpha=120, blur=60)
    for y, word, color in ((170, "WAIT FOR", WHITE), (300, "THE", WHITE), (430, "LEFTOVERS", YELLOW)):
        text(img, (50, y), word, 112, color, max_w=560)
    img.save(os.path.join(HERE, "thumbnail_2.png"))


if __name__ == "__main__":
    thumb_1()
    thumb_2()
    print("Xong: thumbnail_1.png, thumbnail_2.png")
