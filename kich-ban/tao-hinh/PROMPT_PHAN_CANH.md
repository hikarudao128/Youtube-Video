# PROMPT TẠO ẢNH TỪNG PHÂN CẢNH: CHÍ PHÈO

> Dùng cùng [`../CHI_PHEO_PHAN_CANH.md`](../CHI_PHEO_PHAN_CANH.md) (94 cảnh) và 7 bảng nhân vật trong thư mục này.
> Prompt viết bằng tiếng Anh vì các mô hình tạo ảnh hiểu tiếng Anh tốt hơn.

## Cách dùng

1. **Luôn đính kèm bảng nhân vật** ghi ở dòng *Tham chiếu* của mỗi cảnh, để nhân vật giống hệt bảng tạo hình.
2. **Dán KHỐI PHONG CÁCH CHUNG lên trước** prompt của từng cảnh. Script `tao_phan_canh.py` tự làm việc này.
3. **Không cho AI vẽ chữ.** Chữ trên màn hình (tiêu đề, con số, nhãn bản đồ) nên thêm sau trong phần mềm dựng (CapCut, Premiere…). AI hay viết sai tiếng Việt có dấu.
4. **Tạo ảnh hàng loạt bằng Codex CLI:**
   ```bash
   cd kich-ban/tao-hinh
   python3 tao_phan_canh.py 0.1 0.2 0.3      # tạo vài cảnh
   python3 tao_phan_canh.py --chuong 2       # tạo cả chương 2
   python3 tao_phan_canh.py --tat-ca -j 6    # tạo cả 94 cảnh, chạy 6 cảnh song song
   ```
   Ảnh được lưu vào `phan-canh/canh_<số>.png`. Cảnh nào đã có ảnh sẽ được bỏ qua (thêm `--ghi-de` để tạo lại).

### Mã bảng nhân vật

| Mã | File | Nhân vật |
|---|---|---|
| 01 | `01_chi_pheo_tre.png` | Chí Phèo lúc trẻ |
| 02 | `02_chi_pheo_ra_tu.png` | Chí Phèo sau khi ra tù |
| 03 | `03_ba_kien.png` | Bá Kiến |
| 04 | `04_ba_ba.png` | Bà Ba |
| 05 | `05_ly_cuong.png` | Lý Cường |
| 06 | `06_thi_no.png` | Thị Nở |
| 07 | `07_ba_co_thi_no.png` | Bà cô Thị Nở |

Nhân vật phụ (dân làng, lính lệ, anh thả ống lươn…) được mô tả ngay trong prompt, vẽ cùng phong cách.

### KHỐI PHONG CÁCH CHUNG (dán trước mọi prompt)

```text
Create ONE 16:9 widescreen illustration for an animated YouTube story video.
STYLE: exactly the same simple flat 2D cartoon style as the attached character sheets: big round heads, solid black oval eyes, simple eyebrows, thin black stick arms and legs, white oval hands, thick black outlines, flat colors with minimal shading, no gradients, no realism. Backgrounds drawn in the same flat, clean, slightly simplified style with thick outlines. Muted earthy palette.
CHARACTERS: any character shown on an attached sheet must look identical to that sheet (same face, hair, clothes, colors, props). Do not show the four-view layout; draw a single scene.
SETTING: rural northern Vietnam in the 1930s: bamboo hedges, thatched huts with mud walls, red dirt roads, rice paddies, a river, brick-and-tile houses for the rich.
RULES: no text, no letters, no captions, no watermark anywhere in the image. Violence is only implied (shadows, objects, cut-away), never graphic; no blood beyond a tiny dark-red mark. Keep composition cinematic with clear foreground, subject and background layers.
SCENE:
```

---

## CHƯƠNG 0 — MỞ ĐẦU

#### CẢNH 0.1 · 0:00–0:05
Tham chiếu: không
```text
Dim interior of a Vietnamese village house at sunset. A worn brick floor lit by one slanted beam of red-orange light through a doorway, dust floating in the beam. On the floor, two motionless cartoon silhouettes lying apart, shown only as dark shapes, faces not visible. Almost everything else is in deep shadow. Mysterious, quiet, ominous.
```

#### CẢNH 0.2 · 0:05–0:13
Tham chiếu: 03, 02
```text
Split composition divided by a vertical black ink stroke. LEFT half (warm gold tones): close-up of Bá Kiến's plump white oval hand with a gold ring hanging limply over the edge of a dark wooden daybed, his black pleated turban fallen on the floor. RIGHT half (cold grey tones): close-up of Chí Phèo's white oval hand lying open on a brick floor next to his small brown liquor bottle with a broken neck. No faces shown. Both halves in heavy shadow.
```

