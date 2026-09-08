#!/usr/bin/env python3
"""Build website-first Pinterest and Shorts assets from real CampGear Compare captures."""

from __future__ import annotations

import csv
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets" / "social" / "week2"
CAP = BASE / "site-captures-v3"
OUT = BASE / "product-v3"
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
GREEN, CREAM, ORANGE, INK = "#123a33", "#f7f1e4", "#f08a3c", "#173e36"
FPS = 12

GROUPS = [
    ("gear-report", [
        ("report-results.png", "543 PRODUCTS. ONE CLEAN REPORT.", "OPEN THE REPORT", (150, 215, 1130, 675)),
        ("report-results.png", "COMPARE WEIGHT AND PRICE BY CATEGORY", "SCAN THE CATEGORY TABLE", (120, 360, 1160, 690)),
        ("tent-table.png", "GO FROM REPORT TO LIVE GEAR TABLE", "EXPLORE THE DATA", (40, 100, 1240, 690)),
    ], [
        ("See the report—not another gear list", ["report-results.png", "tent-table.png"], "543 products become a usable comparison"),
        ("Start with category-level evidence", ["report-results.png", "tents-shortlist.png"], "Then open the shortlist that fits your trip"),
    ]),
    ("tents-under-2kg", [
        ("tents-shortlist.png", "14 TENTS UNDER 2 KG—SIDE BY SIDE", "OPEN THE SHORTLIST", (95, 220, 1175, 690)),
        ("search-cloud-up.png", "SEARCH 275 TENT MODELS IN SECONDS", "TYPE A MODEL NAME", (120, 120, 1160, 620)),
        ("compare-two-models.png", "SELECT TWO. COMPARE THE TRADE-OFF.", "USE THE COMPARE TRAY", (100, 210, 1170, 705)),
    ], [
        ("Need a tent under 2 kg?", ["tents-shortlist.png", "search-cloud-up.png", "compare-two-models.png"], "Search, select, and compare on the live site"),
        ("Stop opening twenty product tabs", ["search-cloud-up.png", "compare-two-models.png"], "The comparison tray keeps the decision together"),
    ]),
    ("lanshan", [
        ("guide-lanshan-top.png", "Lanshan 1 OR 2? START WITH YOUR USE CASE.", "READ THE 3-STEP GUIDE", (80, 150, 1200, 690)),
        ("guide-lanshan-table.png", "SEE BOTH OFFICIAL SPECS TOGETHER", "COMPARE THE NUMBERS", (95, 85, 1180, 660)),
        ("guide-lanshan-table.png", "CHECK THE EVIDENCE BEHIND THE VERDICT", "FOLLOW THE SOURCES", (110, 300, 1170, 705)),
    ], [
        ("Lanshan 1 or Lanshan 2?", ["guide-lanshan-top.png", "guide-lanshan-table.png"], "The guide moves from use case to verified specs"),
        ("A verdict you can audit", ["guide-lanshan-table.png", "guide-lanshan-top.png"], "Official specifications sit beside the recommendation"),
    ]),
    ("cloud-up", [
        ("search-cloud-up.png", "TYPE CLOUD UP. SEE 12 MATCHES.", "TRY THE LIVE SEARCH", (115, 120, 1160, 620)),
        ("product-modal.png", "OPEN A MODEL WITHOUT LEAVING THE TABLE", "CHECK SPECS + SOURCE", (210, 80, 1070, 690)),
        ("cloud-models.png", "COMPARE CLOUD UP MODELS IN ONE GUIDE", "SEE THE MODEL TABLE", (90, 165, 1190, 690)),
    ], [
        ("Which Cloud Up model is actually yours?", ["search-cloud-up.png", "product-modal.png", "cloud-models.png"], "Search the catalog, inspect the model, read the guide"),
        ("The product page is inside the comparison", ["product-modal.png", "compare-two-models.png"], "Specs and the official-source link stay one click away"),
    ]),
    ("neoair", [
        ("search-neoair.png", "SEARCH NEOAIR. NARROW 127 TO 5.", "FILTER THE PAD TABLE", (115, 115, 1160, 625)),
        ("xlite-specs.png", "XLITE VS XTHERM: SPECS SIDE BY SIDE", "READ THE COMPARISON", (100, 140, 1180, 700)),
        ("compare-neoair.png", "SELECT THE TWO PADS YOU'RE DECIDING BETWEEN", "COMPARE YOUR FINALISTS", (90, 210, 1190, 705)),
    ], [
        ("XLite or XTherm? Start on the site", ["search-neoair.png", "compare-neoair.png", "xlite-specs.png"], "Filter 127 pads, select finalists, then read the verdict"),
        ("Turn five NeoAir matches into one decision", ["search-neoair.png", "xlite-specs.png"], "Use the specs table to see the real trade-off"),
    ]),
]


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_PATH, size=size, index=1 if bold else 0)


