# Lão Hạc — "Why you feel guilty when you betray an animal"

Builds the 1920x1080 / 30fps MP4 from the ElevenLabs voiceover and the 110 images in the Drive folder `Lão Hạc/zapi-img`.

1. `tr.py` – transcribes the voiceover with faster-whisper (word-level timestamps).
2. `align.py` – aligns the 111 transcript lines to the real audio timing.
3. `mapping.py` – maps each line to its image (prompt `[01:33] TRUST BROKEN` has no image, file 37 is missing, so the previous image is held).
4. `render.py` – renders each image with a light Ken Burns zoom, cuts on the aligned times, and muxes the audio (H.264 CRF 18 + AAC 192k).

`timeline.csv` lists the final cut points. The output video lives in `output/` (gitignored, ~99 MB).
