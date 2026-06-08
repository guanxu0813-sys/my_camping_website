#!/usr/bin/env python3
"""Download official product images to assets/products/{brandId}/."""

from __future__ import annotations

import argparse
import sys
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import OFFICIAL_DIR, RateLimiter, read_json, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "assets" / "products"

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


def download_image(url: str, dest: Path, limiter: RateLimiter) -> None:
    limiter.wait()
    req = urllib.request.Request(url, headers={"User-Agent": "CampGearCompareScraper/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()

    dest.parent.mkdir(parents=True, exist_ok=True)
    if Image is not None:
        img = Image.open(BytesIO(data))
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        elif img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        img.save(dest, format="WEBP", quality=82, method=6)
    else:
        ext = Path(urllib.parse.urlparse(url).path).suffix or ".jpg"
        dest = dest.with_suffix(ext)
        dest.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Download official catalog images")
    parser.add_argument("brand", help="brandId directory under data/official/")
    parser.add_argument("--status", default="verified", help="Only products with this status")
    parser.add_argument("--all", action="store_true", help="Download for all products regardless of status")
    args = parser.parse_args()

    products_path = OFFICIAL_DIR / args.brand / "products.json"
    if not products_path.exists():
        print(f"Missing {products_path}", file=sys.stderr)
        return 1

    products = read_json(products_path)
    limiter = RateLimiter(0.75)
    updated = 0

    for product in products:
        if not args.all and product.get("status") != args.status:
            continue
        url = product.get("imageUrl")
        if not url:
            continue
        rel = Path("assets") / "products" / args.brand / f"{product['id']}.webp"
        dest = ROOT / rel
        try:
            download_image(url, dest, limiter)
            product["imageLocal"] = rel.as_posix()
            updated += 1
            print(f"OK {product['id']} -> {rel}")
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {product['id']}: {exc}", file=sys.stderr)

    write_json(products_path, products)
    print(f"Downloaded {updated} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