#### CẢNH 0.3 · 0:13–0:19
Tham chiếu: 06
```text
Extreme close-up still life: Thị Nở's small brown clay pot of rice porridge with green scallion dots, sitting on a bamboo slat bed, three soft curling lines of steam rising. Pure black background, a single warm spotlight on the pot. Cozy but lonely.
```

#### CẢNH 0.4 · 0:19–0:22
Tham chiếu: 06
```text
Same clay pot of scallion porridge as before, small and centered low in the frame, softly darker, with lots of empty black space above it for text to be added later in editing.
```

#### CẢNH 0.5 · 0:22–0:27
Tham chiếu: không
```text
An abandoned dome-shaped brick kiln standing alone in an empty field, cracked red bricks, weeds growing on top, a dark arched opening. Inside the opening, a tiny white cloth bundle (a baby) barely visible. Grey sky, a few bare trees, one crow on a branch. Lonely, sepia-tinted flat colors.
```

#### CẢNH 0.6 · 0:27–0:33
Tham chiếu: 02
```text
Close-up of Chí Phèo's white oval hand gripping a jagged shard of broken brown glass. Behind it, out of focus, half of his bald head and angry eyebrow. A single tiny dark-red drop falls toward the dirt ground. Cold grey-blue palette, tense mood, no wound shown.
```

#### CẢNH 0.7 · 0:33–0:39
Tham chiếu: 06
```text
Thị Nở seen from the chest down (face cropped out of frame), holding her steaming clay pot of scallion porridge with both hands as she steps through a bamboo lattice door. Warm golden morning light behind her, glowing rim of light around her patched brown blouse. Tender, hopeful mood.
```

#### CẢNH 0.8 · 0:39–0:44
Tham chiếu: 02
```text
High wide shot of a long straight red dirt village road between two bamboo hedges. In the middle, tiny Chí Phèo stands swaying, raising his liquor bottle to the sky, mouth open shouting. On both sides, villagers' bamboo gates are swinging shut. Harsh white midday sun, long shadow behind him. Lonely and isolated.
```

#### CẢNH 0.9 · 0:44–0:50
Tham chiếu: không
```text
Plain textured cream rice-paper background with subtle paper grain and a faint red brush stroke along the bottom edge. Completely empty in the center so the title can be added in editing. Calm, minimal.
```

---

## CHƯƠNG 1 — ĐỨA TRẺ TRONG LÒ GẠCH

#### CẢNH 1.1 · 0:50–0:55
Tham chiếu: không
```text
Top-down hand-drawn style map of a small northern Vietnamese village in the same flat cartoon style: a winding river along the bottom with a riverside banana garden and a tiny thatched hut; a large brick-and-tile mansion with a gated courtyard in the center; small thatched houses; bamboo groves; green rice paddies; a red dirt road from a village gate with a banyan tree to the mansion; an old brick kiln alone at the far left edge. Cream paper background, brown outlines. No labels, no text.
```

#### CẢNH 1.2 · 0:55–1:01
Tham chiếu: 02
```text
Medium-wide side view of Chí Phèo staggering along a red dirt village road from left to right, open shirt showing his chest tattoos, holding his liquor bottle, mouth wide open shouting, angry eyebrows. Bamboo hedge in the foreground partly framing him. Daylight but desaturated, greyish colors.
```

#### CẢNH 1.3 · 1:01–1:06
Tham chiếu: 02
```text
Low-angle shot looking up at Chí Phèo standing in the middle of the road, shaking his fist at a pale white sky, head thrown back, shouting. Tall bamboo tips sway behind him. Defiant and lonely.
```

#### CẢNH 1.4 · 1:06–1:13
Tham chiếu: không
```text
Three-panel horizontal strip in one image, separated by thin black lines: (1) an old village woman in a brown blouse and black headscarf sweeping her yard, turning her back to the road; (2) two village men squatting under a banyan tree smoking a long bamboo water pipe, one smirking, one shaking his head, both ignoring the road; (3) a bamboo gate closing, a small child's curious eye peeking through the gap. Flat cartoon villagers in the same style.
```

#### CẢNH 1.5 · 1:13–1:15
Tham chiếu: 02
```text
Extreme close-up of Chí Phèo's face filling the frame: two black oval eyes under sharply angry eyebrows, red-rimmed, the glass-shard scar on his left cheek partly visible. Intense stare at the viewer.
```

