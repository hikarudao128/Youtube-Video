import json, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
raw = subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
a = np.frombuffer(raw, np.float32)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, info = m.transcribe(a, word_timestamps=True, language="en")
out=[]
for s in segs:
    for w in s.words: out.append([round(w.start,2), round(w.end,2), w.word])
json.dump(out, open(sys.argv[2],"w"))
print(len(out))
