from PIL import Image, ImageDraw, ImageFont
import sys, os
out = sys.argv[1]
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def grad(w,h,c1,c2):
    im=Image.new("RGB",(w,h)); px=im.load()
    for x in range(w):
        for y in range(h):
            t=(x/w*0.6+y/h*0.4)
            px[x,y]=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))
    return im
def icon(size):
    s=512
    bg=grad(s,s,(30,58,138),(29,78,216))
    m=Image.new("L",(s,s),0); ImageDraw.Draw(m).rounded_rectangle([0,0,s-1,s-1],radius=110,fill=255)
    im=Image.new("RGBA",(s,s),(0,0,0,0)); im.paste(bg,(0,0),m)
    d=ImageDraw.Draw(im); f=ImageFont.truetype(B,230)
    d.text((s/2,s/2+6),"ТС",font=f,fill="white",anchor="mm")
    return im.resize((size,size),Image.LANCZOS)
icon(32).save(os.path.join(out,"favicon-32x32.png"))
icon(512).save(os.path.join(out,"icon-512.png"))
a=icon(180).convert("RGB"); a.save(os.path.join(out,"apple-touch-icon.png"))
icon(64).save(os.path.join(out,"favicon.ico"),sizes=[(16,16),(32,32),(48,48)])
# OG image
W,H=1200,630
og=grad(W,H,(30,58,138),(59,130,246)); d=ImageDraw.Draw(og)
d.text((80,150),"Калкулатор за",font=ImageFont.truetype(B,76),fill="white")
d.text((80,240),"трудов стаж",font=ImageFont.truetype(B,76),fill="white")
d.text((80,360),"Години, месеци и дни  •  Няколко периода  •  Безплатно",font=ImageFont.truetype(R,32),fill=(219,234,254))
d.rounded_rectangle([80,450,620,520],radius=16,fill="white")
d.text((350,485),"workexperiencecalculator.online",font=ImageFont.truetype(B,26),fill=(30,58,138),anchor="mm")
ic=icon(200); og.paste(ic,(920,80),ic)
og.save(os.path.join(out,"og-image.png"),optimize=True)