#### CẢNH 1.6 · 1:15–1:23
Tham chiếu: không
```text
Sepia-toned flashback with slightly burnt paper edges. Misty dawn beside the abandoned brick kiln. A poor young peasant in a worn conical hat, carrying a bundle of bamboo eel traps on his shoulder, has stopped and bends down toward the dark kiln opening, where a tiny pale baby wrapped in old straw lies. He reaches out hesitantly. Same flat cartoon style, quiet and melancholic.
```

#### CẢNH 1.7 · 1:23–1:29
Tham chiếu: không
```text
The same top-down village map style as before, zoomed toward the left edge, with a bold red brush-stroke circle drawn around the old brick kiln. Empty fields around the kiln, far from houses. No text.
```

#### CẢNH 1.8 · 1:29–1:36
Tham chiếu: 01
```text
Three-panel strip in loose sketchy ink lines with very little color, like old photos: (1) a blind old widow sitting on a doorstep, feeling with her hands while holding a baby; (2) an old carpenter carving a wooden rice mortar while a 5-year-old boy (a tiny version of young Chí Phèo with short black hair) collects wood chips beside him; (3) a skinny 10-year-old boy (same child, older) carrying two heavy water buckets on a shoulder pole past village gates.
```

#### CẢNH 1.9 · 1:36–1:42
Tham chiếu: 01
```text
Wide shot of a bright green rice paddy. Young Chí Phèo, his light-brown áo cánh damp with sweat, trousers rolled to the knees, barefoot in the mud, guides a grey water buffalo pulling a wooden plow. In the far background, the red tiled roof of a large mansion rises above bamboo groves. Warm sepia and green tones, peaceful.
```

#### CẢNH 1.10 · 1:42–1:46
Tham chiếu: 01
```text
Close-up of young Chí Phèo wiping sweat from his forehead with the back of his white oval hand, a small shy smile, kind eyebrows. He glances up toward the distant mansion. Warm soft light.
```

#### CẢNH 1.11 · 1:46–1:52
Tham chiếu: 04, 01
```text
Dim interior of a rich Vietnamese house seen from an inner-room doorway. Bà Ba reclines on a dark wooden daybed against folded pillows, half-lifted curtain, lazily beckoning with her red fan. Young Chí Phèo stands stiffly at the doorway with muddy bare feet, holding the hem of his shirt, eyes looking down at the floor. Light through window bars falls in stripes; Bà Ba in warm light, Chí in shadow. Fully clothed, nothing intimate.
```

#### CẢNH 1.12 · 1:52–1:59
Tham chiếu: 03, 05
```text
Interior of the mansion's main hall: Bá Kiến sits cross-legged on a dark wooden daybed calmly pouring tea from a small teapot into a tiny cup, sly closed-eye smile. His son Lý Cường stands beside him holding his rattan cane, sneering. Behind them, red lacquered wooden boards and an altar cabinet. Calm but menacing mood.
```

#### CẢNH 1.13 · 1:59–2:10
Tham chiếu: 01
```text
Wide shot on top of a high grassy river dike under a grey overcast sky. Young Chí Phèo, hands tied behind his back with rope, is led away by two colonial-era village militiamen in flat conical hats and dark tunics holding wooden batons. Chí looks back over his shoulder toward the village. Below the dike, a small group of villagers watch silently. Cold grey-blue palette, desolate.
```

---

## CHƯƠNG 2 — KẺ TRỞ VỀ TỪ NHÀ TÙ

#### CẢNH 2.1 · 2:10–2:15
Tham chiếu: 02
```text
Wide shot of an old brick village gate beside a huge banyan tree at dusk. Chí Phèo walks toward the camera, backlit by a pale orange sky, his figure mostly a dark silhouette with a bald round head, a long shadow stretching toward the viewer. Grey-blue palette, ominous.
```

#### CẢNH 2.2 · 2:15–2:18
Tham chiếu: không
```text
Three villagers carrying bundles of straw on bamboo shoulder poles have stopped on the road, squinting at someone off-screen to the left, one whispering to another, the third shaking his head. Flat cartoon villagers, curious and uneasy.
```

#### CẢNH 2.3 · 2:18–2:30
Tham chiếu: 02
```text
Full-body front view of Chí Phèo standing on the village road at dusk, composed tall so the camera can pan from his bare feet up to his bald head: bare tan feet, ragged black trousers, rope belt, open brown shirt showing dragon and phoenix tattoos, wide white-toothed grin, glaring angry eyes, shiny bald head. Intimidating hero-shot framing, grey-blue tones.
```

