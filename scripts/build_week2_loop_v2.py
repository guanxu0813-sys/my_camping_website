#!/usr/bin/env python3
"""Build loop-v2 Pinterest creatives and genuinely animated Shorts."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets" / "social" / "week2"
OUT = BASE / "loop-v2"
CONTENT = json.loads((BASE / "content-loop-v2.json").read_text(encoding="utf-8"))
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
GREEN = "#123a33"
CREAM = "#f7f1e4"
ORANGE = "#f08a3c"
INK = "#173e36"
FPS = 12
VIDEO_SECONDS = 18


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_PATH, size=size, index=1 if bold else 0)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    w, h = size
    scale = max(w / image.width, h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - w) // 2
    top = (resized.height - h) // 2
    return resized.crop((left, top, left + w, top + h))


def wrap(draw, text, selected_font, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if not line or draw.textbbox((0, 0), candidate, font=selected_font)[2] <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_centered(draw, text, selected_font, center_x, y, max_width, fill, spacing=8):
    lines = wrap(draw, text, selected_font, max_width)
    for line in lines:
        draw.text((center_x, y), line, font=selected_font, fill=fill, anchor="ma")
        y += selected_font.size + spacing
    return y, len(lines)


def validate_sources():
    for item in CONTENT:
        guide = (ROOT / "guides" / item["guide"]).read_text(encoding="utf-8")
        for fact in item["source_checks"]:
            if fact not in guide:
                raise ValueError(f"Source check failed for {item['slug']}: {fact}")


def build_pin(item, pin, index):
    bg = cover(Image.open(BASE / "backgrounds" / item["background"]).convert("RGB"), (1000, 1500))
    bg = ImageEnhance.Contrast(bg).enhance(1.05)
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 1000, 1500), fill=(6, 27, 23, 92))
    od.rounded_rectangle((48, 110, 952, 900), radius=44, fill=(247, 241, 228, 244))
    canvas = Image.alpha_composite(bg.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((48, 34, 394, 92), radius=29, fill=GREEN)
    draw.text((221, 63), "CAMPGEAR COMPARE", font=font(23, True), fill=CREAM, anchor="mm")
    draw.text((96, 178), pin["label"], font=font(31, True), fill=ORANGE)
    y, lines = draw_centered(draw, pin["hook"], font(72, True), 500, 282, 800, INK, spacing=8)
    if lines > 3:
        raise ValueError(f"Mobile headline exceeds three lines: {pin['hook']}")
    y += 40
    draw.rounded_rectangle((110, y, 890, y + 126), radius=25, fill=GREEN)
    draw.text((500, y + 63), pin["stat"], font=font(49, True), fill=CREAM, anchor="mm")
    y, _ = draw_centered(draw, pin["decision"], font(31, True), 500, y + 175, 760, "#365a51", spacing=7)

    draw.rounded_rectangle((48, 1360, 952, 1454), radius=24, fill=(18, 58, 51, 240))
    draw.text((86, 1407), "OPEN THE VERIFIED COMPARISON", font=font(26, True), fill=CREAM, anchor="lm")
    draw.text((914, 1407), ">", font=font(36, True), fill=ORANGE, anchor="rm")
    output = OUT / "pinterest" / f"{item['slug']}-{index:02d}.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=94, optimize=True)


def ease(value):
    value = max(0.0, min(1.0, value))
    return 1 - (1 - value) ** 3


def moving_background(source, frame_index, total_frames, scene_index):
    progress = frame_index / max(1, total_frames - 1)
    zoom = 1.04 + 0.06 * progress
    target_w, target_h = round(720 * zoom), round(1280 * zoom)
    frame = cover(source, (target_w, target_h))
    travel_x = max(0, target_w - 720)
    travel_y = max(0, target_h - 1280)
    if scene_index % 2:
        left = round(travel_x * (1 - progress))
    else:
        left = round(travel_x * progress)
    top = round(travel_y * (0.25 + 0.5 * progress))
    return frame.crop((left, top, left + 720, top + 1280))


def video_frame(source, text, scene_index, local_frame, scene_frames, global_frame):
    bg = moving_background(source, local_frame, scene_frames, scene_index)
    bg = ImageEnhance.Brightness(bg).enhance(0.56).convert("RGBA")
    canvas = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    canvas = Image.alpha_composite(bg, canvas)
    draw = ImageDraw.Draw(canvas)

    fade_in = ease(local_frame / (FPS * 0.55))
    fade_out = ease((scene_frames - 1 - local_frame) / (FPS * 0.45))
    opacity = min(fade_in, fade_out)
    slide = round((1 - fade_in) * 70)

    draw.rounded_rectangle((32, 34, 357, 91), radius=28, fill=(18, 58, 51, 235))
    draw.text((194, 63), "CAMPGEAR COMPARE", font=font(21, True), fill=CREAM, anchor="mm")
    draw.rounded_rectangle((42, 270, 678, 1005), radius=40, fill=(247, 241, 228, round(238 * opacity)))

    labels = ["THE QUESTION", "THE DATA", "THE TRADE-OFF", "THE DECISION"]
    colors = [ORANGE, "#4b7f72", "#b56d34", ORANGE]
    draw.text((360, 350 + slide), labels[scene_index], font=font(29, True), fill=colors[scene_index], anchor="mm")
    size = 62 if scene_index in (0, 3) else 54
    text_font = font(size, True)
    lines = wrap(draw, text, text_font, 540)
    y = 610 + slide - len(lines) * (size + 10) / 2
    for line in lines:
        draw.text((360, y), line, font=text_font, fill=INK, anchor="ma")
        y += size + 10
    if scene_index == 3:
        draw.rounded_rectangle((135, 865 + slide, 585, 936 + slide), radius=35, fill=GREEN)
        draw.text((360, 901 + slide), "SEE FULL COMPARISON", font=font(24, True), fill=CREAM, anchor="mm")

    progress = (global_frame + 1) / (VIDEO_SECONDS * FPS)
    draw.rectangle((0, 1258, 720, 1280), fill=(247, 241, 228, 205))
    draw.rectangle((0, 1258, round(720 * progress), 1280), fill=ORANGE)
    return canvas.convert("RGB")


def build_video(item, video, index):
    source = Image.open(BASE / "backgrounds" / item["background"]).convert("RGB")
    output = OUT / "video" / f"{item['slug']}-{index:02d}.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)
    scenes = [video["hook"], video["fact1"], video["fact2"], video["decision"]]
    durations = [3, 5, 5, 5]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    process = subprocess.Popen(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", "720x1280", "-r", str(FPS), "-i", "-",
         "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)],
        stdin=subprocess.PIPE,
    )
    global_frame = 0
    try:
        for scene_index, (text, seconds) in enumerate(zip(scenes, durations)):
            count = seconds * FPS
            for local_frame in range(count):
                frame = video_frame(source, text, scene_index, local_frame, count, global_frame)
                process.stdin.write(frame.tobytes())
                global_frame += 1
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError(f"Video encoding failed: {output}")


def main():
    validate_sources()
    for item in CONTENT:
        for index, pin in enumerate(item["pins"], 1):
            build_pin(item, pin, index)
        for index, video in enumerate(item["videos"], 1):
            build_video(item, video, index)
    print("loop-v2 built: 15 mobile-first pins and 10 animated Shorts")


if __name__ == "__main__":
    main()
