#!/usr/bin/env python3
"""Build deterministic Pinterest cards and vertical-video frames for Week 2."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlencode

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets" / "social" / "week2"
CONTENT = json.loads((BASE / "content.json").read_text(encoding="utf-8"))
FONT_REGULAR = "/System/Library/Fonts/Avenir Next.ttc"
FONT_BOLD = "/System/Library/Fonts/Avenir Next.ttc"
GREEN = "#173c35"
CREAM = "#f4efe3"
ORANGE = "#e7863a"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size, index=1 if bold else 0)


def cover(image: Image.Image, size: tuple[int, int], focus_y: float = 0.5) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_w) // 2)
    top = max(0, min(resized.height - target_h, round((resized.height - target_h) * focus_y)))
    return resized.crop((left, top, left + target_w, top + target_h))


def wrap(draw: ImageDraw.ImageDraw, text: str, selected_font, max_width: int) -> list[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if draw.textbbox((0, 0), candidate, font=selected_font)[2] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def multiline(draw, xy, text, selected_font, fill, max_width, spacing=12, anchor="la"):
    lines = wrap(draw, text, selected_font, max_width)
    x, y = xy
    line_height = selected_font.size + spacing
    for line in lines:
        draw.text((x, y), line, font=selected_font, fill=fill, anchor=anchor)
        y += line_height
    return y


def add_brand(draw, width, y=54):
    draw.rounded_rectangle((54, y, 416, y + 58), radius=29, fill=GREEN)
    draw.text((78, y + 29), "CAMPGEAR COMPARE", font=font(24, True), fill=CREAM, anchor="lm")


def build_pin(item, pin, index):
    out = BASE / "pinterest" / f"{item['slug']}-{index:02d}.png"
    if out.exists():
        return
    bg = Image.open(BASE / "backgrounds" / item["background"]).convert("RGB")
    canvas = cover(bg, (1000, 1500), focus_y=0.45)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 1000, 1500), fill=(9, 28, 25, 70))
    od.rounded_rectangle((54, 138, 946, 790), radius=34, fill=(244, 239, 227, 238))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(canvas)
    add_brand(draw, 1000)
    draw.text((92, 194), pin["eyebrow"], font=font(27, True), fill=ORANGE)
    y = multiline(draw, (92, 248), pin["title"], font(58, True), GREEN, 810, spacing=9)
    draw.rounded_rectangle((92, y + 24, 650, y + 126), radius=20, fill=GREEN)
    draw.text((120, y + 75), pin["stat"], font=font(42, True), fill=CREAM, anchor="lm")
    multiline(draw, (92, y + 158), pin["detail"], font(30), "#284940", 800, spacing=8)
    draw.rounded_rectangle((54, 1360, 946, 1446), radius=20, fill=(23, 60, 53, 235))
    draw.text((90, 1403), "See the full comparison  >", font=font(30, True), fill=CREAM, anchor="lm")
    draw.text((910, 1403), "campgearcompare.com", font=font(20), fill=CREAM, anchor="rm")
    canvas.convert("RGB").save(out, quality=94, optimize=True)


def video_slide(bg, headline, slide_no, total):
    canvas = cover(bg, (1080, 1920), focus_y=0.5).filter(ImageFilter.GaussianBlur(1.2))
    canvas = ImageEnhance.Brightness(canvas).enhance(0.58).convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 1080, 1920), fill=(7, 25, 22, 75))
    od.rounded_rectangle((64, 520, 1016, 1340), radius=42, fill=(244, 239, 227, 235))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)
    add_brand(draw, 1080, y=72)
    size = 76 if len(headline) < 32 else 62
    lines = wrap(draw, headline, font(size, True), 820)
    block_h = len(lines) * (size + 16)
    y = 930 - block_h / 2
    for line in lines:
        draw.text((540, y), line, font=font(size, True), fill=GREEN, anchor="ma")
        y += size + 16
    draw.rectangle((440, y + 28, 640, y + 36), fill=ORANGE)
    draw.text((540, 1265), f"{slide_no}/{total}", font=font(26, True), fill="#557068", anchor="mm")
    draw.text((540, 1790), "campgearcompare.com", font=font(30, True), fill=CREAM, anchor="mm")
    return canvas.convert("RGB")


def build_video_frames(item, script, video_index):
    bg = Image.open(BASE / "backgrounds" / item["background"]).convert("RGB")
    frame_dir = BASE / "frames" / f"{item['slug']}-{video_index:02d}"
    frame_dir.mkdir(parents=True, exist_ok=True)
    if len(list(frame_dir.glob("*.png"))) == len(script):
        return
    frame_number = 0
    for slide_no, headline in enumerate(script, 1):
        slide = video_slide(bg, headline, slide_no, len(script))
        # The encoder presents each card for three seconds.
        slide.save(frame_dir / f"{frame_number:03d}.png")
        frame_number += 1


def main():
    for item in CONTENT:
        for index, pin in enumerate(item["pins"], 1):
            build_pin(item, pin, index)
        for index, script in enumerate(item["videos"], 1):
            build_video_frames(item, script, index)
    print("Built 15 Pinterest images and 10 video frame sequences.")


if __name__ == "__main__":
    main()
