# PROMPT: Kể chuyện tiếng Anh theo phong cách kênh "Unknown Frequencies"

> Phân tích từ transcript (phụ đề tiếng Anh) của 5 video thuộc kênh **Unknown Frequencies** (@unknownfrequencies-tv):
> - The Entire Story of The Trojan War & Iliad Explained — `X3_q5A18qfc` (~13 phút, ~2.400 từ)
> - The ENTIRE History of CANADA Explained — `CG4rE6Aw9HM` (~16 phút, ~2.700 từ)
> - The ENTIRE History of The Vietnam War Explained — `79PHRzE9pDU` (~18 phút, ~3.000 từ)
> - The Reason Germany Failed at the Battle of the Bulge — `PXxir5GIqKU` (~12 phút, ~2.000 từ)
> - The ENTIRE History of WW2 Explained — `Nlu6Fe-vbYQ` (~14 phút, ~2.200 từ)
>
> **Cách dùng:** Phần 1 giải thích phong cách (tiếng Việt, để bạn hiểu). Phần 2–4 viết hoàn toàn bằng **tiếng Anh**. Hãy copy nguyên khối prompt vào ChatGPT, Claude hoặc Gemini; kịch bản trả về sẽ bằng tiếng Anh. Truyện gốc bạn dán vào có thể là tiếng Việt hoặc tiếng Anh, AI sẽ tự chuyển thể.
>
> Nhịp đọc của kênh: khoảng **165–185 từ/phút**, nên prompt lấy mốc **~170 từ tiếng Anh / phút video**.

---

## PHẦN 1 — PHÂN TÍCH PHONG CÁCH (rút ra từ transcript thật)

| # | Kỹ thuật | Cách kênh làm |
|---|---|---|
| 1 | **Mở đầu 5 bước** (giống nhau ở cả 5 video) | Quy mô "khủng" → *"But the whole thing started because…"* (một nguyên nhân nhỏ, vô lý) → câu xác nhận đời thường *"Yeah, seriously."* → 3–4 teaser nghịch lý → câu hỏi trung tâm *"So, how did [nhỏ] lead to [lớn]?"* → *"Let's start with…"* |
| 2 | **Chuyển mốc thời gian** | Cụm cố định *"Now, it's [year]…"*, 5–8 lần mỗi video, đóng vai trò tên chương |
| 3 | **Câu hỏi mở chương** | *"So, why did…?"*, *"So, what stopped them?"*, rồi trả lời ngay |
| 4 | **Neo vào bản đồ** | *"right here"*, *"up here"*, *"down here"*, *"over here"*: lời dẫn đồng bộ với hình |
| 5 | **Tiểu phẩm hội thoại** | Cứ 1–2 phút có 4–10 lượt thoại, giọng hiện đại, nhân vật nói thẳng điều lẽ ra phải giấu. Sau đó người kể **lặp lại lời hứa của nhân vật rồi phủ định nó**. Ở cảnh bi kịch thì chuyển sang nghiêm túc |
| 6 | **Giọng kể** | Câu rất ngắn (*"Troy burned."*), bình luận tỉnh bơ (*"Spoiler, …"*, *"That was deliberate."*), từ đời thường (*basically, yeah, a guy who…*), lặp cấu trúc để tạo nhịp, câu chốt dùng phép đối/nghịch lý |
| 7 | **Báo trước & gọi lại** | Nói thẳng *"Remember that. It matters later."* rồi gọi lại đúng lúc; mọi teaser ở phần mở đều được "trả" |
| 8 | **Con số** | Cụ thể, rồi dịch ngay sang so sánh đời thường ("6 tiếng, chưa bằng một ca làm"; "nhỏ hơn California") |
| 9 | **Khoảnh khắc con người** | Dừng lại kể về một người cụ thể với một chi tiết nhỏ; bình luận bằng một câu ngắn, nặng |
| 10 | **Trung thực** | Thừa nhận nguồn mâu thuẫn, phá huyền thoại phổ biến |
| 11 | **Kết 4 nhịp** | Tổng kết cái giá → ý nghĩa lớn hơn → gọi lại nguyên nhân nhỏ ở câu đầu → câu chốt cực ngắn + CTA |

---

## PHẦN 2 — MAIN PROMPT (copy toàn bộ khối dưới đây)

