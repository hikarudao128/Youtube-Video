import json, os, re
S=os.path.dirname(os.path.abspath(__file__))
files=os.listdir(f"{S}/imgs")
bynum={}
for f in files:
    m=re.match(r"(\d+)_\[(\d\d)-(\d\d)\]",f)
    if m: bynum[(int(m[1]),f"{m[2]}:{m[3]}")]=f
starts=json.load(open(f"{S}/starts.json"))
seq=[]
for i in range(111):
    if i==0: f=bynum[(1,"00:00")]
    elif i==1: f=[x for x in files if x.startswith("Cartoon_dog")][0]
    elif i==2: f=bynum[(1,"00:05")]
    elif i==38: f=None   # prompt [01:33] TRUST BROKEN -> file 37 missing
    else: f=[v for (n,_),v in bynum.items() if n==i-1][0]
    seq.append(f)
json.dump(seq,open(f"{S}/seq.json","w"),indent=0)
used={x for x in seq if x}; print("unused:",set(files)-used, "missing idx:",[i for i,x in enumerate(seq) if not x])
