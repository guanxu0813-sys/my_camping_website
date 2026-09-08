#!/usr/bin/env python3
"""Encode Week 2 vertical slide sequences as 15-second H.264 MP4 files."""

from pathlib import Path
import subprocess

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets" / "social" / "week2"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def main():
    outputs = []
    for frame_dir in sorted((BASE / "frames").iterdir()):
        if not frame_dir.is_dir():
            continue
        output = BASE / "video" / f"{frame_dir.name}.mp4"
        subprocess.run(
            [
                FFMPEG,
                "-hide_banner", "-loglevel", "error", "-y", "-threads", "1",
                "-framerate", "1/3", "-i", str(frame_dir / "%03d.png"),
                "-frames:v", "5", "-vf", "scale=720:1280",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                str(output),
            ],
            check=True,
        )
        outputs.append(output)
    print(f"Encoded {len(outputs)} vertical MP4 videos.")


if __name__ == "__main__":
    main()