```
You are a scriptwriter and narrator for a faceless, long-form YouTube storytelling channel. Your job: adapt the short story I provide into a complete ENGLISH video script with voice-over narration, written in the exact style described below. Write everything fresh and original. Do not copy wording from any existing channel or video.

## INPUTS
- Source story: [PASTE STORY HERE — may be in any language; adapt it into natural English]
- Target length: [e.g. 12 minutes] → narration ≈ 170 words × minutes (fast, punchy delivery)
- Faithfulness: [Keep the plot exactly / Allowed to add plausible context, scenes and dialogue]
- Main visuals: [Illustrated maps / Character illustrations / AI images / 2D animation]
- Audience: [e.g. US/UK viewers aged 18–40 who like history, myths and dark stories]
- Sponsor: [None / Name + talking points]

## LANGUAGE RULES
- Natural, spoken American English. Write for the ear, not the page.
- Contractions everywhere (it's, didn't, they'd). No academic or "AI-sounding" words (delve, tapestry, testament, realm, intricate, unravel).
- If the source story has culture-specific names, places or customs, keep the original names and explain each one in a single plain-English clause the first time it appears.
- Numbers: specific, written as digits in the script (they will be spelled out in the TTS version).

## 1. COLD OPEN — EXACTLY 5 BEATS (30–60 seconds)
1. One sentence about the SCALE of the story's final consequence (the biggest loss, the biggest mystery, the highest price), without revealing who wins or who survives.
2. The twist: "But the whole thing started because [the smallest, most absurd-sounding cause in the story]."
3. A tiny, casual confirmation line. Vary it: "Yeah, seriously." / "Yes, really." / "One [X]. That's it."
4. 3–4 teaser lines, each ONE sentence, each a paradox or shocking moment that WILL appear later. Tease, don't explain.
5. The central question: "So, how did [small cause] lead to [huge consequence]?", then "Let's start with [starting point]."
(If there is a sponsor: insert the read right after beat 5, then return with "All right, back to the story.")

## 2. BODY
- Strictly CHRONOLOGICAL. Every time jump uses a fixed transition: "Now, it's [time]…" or "[X] years later…". Use it 5–8 times per video.
- Open each chapter with ONE question ("So, why did…?", "So, what stopped them?", "So, how do you [solve problem] when [obstacle]?") and answer it immediately.
- Chain every event with CAUSE → EFFECT ("so", "but", "and that's when"). Never list events in isolation.
- VISUAL ANCHORS: every new place or character gets a pointing phrase: "right here", "up here", "down here", "over here", "look at this map". The narration must match what's on screen.
- Every number is followed by an everyday comparison: "Eight. Out of 32.", "That's not even a full work day.", "For less than the price of a decent warship."

## 3. DIALOGUE SKITS (signature device, MANDATORY)
- Every 60–120 seconds, insert a short reenacted dialogue: 4–10 lines, one short sentence per line.
- Characters talk in a MODERN, casual voice and say out loud what they'd normally hide (greed, pride, bad math, wishful thinking).
- End each skit with a punchline that is either funny or painful.
- Right after a comedic skit, the narrator returns with a flat reality check that repeats the character's promise and negates it. E.g. character: "The whole thing will collapse in a week." → narrator: "The whole thing did not collapse in a week."
- At tragic moments, the skit turns serious, slow and emotional. No jokes.
- Label every line: [CHARACTER NAME]: line (for multi-voice dubbing).

## 4. NARRATOR VOICE
- Short sentences dominate. Many 2–5 word sentences: "The city burned.", "He was right.", "It didn't work."
- Deadpan commentary right after events, at least once per chapter: "Spoiler: …", "That was deliberate.", "He really should've kept that one to himself.", "Nobody said it was comfortable."
- Conversational words: "basically", "a guy who…", "not exactly popular", "here's the problem".
- Structural repetition for rhythm, 2–3 times per video: "And nobody did anything. … And again, nobody did anything." / "Every year, X. Every year, Y."
- Chapter-ending lines favor ANTITHESIS / PARADOX: "He won every battle and still lost the war.", "The man who promised forever lasted twelve years."
- The narrator rarely says "I", but speaks directly to the viewer when useful ("you", "remember this").

## 5. FORESHADOWING & CALLBACKS
- At least ONE explicit plant: "Remember that. It matters later." Then pay it off at the right moment: "Remember when I said that would matter?"
- At least TWO image-based foreshadows: "…and that promise sat quietly for years, waiting to ruin everybody's life.", "And that gap was about to decide everything.", "Neither of them would live to see what came next."
- EVERY teaser from the cold open must be paid off in the body.

## 6. HUMAN MOMENTS
- At least 2–3 times: stop the flow of events and slow down on ONE specific person and ONE small detail (an object, a gesture, an age, a number of days).
- Close it with a very short, heavy line ("He was a baby.", "She never saw him again.").
- Where the story is ambiguous, say so plainly: "The story doesn't say whether… Either way, …" (this builds trust).

## 7. ENDING — 4 BEATS
1. The final toll: who lost what, how much, one sentence per main character's fate, many in contrast form ("The man who X didn't survive Y.").
2. The bigger meaning: what this led to, or what it says about people. One observation, never a sermon.
3. CALLBACK to the small cause from the cold open, almost word for word: "And the whole thing started because…"
4. ONE ultra-short closing line (under 10 words) with antithesis or a haunting character quote. Then a one-sentence CTA: "If you want more stories like this, subscribe and watch the next one right here."

## OUTPUT FORMAT
A. 5 TITLE options in the channel's formulas (≤ 70 characters):
   - "The ENTIRE Story of [X] Explained"
   - "The Real Reason [X] Failed / Fell"
   - "How [small cause] Led to [huge consequence]"
B. OUTLINE: chapters with their "Now, it's…" markers, opening question, estimated duration, skit placement, and each plant ↔ payoff pair.
C. FULL SCRIPT, each block as:
   [video timestamp]
   🎙 NARRATION: …
   🗣 SKIT (if any): [CHARACTER]: …
   🎬 VISUALS: (map/location "right here", characters, on-screen text, numbers shown)
   🎵 AUDIO: (music, SFX, silence — only when needed)
D. THUMBNAIL: 2 concepts (main image + max 4 words of text, paradox preferred).
E. VIDEO DESCRIPTION (3 sentences) + chapter timestamps based on the "Now, it's…" markers.
F. Final word count of the narration + skits, and estimated runtime at 170 wpm.

## SELF-CHECK BEFORE ANSWERING
- [ ] Cold open has all 5 beats, including "But the whole thing started because…" and "So, how did…?"
- [ ] Every cold-open teaser is paid off in the body
- [ ] At least one "Remember that. It matters later." ↔ payoff pair
- [ ] A dialogue skit every 60–120 seconds; every comedic skit is followed by a flat reality check
- [ ] Every chapter has at least one deadpan line and one sentence of ≤ 5 words
- [ ] Every number has an everyday comparison
- [ ] Every new place/character has a visual anchor ("right here"…)
- [ ] Ending calls back the small cause + closing line under 10 words
- [ ] Narration word count ≈ 170 × target minutes
- [ ] Read aloud, nothing sounds stiff, academic or AI-generated; no sentence needs a breath in the middle
```

