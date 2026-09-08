#!/usr/bin/env python3
"""Decode and make visual QA sheets for website-first week-two assets."""

from pathlib import Path
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/social/week2/product-v3"
QA=Path("/private/tmp/week2-v3-qa"); QA.mkdir(parents=True,exist_ok=True)
FONT=ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc",18,index=1)
FF=imageio_ffmpeg.get_ffmpeg_exe()

def sheet(paths, out, thumb):
    cols=5; rows=(len(paths)+cols-1)//cols
    canvas=Image.new("RGB",(cols*thumb[0],rows*(thumb[1]+34)),"#dedbd2")
    d=ImageDraw.Draw(canvas)
    for i,p in enumerate(paths):
        im=Image.open(p).convert("RGB"); im.thumbnail(thumb,Image.Resampling.LANCZOS)
        x=(i%cols)*thumb[0]+(thumb[0]-im.width)//2; y=(i//cols)*(thumb[1]+34)
        canvas.paste(im,(x,y)); d.text((x+5,y+thumb[1]+5),p.stem,font=FONT,fill="#173e36")
    canvas.save(out,quality=92)

pins=sorted((ASSETS/"pinterest").glob("*.png"))
assert len(pins)==15
for p in pins:
    assert Image.open(p).size==(1000,1500)
sheet(pins,QA/"pins-mobile-sheet.jpg",(200,300))

frames=[]
videos=sorted((ASSETS/"video").glob("*.mp4")); assert len(videos)==10
for video in videos:
    # Full decode is the acceptance check. Extraction samples four moments for visual review.
    subprocess.run([FF,"-v","error","-i",str(video),"-f","null","-"],check=True)
    for n,t in enumerate((1.0,4.0,7.0,10.0)):
        out=QA/f"{video.stem}-{n}.png"
        subprocess.run([FF,"-v","error","-ss",str(t),"-i",str(video),"-frames:v","1","-y",str(out)],check=True)
        frames.append(out)
sheet(frames,QA/"videos-frames-sheet.jpg",(180,320))
print(QA/"pins-mobile-sheet.jpg")
print(QA/"videos-frames-sheet.jpg")
print("decoded 10/10 videos; checked 15/15 pin dimensions")
