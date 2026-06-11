#!/usr/bin/env python3
"""Legacy: merge verified official catalog entries into data/products.json.

The site reads data/official/ directly; this script is only for exporting to the
old products.json format.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import OFFICIAL_DIR, read_json, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PRODUCTS_PATH = ROOT / "data" / "products.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_catalog.py"


def official_to_display(item: dict[str, Any], target_id: str | None = None) -> dict[str, Any]:
    specs = item.get("specs") or {}
    out: dict[str, Any] = {
        "id": target_id or item["id"],
        "brandId": item["brandId"],
        "category": item["category"],
        "model": item["model"],
        "priceMin": item.get("priceMin", item.get("price")),
        "priceMax": item.get("priceMax", item.get("price")),
        "highlights": item.get("highlights") or [],
        "inSummaryTable": item.get("inSummaryTable", True),
        "inDetailCards": item.get("inDetailCards", True),
        "sourceUrl": item.get("sourceUrl"),
        "description": item.get("description"),
        "scrapedAt": item.get("scrapedAt"),
    }

    image = item.get("imageLocal") or item.get("imageUrl")
    if image:
        out["imageUrl"] = image if image.startswith(("http", "/")) else f"/{image.lstrip('/')}"
    if item.get("imageAlt"):
        out["imageAlt"] = item["imageAlt"]

    for key in (
        "structure",
        "detailStructure",
        "weightKg",
        "weightDisplay",
        "weightRange",
        "capacity",
        "fabric",
        "tarpType",
        "size",
        "scenarios",
        "pros",
        "cons",
        "subcategory",
    ):
        if key in item and item[key] not in (None, ""):
            out[key] = item[key]
        elif key in specs and specs[key] not in (None, ""):
            out[key] = specs[key]

    if item["category"] == "tent" and "structure" in out and "detailStructure" not in out:
        out["detailStructure"] = out["structure"]
    if item["category"] == "tarp" and "subcategory" in out and "tarpType" not in out:
        out["tarpType"] = out["subcategory"]

    out = {k: v for k, v in out.items() if v is not None}
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge verified official products into products.json")
    parser.add_argument("brand", help="brandId under data/official/")
    parser.add_argument("--ids", nargs="+", help="Official product ids to merge")
    parser.add_argument(
        "--target-id",
        help="When merging a single product, write to this existing products.json id",
    )
    parser.add_argument("--include-verified", action="store_true", help="Merge all status=verified")
    parser.add_argument("--mark-merged", action="store_true", default=True)
    parser.add_argument("--no-build", action="store_true")
    args = parser.parse_args()

    official_path = OFFICIAL_DIR / args.brand / "products.json"
    if not official_path.exists():
        print(f"Missing {official_path}", file=sys.stderr)
        return 1

    official = read_json(official_path)
    display = read_json(PRODUCTS_PATH)
    by_id = {p["id"]: p for p in display}

    selected: list[dict[str, Any]] = []
    if args.ids:
        wanted = set(args.ids)
        selected = [p for p in official if p["id"] in wanted]
    elif args.include_verified:
        selected = [p for p in official if p.get("status") == "verified"]
    else:
        print("Provide --ids or --include-verified", file=sys.stderr)
        return 1

    if not selected:
        print("No matching official products", file=sys.stderr)
        return 1

    if args.target_id and len(selected) != 1:
        print("--target-id requires exactly one selected product", file=sys.stderr)
        return 1

    merged_count = 0
    for item in selected:
        if item.get("status") not in ("verified", "merged") and not args.ids:
            print(f"Skip {item['id']}: status={item.get('status')}", file=sys.stderr)
            continue
        target_id = args.target_id if args.target_id else item["id"]
        by_id[target_id] = official_to_display(item, target_id=target_id)
        item["status"] = "merged"
        merged_count += 1
        print(f"Merged {item['id']} -> products.json#{target_id}")

    write_json(PRODUCTS_PATH, list(by_id.values()))
    write_json(official_path, official)

    if not args.no_build and BUILD_SCRIPT.exists():
        subprocess.run([sys.executable, str(BUILD_SCRIPT)], check=True)

    print(f"Done. Merged {merged_count} product(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
