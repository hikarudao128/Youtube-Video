import json, re, difflib
W=json.load(open("words.json"))
norm=lambda s: re.sub(r"[^a-z0-9]","",s.lower())
wt=[norm(w[2]) for w in W]
lines=[]
for l in open("/root/.claude/uploads/f2e08ef8-f343-52c0-b38c-8cce9b890c0a/241727b7-transcript_1.txt"):
    m=re.match(r"\[(\d+):(\d+)\]\s*(.*)",l.strip())
    if m: lines.append((int(m[1])*60+int(m[2]), m[3]))
tt=[];owner=[]
for i,(t,txt) in enumerate(lines):
    for tok in txt.split():
        n=norm(tok)
        if n: tt.append(n); owner.append(i)
sm=difflib.SequenceMatcher(None,tt,wt,autojunk=False)
tmap={}
for a,b,n in sm.get_matching_blocks():
    for k in range(n): tmap[a+k]=b+k
starts=[]
for i in range(len(lines)):
    idx=[k for k,o in enumerate(owner) if o==i]
    hit=[(k-idx[0],tmap[k]) for k in idx if k in tmap]
    starts.append(W[hit[0][1]][0] if hit else None)
print("matched tokens",len(tmap),"of",len(tt))
for i,(t,txt) in enumerate(lines): print(i,t,starts[i],txt[:50])
json.dump(starts,open("starts.json","w"))
print("last word end",W[-1][1])
