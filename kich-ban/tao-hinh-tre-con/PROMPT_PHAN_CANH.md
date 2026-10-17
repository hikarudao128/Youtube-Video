# PROMPT TẠO ẢNH TỪNG PHÂN CẢNH: TRẺ CON KHÔNG ĐƯỢC ĂN THỊT CHÓ

> Dùng cùng kịch bản [`../TRE_CON_KHONG_DUOC_AN_THIT_CHO_EN.md`](../TRE_CON_KHONG_DUOC_AN_THIT_CHO_EN.md) và 9 bảng nhân vật trong thư mục này.
> Prompt từng cảnh nằm trong `phan-canh-prompt/chuong_<N>.md` (mỗi chương một file). Prompt viết bằng tiếng Anh vì các mô hình tạo ảnh hiểu tiếng Anh tốt hơn.

## Cách dùng

1. **Luôn đính kèm bảng nhân vật** ghi ở dòng *Tham chiếu* của mỗi cảnh. Script làm việc này tự động.
2. **KHỐI PHONG CÁCH CHUNG** bên dưới được dán trước prompt của từng cảnh.
3. **Không cho AI vẽ chữ.** Chữ trên màn hình (tiêu đề, con số, nhãn bản đồ) thêm sau trong phần mềm dựng.
4. **Tạo ảnh bằng Codex CLI:**
   ```bash
   cd kich-ban/tao-hinh-tre-con
   python3 tao_phan_canh.py 0.1 0.2          # vài cảnh
   python3 tao_phan_canh.py --chuong 2       # cả chương 2
   python3 tao_phan_canh.py --tat-ca -j 4    # tất cả
   python3 ghep_storyboard.py                # ghép trang storyboard 2x2
   ```
   Ảnh lưu ở `phan-canh/canh_<x>_<y>.png`, trang storyboard ở `storyboard/storyboard_XX.jpg`.

### Định dạng một cảnh (trong `phan-canh-prompt/chuong_<N>.md`)

````
#### CẢNH 2.3 · 2:24–2:30
Lời dẫn: And there it is. Right here, by the fence. The family dog. Asleep in the sun.
Tham chiếu: 08
```text
<prompt tiếng Anh mô tả riêng cảnh này>
```
````

### Mã bảng nhân vật

| Mã | File | Nhân vật |
|---|---|---|
| 01 | `01_nguoi_bo.png` | Người bố (hắn) |
| 02 | `02_nguoi_me.png` | Người mẹ (thị) |
| 03 | `03_cai_gai.png` | Cái Gái, chị cả |
| 04 | `04_cu_nhon.png` | Cu Nhớn |
| 05 | `05_cu_nho.png` | Cu Nhỡ |
| 06 | `06_cu_con.png` | Cu Con, út |
| 07 | `07_mu_vu.png` | Mụ Vụ |
| 08 | `08_con_cho.png` | Con chó vàng |
| 09 | `09_ba_ong_khach.png` | Ba ông khách |

Nhân vật phụ (người hàng xóm mua chuối lần hai, chủ quán…) được mô tả ngay trong prompt, vẽ cùng phong cách.

### KHỐI PHONG CÁCH CHUNG (dán trước mọi prompt)

```text
Create ONE 16:9 widescreen illustration for an animated YouTube story video.
STYLE: exactly the same simple flat 2D cartoon style as the attached character sheets: big round heads, solid black oval eyes, round pink-orange bulb noses, simple eyebrows, thin black stick arms and legs, white oval hands, thick black outlines, flat colors with minimal shading, no gradients, no realism. Backgrounds drawn in the same flat, clean, slightly simplified style with thick outlines. Muted earthy palette.
CHARACTERS: any character shown on an attached sheet must look identical to that sheet (same face, hair, body proportions, clothes, colors, props). Children stay clearly smaller than adults. Props shown on the sheets (the mother's basket, cái Gái's tray, cu Con's bowl, the father's liquor bottle, mụ Vụ's purse) appear only when the scene text asks for them. Do not show the four-view layout; draw a single scene.
SETTING: a poor village in rural northern Vietnam, early 1940s: one small thatched hut with mud walls, a dirt yard, a low bamboo fence, banana plants, a dark smoky kitchen corner with a clay stove and straw on the floor, bamboo bed and a low bamboo table in the main room.
RULES: no text, no letters, no numbers, no captions, no watermark anywhere in the image. The killing of the dog is NEVER shown: no blood, no knife on the dog, no dead or cooked dog body; only imply it (empty spot, a rope, faces, steam from a covered pot). Food on the table is shown as covered clay pots, bowls and steam, never an identifiable animal. Keep composition cinematic with clear foreground, subject and background layers.
SCENE:
```
