import json, subprocess, os
from concurrent.futures import ThreadPoolExecutor
S=os.path.dirname(os.path.abspath(__file__))
AUDIO=[f for f in os.listdir("/root/.claude/uploads/f2e08ef8-f343-52c0-b38c-8cce9b890c0a") if f.endswith(".mp3")][0]
AUDIO="/root/.claude/uploads/f2e08ef8-f343-52c0-b38c-8cce9b890c0a/"+AUDIO
FPS=30
seq=json.load(open(f"{S}/seq.json")); starts=json.load(open(f"{S}/starts.json"))
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",AUDIO]))
starts[0]=0.0
segs=[]  # (image, start)
for i,(f,t) in enumerate(zip(seq,starts)):
    if f is None: continue  # hold previous image
    segs.append((f,t))
total=round(dur*FPS)
frames=[round(t*FPS) for _,t in segs]+[total]
os.makedirs(f"{S}/segs",exist_ok=True)
jobs=[]
for k,(f,_) in enumerate(segs):
    n=frames[k+1]-frames[k]
    zin = k%2==0
    z = f"1+0.06*on/{n}" if zin else f"1.06-0.06*on/{n}"
    vf=(f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
        f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={FPS},"
        f"format=yuv420p")
    out=f"{S}/segs/{k:03d}.mp4"
    jobs.append(["ffmpeg","-v","error","-y","-loop","1","-framerate",str(FPS),"-i",f"{S}/imgs/{f}","-vf",vf,
                 "-frames:v",str(n),"-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),out])
with ThreadPoolExecutor(4) as ex: list(ex.map(lambda c: subprocess.run(c,check=True),jobs))
open(f"{S}/segs/list.txt","w").write("".join(f"file '{S}/segs/{k:03d}.mp4'\n" for k in range(len(segs))))
json.dump({"segs":segs,"frames":frames,"dur":dur},open(f"{S}/plan.json","w"))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{S}/segs/list.txt","-i",AUDIO,
  "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",f"{S}/out.mp4"],check=True)
print("segments",len(segs),"frames",total,"dur",dur)