#### CẢNH 2.4 · 2:30–2:38
Tham chiếu: 01, 02
```text
Two portrait close-ups side by side on cream paper, connected by a horizontal brush stroke: LEFT, young Chí Phèo with short black hair, kind eyebrows and a shy smile, in warm sepia; RIGHT, Chí Phèo after prison, bald, scarred, angry grin, in cold grey-blue. Empty space between them for a number to be added later.
```

#### CẢNH 2.5 · 2:38–2:45
Tham chiếu: 02
```text
Inside a dim thatched village liquor shop: Chí Phèo squats on a low wooden platform, head tilted back, drinking straight from his brown ceramic liquor bottle. Behind a large clay jar, a frightened middle-aged shop woman in a brown blouse and headscarf peeks out nervously. Chipped cups on the platform.
```

#### CẢNH 2.6 · 2:45–2:50
Tham chiếu: không
```text
Top-down hand-drawn style village map in flat cartoon style (river at bottom, mansion in center, bamboo, rice paddies, brick kiln at left edge), with a bold wobbly red brush arrow drawn from a small shop near the village gate straight along the road to the gate of the large central mansion. No text.
```

#### CẢNH 2.7 · 2:50–2:56
Tham chiếu: 02
```text
View from inside the mansion's brick courtyard toward its tiled-roof brick gate with heavy wooden doors. Chí Phèo stands between the open doors, legs apart, waving his liquor bottle and shouting. In the courtyard, two servants with brooms freeze in surprise. A dog barks at him.
```

#### CẢNH 2.8 · 2:56–3:00
Tham chiếu: 05
```text
Lý Cường steps out onto the veranda of the mansion, sleeves rolled up, pointing his rattan cane toward the gate with a sneer. Behind him, two servants holding wooden sticks.
```

#### CẢNH 2.9 · 3:00–3:06
Tham chiếu: 02
```text
On the brick gate wall, only the black shadow of Chí Phèo is visible: his bald round head and stick arm raising a jagged broken bottle shard toward his own face. Glass fragments sparkle in the air in front of the wall. Dramatic, implied action only, no wound shown.
```

#### CẢNH 2.10 · 3:06–3:12
Tham chiếu: 02
```text
High-angle shot: Chí Phèo rolls on the dirt in front of the mansion gate, both white oval hands covering his face, a tiny dark-red mark between his fingers, mouth open yelling. Villagers gather in a wide semicircle a few steps away, keeping their distance.
```

#### CẢNH 2.11 · 3:12–3:16
Tham chiếu: không
```text
Medium shot of a group of villagers: two women link arms and one pulls the other away; an old man with his hands behind his back shakes his head and walks off. Flat cartoon villagers in brown clothes and conical hats.
```

#### CẢNH 2.12 · 3:16–3:28
Tham chiếu: 03, 02
```text
Bá Kiến, smiling sweetly with closed crescent eyes, bends down slightly toward Chí Phèo, holding his folded paper fan and raising one hand in a calming gesture. Chí sits on the ground at the gate looking up, angry face turning confused. Bá Kiến stands in warm sunlight; Chí sits in the gate's shadow. Ironic contrast.
```

#### CẢNH 2.13 · 3:28–3:34
Tham chiếu: 03, 02
```text
Extreme close-up: Bá Kiến's white oval hand with a gold ring placing a single silver Indochina coin into Chí Phèo's open white oval hand, which has a small dark smudge. Chí's fingers are starting to close around the coin. Spotlit against a dark background, symbolic.
```

#### CẢNH 2.14 · 3:34–3:52
Tham chiếu: 03
```text
Bá Kiến seen from behind and slightly to the side, walking back into his mansion's dark doorway, his smile gone, face cold and calculating in profile. Above the doorway, a faint ghostly drawing of a knife with a hand gripping its handle. Moody contrast between bright courtyard and dark interior.
```

#### CẢNH 2.15 · 3:52–4:00
Tham chiếu: 02
```text
Extreme close-up of Chí Phèo's left cheek and black oval eye in late afternoon light, showing the fresh diagonal glass-shard scar clearly. Quiet, heavy mood.
```

---

## CHƯƠNG 3 — CON QUỶ CỦA LÀNG VŨ ĐẠI

#### CẢNH 3.1 · 4:00–4:08
Tham chiếu: không
```text
Top-down hand-drawn style village map in flat cartoon style (river at bottom, mansion in center, bamboo, rice paddies), with a dark blue-black stain spreading outward from the central mansion through the lanes like spilled ink, swallowing the green fields. A tiny dark figure follows the edge of the stain. No text.
```