def wrap(draw, text, fnt, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if not line or draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            line = trial
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    return lines


def browser_card(source: Image.Image, box, crop=None):
    x1, y1, x2, y2 = box
    card = Image.new("RGB", (x2-x1, y2-y1), "white")
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((0, 0, card.width-1, card.height-1), radius=26, fill="white", outline="#d9d4c9", width=3)
    draw.rectangle((1, 42, card.width-2, card.height-2), fill="white")
    draw.ellipse((18, 15, 32, 29), fill="#ef6b5e"); draw.ellipse((40, 15, 54, 29), fill="#f5bd4f"); draw.ellipse((62, 15, 76, 29), fill="#61c454")
    inner = (14, 52, card.width-14, card.height-14)
    img = source.crop(crop) if crop else source
    scale = min((inner[2]-inner[0])/img.width, (inner[3]-inner[1])/img.height)
    img = img.resize((round(img.width*scale), round(img.height*scale)), Image.Resampling.LANCZOS)
    px = inner[0] + (inner[2]-inner[0]-img.width)//2; py = inner[1] + (inner[3]-inner[1]-img.height)//2
    card.paste(img, (px, py))
    return card


def build_pin(slug, idx, spec):
    filename, headline, label, crop = spec
    src = Image.open(CAP / filename).convert("RGB")
    canvas = Image.new("RGB", (1000, 1500), CREAM); d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((42, 35, 395, 95), radius=30, fill=GREEN)
    d.text((218, 65), "CAMPGEAR COMPARE", font=font(23, True), fill=CREAM, anchor="mm")
    f = font(65, True); lines = wrap(d, headline, f, 890)
    y = 145
    for line in lines[:3]: d.text((55, y), line, font=f, fill=INK); y += 75
    full = browser_card(src, (45, 390, 955, 960))
    canvas.paste(full, (45, 390))
    zoom = browser_card(src, (90, 990, 910, 1320), crop)
    canvas.paste(zoom, (90, 990))
    d.rounded_rectangle((70, 1360, 930, 1450), radius=28, fill=GREEN)
    d.text((500, 1405), label + "  >", font=font(28, True), fill=CREAM, anchor="mm")
    out = OUT / "pinterest" / f"{slug}-{idx:02d}.png"; out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, optimize=True)


def video_canvas(src, crop, progress, title, scene_label, final=False):
    canvas = Image.new("RGB", (720, 1280), CREAM); d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((25, 24, 350, 80), radius=28, fill=GREEN)
    d.text((188, 52), "CAMPGEAR COMPARE", font=font(20, True), fill=CREAM, anchor="mm")
    f = font(52 if not final else 46, True); lines = wrap(d, title, f, 650)
    y = 120
    for line in lines[:3]: d.text((360, y), line, font=f, fill=INK, anchor="ma"); y += f.size+5
    x1,y1,x2,y2=crop; pad=20
    # continuous push-in and horizontal drift makes every scene visibly animated
    z = 1.0 + .10*progress
    cw,ch=x2-x1,y2-y1; nw,nh=cw/z,ch/z
    drift=(cw-nw)*(.25+.5*progress)
    box=(x1+drift, y1+(ch-nh)*progress*.55, x1+drift+nw, y1+(ch-nh)*progress*.55+nh)
    card = browser_card(src, (30, 330, 690, 1090), box)
    canvas.paste(card, (30,330))
    pulse = 16 + round(7*(1+math.sin(progress*math.pi*4)))
    d.ellipse((602-pulse, 1012-pulse, 602+pulse, 1012+pulse), outline=ORANGE, width=7)
    d.rounded_rectangle((45, 1125, 675, 1210), radius=25, fill=GREEN)
    d.text((360, 1167), scene_label, font=font(26, True), fill=CREAM, anchor="mm")
    return canvas


def build_video(slug, idx, spec):
    hook, files, conclusion = spec
    scenes=[]
    for filename in files:
        src=Image.open(CAP/filename).convert("RGB")
        scenes.append((src, (0, 70, src.width, src.height), "LIVE SITE WALKTHROUGH"))
    durations=[3]+[max(3, (12-3)//len(scenes))]*len(scenes)
    out=OUT/"video"/f"{slug}-{idx:02d}.mp4"; out.parent.mkdir(parents=True, exist_ok=True)
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    p=subprocess.Popen([ff,"-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","720x1280","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],stdin=subprocess.PIPE)
    # First three seconds are a hook, but still show the live website in motion.
    ordered=[(scenes[0][0], hook, "WATCH THE SITE WORK")]+[(s[0], hook, f"STEP {i+1} OF {len(scenes)}") for i,s in enumerate(scenes)]+[(scenes[-1][0], conclusion, "OPEN THE LIVE COMPARISON >")]
    seconds=[3]+[3]*len(scenes)+[3]
    for si,((src,title,label),sec) in enumerate(zip(ordered,seconds)):
        n=sec*FPS
        for j in range(n):
            frame=video_canvas(src,(0,60,src.width,src.height),j/max(1,n-1),title,label,si==len(ordered)-1)
            p.stdin.write(frame.tobytes())
    p.stdin.close()
    if p.wait()!=0: raise RuntimeError(out)


def write_manifest():
    rows=[]
    for slug,pins,videos in GROUPS:
        for i,s in enumerate(pins,1):
            rows.append(["pinterest",f"{slug}-{i:02d}.png",s[1],f"?utm_source=pinterest&utm_medium=organic&utm_campaign=week2_product_demo&utm_content={slug}_pin{i}","headline_or_ui_crop"])
        for i,s in enumerate(videos,1):
            rows.append(["youtube_shorts",f"{slug}-{i:02d}.mp4",s[0],f"?utm_source=youtube&utm_medium=shorts&utm_campaign=week2_product_demo&utm_content={slug}_short{i}","hook_or_walkthrough_order"])
    path=ROOT/"docs"/"week2-product-v3-publishing.csv"
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["channel","asset","caption_hook","utm","test_variable"]); w.writerows(rows)


def main():
    for slug,pins,videos in GROUPS:
        for i,s in enumerate(pins,1): build_pin(slug,i,s)
        for i,s in enumerate(videos,1): build_video(slug,i,s)
    write_manifest()
    print("built 15 website-first pins and 10 animated product walkthroughs")

if __name__ == "__main__": main()
