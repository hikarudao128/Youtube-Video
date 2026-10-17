# Chạy trong thư mục nguoi-que:  python3 tools/cat-sprite.py tao-hinh/neoptolemus.webp sprites.js
# Cần: pip install opencv-python-headless numpy
# Cắt tạo hình Neoptolemus thành sprite: đầu, thân (đã xoá tay chân), lớp áo phía trước.
import cv2, numpy as np, json, base64, sys
src = cv2.imread(sys.argv[1] if len(sys.argv) > 1 else 'tao-hinh/neoptolemus.webp')                      # BGR
H, W = src.shape[:2]
BG = np.array([214, 230, 237], np.int16)                    # BGR nền giấy
INK = (20, 24, 30)
CAPE = np.array([62, 51, 110], np.int16)            # BGR màu áo choàng

# 1) Nền: vùng gần màu nền nối với mép ảnh
near = (np.abs(src.astype(np.int16) - BG).sum(2) < 30).astype(np.uint8)
n, lab = cv2.connectedComponents(near, connectivity=4)
border = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
bg = np.isin(lab, list(border))

def line(m, a, b, w): cv2.line(m, a, b, 255, w, cv2.LINE_AA)
def ell(m, c, ax): cv2.ellipse(m, c, ax, 0, 0, 360, 255, -1)

VIEWS = {
  'front': dict(
    erase=lambda m: [line(m, (164, 296), (129, 447), 13), ell(m, (123, 469), (24, 33)),
                     line(m, (277, 300), (302, 447), 14), ell(m, (308, 470), (24, 32)),
                     line(m, (172, 515), (170, 640), 15), line(m, (247, 515), (249, 640), 15)],
    cape=lambda m: [line(m, (277, 300), (302, 447), 14), ell(m, (308, 470), (24, 32)),
                    line(m, (164, 296), (129, 447), 13), ell(m, (123, 469), (24, 33)),
                    line(m, (172, 515), (170, 640), 15), line(m, (247, 515), (249, 640), 15)],
    seed=(210, 470), body=(40, 244, 345, 615), head=(90, 40, 345, 256), front_y=420, sword=None,
    rig=dict(hipL=(174, 470), hipR=(246, 470), shL=(164, 302), shR=(277, 306), neck=(213, 246))),
  'tq': dict(
    erase=lambda m: [line(m, (585, 286), (552, 447), 13), ell(m, (542, 469), (24, 33)),
                     line(m, (692, 300), (712, 447), 14), ell(m, (721, 469), (24, 32)),
                     line(m, (591, 515), (588, 640), 15), line(m, (662, 515), (664, 640), 15)],
    cape=lambda m: [line(m, (692, 300), (712, 447), 14), ell(m, (721, 469), (24, 32)),
                    line(m, (585, 286), (552, 447), 13), ell(m, (542, 469), (24, 33)),
                    line(m, (591, 515), (588, 640), 15), line(m, (662, 515), (664, 640), 15)],
    seed=(630, 470), body=(455, 242, 765, 615), head=(505, 40, 765, 254), front_y=420, sword=None,
    rig=dict(hipL=(592, 470), hipR=(660, 470), shL=(585, 292), shR=(692, 306), neck=(628, 244))),
  'side': dict(
    erase=lambda m: [line(m, (1006, 292), (1022, 447), 11), ell(m, (1030, 472), (27, 33)),
                     line(m, (1013, 506), (1013, 660), 19)],
    blade=dict(top=(1010, 395), slope=0.19, y=(406, 512), w=19),   # vẽ lại lưỡi kiếm bị bàn tay che
    seed=(985, 470), body=(905, 246, 1180, 665), head=(900, 35, 1155, 258), front_y=410,
    sword=[(990, 392), (1013, 386), (1062, 560), (1040, 574)],
    rig=dict(hipL=(1013, 475), hipR=(1013, 475), shL=(1006, 296), shR=(1006, 296), neck=(1004, 250))),
}

def rgba(img, alpha, box):
    x0, y0, x1, y1 = box
    out = np.dstack([img[y0:y1, x0:x1], alpha[y0:y1, x0:x1]])
    return out