#### CẢNH 3.2 · 4:08–4:18
Tham chiếu: 03, 02
```text
Night interior of the mansion lit by one hanging oil lamp: Bá Kiến sits cross-legged on his daybed smoking a long bamboo water pipe, smoke curling up. Behind him, half in shadow beside a wooden pillar, Chí Phèo stands with arms crossed, only his tattoos and scar catching the lamplight. Chí's shadow on the wall is three times larger than him. Dark teal and amber palette.
```

#### CẢNH 3.3 · 4:18–4:34
Tham chiếu: 03, 02
```text
Two-shot by the oil lamp: Bá Kiến looks up with a thin knowing smile, tapping ash from his water pipe; Chí Phèo stands opposite him with arms crossed, smirking. Conspiratorial mood, dark teal and warm amber.
```

#### CẢNH 3.4 · 4:34–4:40
Tham chiếu: 03, 05
```text
Bá Kiến turns pages of a thick debt ledger under the oil lamp without looking up. Lý Cường stands in the doorway, looking out at a departing shadow in the dark yard, frowning. Faint chain links drawn subtly in the shadows on the floor.
```

#### CẢNH 3.5 · 4:40–4:50
Tham chiếu: không
```text
A riverside plot of land with wild grass, a few clumps of banana trees and a newly built small thatched hut with mud walls, the river beyond. Overcast sky. Empty of people.
```

#### CẢNH 3.6 · 4:50–4:56
Tham chiếu: không
```text
Top-down hand-drawn style village map in flat cartoon style. A drawn iron chain stretches from a small riverside garden plot with a hut all the way to the large central mansion, pulled tight. No text.
```

#### CẢNH 3.7 · 4:56–5:08
Tham chiếu: 02
```text
Four-panel grid, almost monochrome dark teal: (1) a bamboo door kicked open, Chí Phèo silhouetted in the doorway; (2) a smashed clay rice jar with white rice spilled across a dirt floor; (3) an old village woman crying in front of a hut with its roof torn off; (4) a small boy hiding behind his mother's skirt, wide frightened eyes. The only bright color is the white rice.
```

#### CẢNH 3.8 · 5:08–5:16
Tham chiếu: 02
```text
Hazy dreamlike double exposure, tilted frame: Chí Phèo eating and drinking at the same time; Chí asleep slumped at the roadside clutching his bottle; and a dark silhouette of him swinging a knife at night, all layered translucently over each other. Drunk, blurry, disorienting mood.
```

#### CẢNH 3.9 · 5:16–5:22
Tham chiếu: 02
```text
Chí Phèo sits alone slumped against a banana tree trunk on the riverbank at dusk, dull half-closed eyes staring at the water, bottle beside him. No one else around. Lonely, empty space at the top of the frame for a title.
```

#### CẢNH 3.10 · 5:22–5:30
Tham chiếu: 03
```text
Wide panoramic image split by a brick wall in the middle: on the LEFT, a group of villagers whisper and glance toward a distant hut; on the RIGHT, behind the wall, Bá Kiến sits under an oil lamp counting neat stacks of silver coins, smiling with closed crescent eyes.
```

---

## CHƯƠNG 4 — ĐÊM TRĂNG BỜ SÔNG

#### CẢNH 4.1 · 5:30–5:36
Tham chiếu: không
```text
A big full moon in a deep blue night sky above a quiet river, silver moonlight shimmering on the water, a dark silhouette of a banana grove on the near bank. Serene, beautiful, calm.
```

#### CẢNH 4.2 · 5:36–5:41
Tham chiếu: 06
```text
Silhouette of Thị Nở walking along a dirt path toward the river at night, carrying two water buckets on a bamboo shoulder pole, the pole bending with her steps, the moonlit sky behind her. Her headscarf and bun recognizable in silhouette.
```

#### CẢNH 4.3 · 5:41–5:52
Tham chiếu: 06
```text
Two-part image. LEFT (night, blue moonlight): gentle portrait of Thị Nở, plain but kind, worried eyebrows, innocent eyes. RIGHT (daytime, warmer): a village lane where small children run away from Thị Nở laughing and a mother pulls her child inside a gate, while Thị Nở stands confused. Sympathetic, not mocking.
```

#### CẢNH 4.4 · 5:52–6:00
Tham chiếu: 02, 06
```text
Split screen merging toward the center: LEFT, Chí Phèo sitting alone on a straw mat in his dark hut with his bottle; RIGHT, Thị Nở sitting alone on the doorstep of her thatched house, chin on her knees. A single row of big banana leaves separates the two halves. Blue moonlight on both.
```

#### CẢNH 4.5 · 6:00–6:10
Tham chiếu: 06
```text
Moonlit riverside next to a banana garden: Thị Nở has set down her two full water buckets and sits leaning against a banana tree trunk, fanning herself with her hand, the breeze moving the banana leaves. River shimmering behind her.
```

