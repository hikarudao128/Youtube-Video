"""Ghép chữ lên ảnh nền thumbnail YouTube (1280x720).

python ghep_thumbnail.py nen.png ra.jpg --mau a   # "ONE POT. / TWO BODIES." bên trái
python ghep_thumbnail.py nen.png ra.jpg --mau b   # "GENTLE" / "DEMON" hai bên mặt
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1280, 720
FONT = Path(__file__).parent / "fonts" / "Anton-Regular.ttf"
VANG = (255, 214, 0)
TRANG = (255, 255, 255)
DO = (235, 35, 35)


def chu(im, xy, text, size, fill, anchor="la", stroke=10):
    """Chữ có viền đen dày + bóng đổ mờ, đọc được ở cỡ nhỏ."""
    f = ImageFont.truetype(str(FONT), size)
    bong = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(bong).text((xy[0] + 8, xy[1] + 10), text, font=f, anchor=anchor,
                              fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    im.alpha_composite(bong.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).text(xy, text, font=f, anchor=anchor, fill=fill,
                            stroke_width=stroke, stroke_fill=(0, 0, 0))


def lop_toi(im, mask):
    """Phủ đen theo mask (L) để chữ nổi lên."""
    den = Image.new("RGBA", im.size, (0, 0, 0, 0))
    den.putalpha(mask)
    im.alpha_composite(den)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nen")
    ap.add_argument("ra")
    ap.add_argument("--mau", choices=["a", "b"], required=True)
    a = ap.parse_args()

    im = ImageOps.fit(Image.open(a.nen).convert("RGB"), (W, H), Image.LANCZOS).convert("RGBA")
    g = Image.linear_gradient("L")  # trên đen (0) → dưới trắng (255)
    if a.mau == "a":
        m = Image.new("L", im.size, 0)
        m.paste(g.rotate(-90).resize((620, H)).point(lambda v: int(v * 0.75)), (0, 0))
        lop_toi(im, m)
        chu(im, (50, 40), "ONE POT.", 200, TRANG)
        chu(im, (50, 300), "TWO", 200, VANG)
        chu(im, (50, 520), "BODIES.", 150, DO)
    else:
        m = Image.new("L", im.size, 0)
        m.paste(g.rotate(180).resize((W, 260)).point(lambda v: int(v * 0.7)), (0, 0))
        lop_toi(im, m)
        # mặt nhân vật nằm khoảng x 420–820: chữ đặt vào hai khoảng trời hai bên
        chu(im, (215, 40), "GENTLE", 140, VANG, anchor="mt")
        chu(im, (1065, 40), "DEMON", 140, DO, anchor="mt")
    im.convert("RGB").save(a.ra, quality=92)
    print(a.ra, Path(a.ra).stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