def png_b64(a):
    ok, buf = cv2.imencode('.png', a, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    return 'data:image/png;base64,' + base64.b64encode(buf).decode()

sprites, rig = {}, {}
for name, v in VIEWS.items():
    # Đầu: lấy nguyên từ ảnh gốc
    head_alpha = np.where(bg, 0, 255).astype(np.uint8)
    hx0, hy0, hx1, hy1 = v['head']
    head = rgba(src, head_alpha, v['head'])
    

    # Thân: xoá tay, bàn tay, chân rồi vá
    m = np.zeros((H, W), np.uint8); v['erase'](m)
    m = (m > 0).astype(np.uint8) * 255
    comp = src.copy(); comp[bg] = (0, 255, 0)
    # Tô vùng đã xoá bằng màu của điểm gần nhất không phải nét mực (giữ màu phẳng, không nhoè)
    lum = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ink = (lum < 42) & ~bg
    mk = cv2.dilate(m, np.ones((3, 3), np.uint8)) > 0
    holes = mk | (ink & (cv2.dilate(m, np.ones((15, 15), np.uint8)) > 0))
    halo = cv2.dilate(ink.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0   # viền sáng quanh nét mực
    srcmask = np.where(holes | halo, 255, 0).astype(np.uint8)
    _, lbl = cv2.distanceTransformWithLabels(srcmask, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(srcmask == 0)
    lut_y = np.zeros(lbl.max() + 1, np.int32); lut_x = np.zeros(lbl.max() + 1, np.int32)
    lut_y[lbl[zy, zx]] = zy; lut_x[lbl[zy, zx]] = zx
    fixed = comp.copy()
    hy, hx = np.nonzero(mk)
    fixed[hy, hx] = comp[lut_y[lbl[hy, hx]], lut_x[lbl[hy, hx]]]
    if 'cape' in v:
        cm = np.zeros((H, W), np.uint8); v['cape'](cm)
        cm = (cv2.dilate(cm, np.ones((3, 3), np.uint8)) > 0) & mk & ~np.all(fixed == (0, 255, 0), 2)
        capey = (np.abs(src.astype(np.int16) - CAPE).sum(2) < 70) & ~holes & ~halo
        cs = np.where(capey, 0, 255).astype(np.uint8)
        _, lb2 = cv2.distanceTransformWithLabels(cs, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        zy, zx = np.nonzero(cs == 0)
        ly = np.zeros(lb2.max() + 1, np.int32); lx = np.zeros(lb2.max() + 1, np.int32)
        ly[lb2[zy, zx]] = zy; lx[lb2[zy, zx]] = zx
        hy, hx = np.nonzero(cm)
        fixed[hy, hx] = src[ly[lb2[hy, hx]], lx[lb2[hy, hx]]]
    fixed = np.where(mk[..., None], cv2.medianBlur(fixed, 5), fixed)
    alpha = np.where(np.all(fixed == (0, 255, 0), 2), 0, 255).astype(np.uint8)
    alpha[bg] = 0
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # vẽ lại viền ở mép bóng mới tạo trong vùng đã xoá
    zone = cv2.dilate(m, np.ones((9, 9), np.uint8)) > 0
    inner = cv2.erode(alpha, np.ones((5, 5), np.uint8))
    edge = (alpha > 0) & (inner == 0) & zone
    fixed[edge] = INK
    if 'blade' in v:
        bl = v['blade']; (tx, ty), k, (ya, yb), bw = bl['top'], bl['slope'], bl['y'], bl['w']
        cx = lambda y: tx + k * (y - ty)
        poly = np.array([(cx(ya) - bw / 2, ya), (cx(ya) + bw / 2, ya), (cx(yb) + bw / 2, yb), (cx(yb) - bw / 2, yb)], np.int32)
        cv2.fillPoly(fixed, [poly], (70, 114, 160), cv2.LINE_AA)
        cv2.line(fixed, tuple(poly[0]), tuple(poly[3]), INK, 2, cv2.LINE_AA)
        cv2.line(fixed, tuple(poly[1]), tuple(poly[2]), INK, 2, cv2.LINE_AA)
    # điểm vá trên nền xanh không được lọt màu xanh
    fixed[alpha == 0] = BG.astype(np.uint8)
    body = rgba(fixed, alpha, v['body'])
    

    # Lớp áo phía trước (che hông, chân mọc ra từ dưới gấu áo)
    ff = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(src.copy(), ff, v['seed'], 0, (12, 12, 12), (12, 12, 12), 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
    tun = ff[1:-1, 1:-1]
    tun = cv2.morphologyEx(tun, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    tun = cv2.dilate(tun, np.ones((9, 9), np.uint8))
    tun[:v['front_y']] = 0
    if v['sword']: cv2.fillPoly(tun, [np.array(v['sword'])], 255)
    fa = np.minimum(alpha, tun)
    front = rgba(fixed, fa, v['body'])
    

    for part, arr in (('head', head), ('body', body), ('front', front)):
        sprites[f'{name}_{part}'] = png_b64(arr)
    rig[name] = dict(v['rig'], head=v['head'][:2], body=v['body'][:2])

js = '// Sprite cắt từ bản thiết kế Neoptolemus (tạo bởi nguoi-que/tools/cat-sprite.py)\n'
js += 'window.NEO_SPRITES = ' + json.dumps(sprites) + ';\n'
js += 'window.NEO_RIG = ' + json.dumps(rig) + ';\n'
open(sys.argv[2] if len(sys.argv) > 2 else 'sprites.js', 'w', encoding='utf-8').write(js)
print('sprites.js', len(js) // 1024, 'KB')