#### CẢNH 4.6 · 6:10–6:18
Tham chiếu: 06
```text
Close-up of Thị Nở asleep, fully clothed, head tilted against the banana trunk, mouth slightly open, a peaceful childlike face, dappled moonlight spots through the banana leaves on her face. Tender, gentle.
```

#### CẢNH 4.7 · 6:18–6:26
Tham chiếu: 02, 06
```text
Over-the-shoulder shot from behind Chí Phèo as he stumbles out of his thatched hut into the banana garden holding his bottle, then stops. Ahead of him, in a patch of moonlight, Thị Nở sleeps under the banana tree, small in the distance. Quiet, still moment. Nothing intimate shown.
```

#### CẢNH 4.8 · 6:26–6:40
Tham chiếu: không
```text
Banana leaves swaying in the foreground, the river beyond, and the full moon in the sky being covered by a drifting cloud. The sky toward the horizon begins to turn pale toward dawn. No people in the frame.
```

---

## CHƯƠNG 5 — NỒI CHÁO HÀNH

#### CẢNH 5.1 · 6:40–6:47
Tham chiếu: 02
```text
Inside Chí Phèo's poor thatched hut at dawn: golden light rays shine through cracks in the mud walls and straw roof, dust floating in the beams. A straw bed, a bamboo slat bed, empty liquor bottles on the floor. Chí lies curled up on the straw. Warm and quiet for the first time.
```

#### CẢNH 5.2 · 6:47–6:55
Tham chiếu: 02
```text
Close-up of Chí Phèo lying down, sweaty bald head, slowly opening his eyes. His eyes look clear and tired, not angry; eyebrows relaxed and soft. Gentle morning light on his face. Vulnerable.
```

#### CẢNH 5.3 · 6:55–6:59
Tham chiếu: không
```text
Two little sparrows hopping playfully on a bamboo branch in bright morning sunlight, simple flat cartoon birds, clear sky behind.
```

#### CẢNH 5.4 · 6:59–7:03
Tham chiếu: không
```text
A line of cheerful village women in brown blouses and conical hats walking to market along a dike, carrying baskets of vegetables and chickens on bamboo shoulder poles, one woman laughing loudly. Morning light.
```

#### CẢNH 5.5 · 7:03–7:07
Tham chiếu: không
```text
A small wooden fishing boat on a misty morning river; a fisherman in a conical hat knocks his oar against the side of the boat to drive fish into his net. Ripples on the water.
```

#### CẢNH 5.6 · 7:07–7:13
Tham chiếu: 02
```text
Extreme close-up of Chí Phèo's eyes, filling the frame, calm and clear, eyebrows soft, listening. Peaceful expression. Warm morning tones.
```

#### CẢNH 5.7 · 7:13–7:28
Tham chiếu: 01
```text
Dreamy hazy image with soft honey-gold tones and blurred edges like a memory: a tidy small thatched cottage with a hibiscus hedge; young Chí Phèo (no scar, short black hair) carrying a hoe toward a field; a wife (back turned, face not shown) weaving at a wooden loom on the porch; a pig in a little bamboo pen; golden rice fields in the distance. Peaceful, longing.
```

#### CẢNH 5.8 · 7:28–7:36
Tham chiếu: 02
```text
Chí Phèo sits up on his straw bed in the empty hut, looking down at his own white oval hands resting in his lap. Morning light, lots of empty space around him. Lonely, reflective.
```

#### CẢNH 5.9 · 7:36–7:42
Tham chiếu: 06
```text
View from inside the hut toward the bamboo door, which is opening. Bright morning sunlight floods in and outlines Thị Nở with a glowing rim of light as she steps in holding her steaming clay pot of scallion porridge with both hands. Warm, hopeful.
```

#### CẢNH 5.10 · 7:42–7:58
Tham chiếu: 02, 06
```text
Inside the hut: Thị Nở kneels by the bamboo bed, holding out a bowl of scallion porridge to Chí Phèo with both hands, smiling shyly. Chí sits on the straw bed reaching out very slowly and hesitantly toward the bowl, eyebrows soft and surprised. The clay pot steams beside them. Warm morning light, tender and chaste.
```

#### CẢNH 5.11 · 7:58–8:10
Tham chiếu: 02
```text
Close-up of Chí Phèo holding the bowl of steaming porridge near his face with both white oval hands, steam partly veiling his scarred face, his eyes closed as he sips, a small shine of moisture at the corner of one eye. Warm golden light. Emotional.
```

