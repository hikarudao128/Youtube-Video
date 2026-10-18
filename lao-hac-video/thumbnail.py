import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S="/tmp/claude-0/-home-user-Youtube-Video/f2e08ef8-f343-52c0-b38c-8cce9b890c0a/scratchpad"
W,H=1280,720
FONT="/usr/share/fonts/opentype/inter/Inter-Black.otf"
try: ImageFont.truetype(FONT,10)
except: FONT="/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
def cover(img,w,h,cx=.5,cy=.5,zoom=1.0):
    r=max(w/img.width,h/img.height)*zoom
    im=img.resize((int(img.width*r),int(img.height*r)),Image.LANCZOS)
    x=int((im.width-w)*cx); y=int((im.height-h)*cy)
    return im.crop((x,y,x+w,y+h))
def text(d,xy,s,size,fill,stroke=10,anchor="la"):
    f=ImageFont.truetype(FONT,size)
    d.text(xy,s,font=f,fill=fill,stroke_width=stroke,stroke_fill="black",anchor=anchor)
dog=Image.open(f"{S}/imgs/Cartoon_dog_showing_sad_eyes_2K_20261017195506.jpg").convert("RGB")
hac=Image.open(f"{S}/imgs/31_[01-20]_Hand-drawn_2D_doo.jpg").convert("RGB")
heart=Image.open(f"{S}/imgs/38_[01-36]_Hand-drawn_2D_doo.jpg").convert("RGB")

def split(title_lines, colors, name):
    c=Image.new("RGB",(W,H),"white")
    L=cover(dog,760,H,cx=.5,cy=1.0,zoom=1.45)          # sad eyes, crop away baked-in title
    R=cover(hac,620,H,cx=.35,cy=.5,zoom=1.15)          # Old Hac crying
    c.paste(R,(W-620,0)); 
    mask=Image.new("L",(W,H),0); md=ImageDraw.Draw(mask)
    # jagged crack edge between the two halves
    pts=[(0,0),(700,0),(740,90),(690,180),(760,290),(700,400),(770,520),(710,620),(750,H),(0,H)]
    md.polygon(pts,fill=255)
    c.paste(L.resize((W,H)) if False else Image.new("RGB",(W,H)),(0,0),None) if False else None
    Lfull=Image.new("RGB",(W,H)); Lfull.paste(L,(0,0))
    c.paste(Lfull,(0,0),mask)
    d=ImageDraw.Draw(c)
    d.line(pts[1:9],fill=(220,30,30),width=14,joint="curve")
    sz=104; y=H-30-len(title_lines)*(sz+6)
    for s,col in zip(title_lines,colors):
        text(d,(34,y),s,sz,col,stroke=12); y+=sz+6
    c.save(f"{S}/thumb/{name}.jpg",quality=95)

split(["WHY DOES","IT HURT","SO MUCH?"],["white","white",(255,214,0)],"thumb_A")
split(["HE SOLD","HIS DOG..."],["white",(255,214,0)],"thumb_B")

# C: full dog face + small Old Hac inset + big text
c=cover(dog,W,H,cx=.5,cy=.9,zoom=1.0)
c=ImageEnhance.Contrast(c).enhance(1.08)
d=ImageDraw.Draw(c)
text(d,(W//2,24),"WHY THE GUILT?",130,"white",stroke=14,anchor="ma")
ins=cover(hac,400,300,cx=.35,cy=.45,zoom=1.1)
bd=Image.new("RGB",(416,316),(220,30,30)); bd.paste(ins,(8,8))
c.paste(bd,(W-440,H-340))
c.save(f"{S}/thumb/thumb_C.jpg",quality=95)