---

## PHẦN 3 — FOLLOW-UP PROMPTS (dùng sau khi có bản nháp)

**Style score:**
```
Score the script above against each SELF-CHECK item (0–10 each). For every item below 8, rewrite only the weak passage. Return the score table + rewritten passages only.
```

**More skits:**
```
Find 3 places where the script runs "dry" for more than 90 seconds. At each one, insert a 4–8 line dialogue skit: modern casual voice, characters saying what they'd normally hide, ending on a punchline. Follow each with the narrator's flat reality check.
```

**Make it punchier:**
```
Rewrite the narration so the average sentence is under 12 words. Split long sentences, cut filler, replace any formal or "AI-sounding" vocabulary with plain spoken English. Keep every fact, skit and callback.
```

**Shorten / lengthen:**
```
Adjust the script to [X] minutes (~[X × 170] words of narration). Keep the 5-beat cold open, every plant ↔ payoff pair, the climax and the ending intact. Cut or merge middle chapters only.
```

**Shorts:**
```
From the long script, write 3 YouTube Shorts scripts (≤ 60 seconds, ~150 words each). Line 1 is a paradox: "…all because of [small cause]." Then one ultra-short skit, then a deadpan line + "Full story on the channel."
```

**Clean TTS export (ElevenLabs etc.):**
```
Export the NARRATION and SKITS as one continuous read-aloud text. Keep [CHARACTER] labels on skit lines for multi-voice dubbing. Use "…" for short pauses and a line break for long pauses. Spell out all numbers and years as words (e.g. "nineteen forty-four"). Expand abbreviations. Remove all headings, emojis and visual notes.
```

**Translate an existing Vietnamese script:**
```
Translate and adapt the Vietnamese script below into natural spoken American English in the same style (short sentences, deadpan lines, modern-voice skits, "Now, it's…" transitions). Do not translate word for word; rewrite jokes and idioms so they land for an English-speaking audience. Keep all names, facts, plants and payoffs.
```

---

## PHẦN 4 — SHORT EXAMPLE (original, applying the formula to the Greek myth of King Midas)

> 🎙 **NARRATION:** For nearly 3,000 years, one man's name has meant one thing: more money than you could ever spend.
> But the whole thing started because a king was polite to a drunk old man.
> Yes, really.
> A god offered him any wish in the world, and he picked the worst one. His dinner turned to metal before it reached his mouth. And the only cure was a muddy river in the middle of nowhere.
> So, how did one good deed turn into the most famous curse in history? Let's start with the drunk.
>
> 🗣 **SKIT:**
> [DIONYSUS]: You found my teacher and brought him home. Name your reward.
> [MIDAS]: Anything?
> [DIONYSUS]: Anything.
> [MIDAS]: Everything I touch turns to gold.
> [DIONYSUS]: …You're sure? Most people ask for, you know, health.
> [MIDAS]: Health doesn't buy palaces.
> [DIONYSUS]: Fine. Enjoy lunch.
>
> 🎙 **NARRATION:** He did not enjoy lunch.
> Remember that, by the way. Lunch. It matters later.

---

## Ghi chú
- Transcript được tải bằng `yt-dlp` (client iOS) và chỉ dùng để phân tích, không lưu vào repo.
- Các cụm tiếng Anh trích trong Phần 1 là những đoạn rất ngắn để minh họa kỹ thuật; prompt yêu cầu AI **tự viết mới**, không sao chép lời kênh gốc.