#### CẢNH 5.12 · 8:10–8:22
Tham chiếu: 02
```text
From behind: Chí Phèo sits on the threshold of his hut holding the bowl, looking out at the village: thatched roofs with cooking smoke rising, distant market-goers on the dike, green fields. Golden hopeful morning. Empty sky area at the top for a quote to be added later.
```

#### CẢNH 5.13 · 8:22–8:40
Tham chiếu: 02, 06
```text
Five-panel horizontal strip, warm tones, each panel a different day: (1) Chí Phèo and Thị Nở eating porridge together, both laughing shyly; (2) Chí repairing the thatched roof while Thị Nở hands up straw; (3) Chí taking the water shoulder pole from Thị Nở to carry it for her; (4) the two sitting silently at the hut door watching the river at dusk; (5) a dusty liquor bottle lying untouched in a corner of the hut.
```

---

## CHƯƠNG 6 — BÀ CÔ

#### CẢNH 6.1 · 8:40–8:47
Tham chiếu: 06
```text
Harsh white midday sun in the banana garden: Thị Nở is hanging a shirt on a rope line when she suddenly freezes, one white oval hand over her mouth as if remembering something important. Washed-out bright colors, hot atmosphere.
```

#### CẢNH 6.2 · 8:47–8:53
Tham chiếu: 07
```text
A small thatched house with a packed-earth yard, a big clay water jar and a gourd trellis. Thị Nở's old aunt sits on a bamboo bed on the veranda, hunched, chewing betel with a red-stained mouth, fanning herself with her round woven bamboo fan, glaring suspiciously at someone entering the yard. Harsh noon light.
```

#### CẢNH 6.3 · 8:53–9:10
Tham chiếu: 07, 06
```text
In the aunt's yard: the old aunt, seen from a slightly low angle so she looks dominant, slams her round woven fan down on the bamboo bed and points angrily, mouth wide open scolding. Thị Nở stands small in the middle of the yard, seen from a slightly high angle, twisting the hem of her blouse, smiling awkwardly and nervously. Harsh noon light.
```

#### CẢNH 6.4 · 9:10–9:18
Tham chiếu: 02
```text
Wide shot: Chí Phèo sits waiting on the threshold of his hut, a freshly washed shirt drying on the fence beside him, looking toward the end of the lane. No bottle in his hands. Quiet, hopeful, harsh afternoon light.
```

#### CẢNH 6.5 · 9:18–9:28
Tham chiếu: 06, 02
```text
In the banana garden: Thị Nở stands with hands on her hips, scolding and pointing at Chí Phèo, copying her aunt's angry posture and expression. Chí stands bewildered, arms hanging limp, eyebrows raised in shock. Slightly tilted frame for a chaotic feeling.
```

#### CẢNH 6.6 · 9:28–9:36
Tham chiếu: 06, 02
```text
Action frozen mid-motion: Thị Nở turns to leave and pushes Chí Phèo away with both hands after he grabbed her wrist; Chí stumbles and falls forward toward the dirt, dust puffing up around him. Motion lines, dynamic composition, cartoonish, not violent.
```

#### CẢNH 6.7 · 9:36–9:50
Tham chiếu: 02
```text
High wide shot looking down: tiny Chí Phèo sits on the bare dirt in the middle of the banana garden next to the river, watching a small figure of Thị Nở disappear behind the banana trees. Lots of empty space around him. Desolate.
```

---

## CHƯƠNG 7 — CON DAO

#### CẢNH 7.1 · 9:50–9:58
Tham chiếu: 02
```text
Dim hut lit by red-orange late-afternoon light through cracks in the walls: Chí Phèo slumps against the mud wall drinking from his dusty liquor bottle, several empty bottles beside him. His eyes are clear and pained rather than angry. Heavy mood.
```

#### CẢNH 7.2 · 9:58–10:05
Tham chiếu: 02, 06
```text
Chí Phèo covers his face with both white oval hands, shoulders hunched, sobbing. In the foreground, slightly out of focus, Thị Nở's clay porridge pot sits cold, with wilted scallions and no steam. Red-orange light.
```

#### CẢNH 7.3 · 10:05–10:10
Tham chiếu: 02
```text
Close-up: Chí Phèo's white oval hand pulling a short farm knife out from under the straw bedding, the blade catching an orange glint of sunset light. Tense, no person harmed.
```

#### CẢNH 7.4 · 10:10–10:20
Tham chiếu: 02
```text
Side tracking shot of Chí Phèo walking fast and unsteadily along a red dirt village road at sunset, muttering, one hand reaching behind his back toward his rope belt. Long orange shadows, bamboo hedges blurred with motion.
```

#### CẢNH 7.5 · 10:20–10:27
Tham chiếu: 02
```text
Chí Phèo seen from behind, standing alone in front of the mansion's tiled-roof brick gate with heavy wooden doors, at blood-red sunset. His long shadow stretches through the open gate across the courtyard bricks. Ominous stillness.
```

#### CẢNH 7.6 · 10:27–10:45
Tham chiếu: 03, 02
```text
Inside the mansion hall: Bá Kiến sits on his dark wooden daybed holding his long water pipe, looking up with a contemptuous half-smile. In the doorway, Chí Phèo stands as a dark silhouette against the blood-red sunset, rim-lit like fire, only his bald head outline and fists visible. Strong contrast.
```

#### CẢNH 7.7 · 10:45–10:52
Tham chiếu: 02
```text
Extreme close-up of Chí Phèo's face filling the frame, red light: several glass-shard scars on his cheek, eyes wet with tears, eyebrows twisted in anguish, mouth open shouting, one white oval hand pressed against the scar on his cheek. Desperate, heartbreaking.
```

#### CẢNH 7.8 · 10:52–10:56
Tham chiếu: 02
```text
Dark silhouette of Chí Phèo's raised arm holding a short farm knife high, the blade glinting red, the whole image washing out toward bright white at the edges as if into a white flash. No other person in frame, no contact shown.
```

#### CẢNH 7.9 · 10:56–11:00
Tham chiếu: 03
```text
Close-up of a brick floor in red sunset light: a short farm knife lying on the bricks next to Bá Kiến's fallen black pleated turban. No people, no blood visible. Total stillness.
```

#### CẢNH 7.10 · 11:00–11:10
Tham chiếu: không
```text
The empty brick courtyard of the mansion at dusk: the gate wide open, a single dry leaf blowing across the bricks, the house door half-closed with darkness inside, a black crow perched on the gate roof. Silent, abandoned.
```

---

## CHƯƠNG 8 — KẾT

#### CẢNH 8.1 · 11:10–11:22
Tham chiếu: không
```text
Aerial view of the small northern Vietnamese village at twilight in purple-grey tones: cooking smoke drifting over thatched roofs and bamboo groves, the large tiled mansion in the center, the river curving below. Quiet and sad. Empty sky area for portraits to be overlaid later.
```

#### CẢNH 8.2 · 11:22–11:30
Tham chiếu: 06
```text
Thị Nở stands alone at a river landing at dusk, two water buckets at her feet, gazing out at the water, her long shadow on the earthen steps. Purple-grey evening light. Lonely.
```

#### CẢNH 8.3 · 11:30–11:36
Tham chiếu: không
```text
A group of villagers gathered at the end of a lane at dusk, chatting and nodding to each other, some smiling or smirking, nobody looks sad. Flat cartoon villagers in brown clothes, conical hats and headscarves.
```

#### CẢNH 8.4 · 11:36–11:48
Tham chiếu: không
```text
Simple symbolic illustration on cream paper: a light-colored stick figure walks through an open wooden gate and comes out the other side as a completely black figure; the black figure turns back toward the gate, but the gate is slammed shut, and behind it stand many silhouettes of villagers. Minimal flat style.
```

#### CẢNH 8.5 · 11:48–11:58
Tham chiếu: không
```text
Close-up of an old yellowed paperback book lying on a dark wooden table, the cover plain and blank (title to be added in editing), slightly worn corners, warm lamplight. Nostalgic, 1940s feel.
```

#### CẢNH 8.6 · 11:58–12:06
Tham chiếu: 06
```text
Close-up of Thị Nở frozen in shock, eyebrows raised, glancing down at her belly; one white oval hand resting gently on her stomach. Dusk light, quiet and ominous.
```

#### CẢNH 8.7 · 12:06–12:12
Tham chiếu: không
```text
The abandoned dome-shaped brick kiln at purple-grey dusk: cracked red bricks, weeds on top, the dark arched opening completely empty, waiting. Soft blurred dreamlike edges. Ominous stillness.
```

#### CẢNH 8.8 · 12:12–12:17
Tham chiếu: không
```text
Top-down hand-drawn style village map in flat cartoon style, the central mansion and the riverside hut faded and grey, and the old brick kiln at the left edge circled with two bold overlapping red brush-stroke circles. No text.
```

#### CẢNH 8.9 · 12:17–12:25
Tham chiếu: không
```text
Plain dark textured rice-paper background with a soft vignette, completely empty, to be used as the end screen with a subscribe button and video thumbnails added in editing.
```
