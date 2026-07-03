#!/usr/bin/env python3
"""Validate data/official/*/products.json against brands and required fields."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = ROOT / "data" / "official"
BRANDS_PATH = ROOT / "data" / "brands.json"

REQUIRED = frozenset(
    {
        "id",
        "brandId",
        "category",
        "model",
        "sourceUrl",
        "sourceSite",
        "scrapedAt",
        "status",
    }
)
VALID_STATUS = frozenset({"draft", "verified", "merged"})
VALID_CATEGORY = frozenset(
    {"tent", "tarp", "sleeping-bag", "sleeping-pad", "stove", "table", "chair", "other"}
)
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def main() -> int:
    brand_ids = {b["id"] for b in json.loads(BRANDS_PATH.read_text(encoding="utf-8"))}
    errors: list[str] = []

    for products_path in sorted(OFFICIAL.glob("*/products.json")):
        brand_dir = products_path.parent.name
        try:
            products = json.loads(products_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{products_path}: invalid JSON: {exc}")
            continue

        if not isinstance(products, list):
            errors.append(f"{products_path}: must be a JSON array")
            continue

        seen_ids: set[str] = set()
        for i, p in enumerate(products):
            prefix = f"{products_path}[{i}]"
            if not isinstance(p, dict):
                errors.append(f"{prefix}: must be an object")
                continue

            missing = REQUIRED - p.keys()
            if missing:
                errors.append(f"{prefix}: missing fields {sorted(missing)}")
                continue

            pid = p["id"]
            if pid in seen_ids:
                errors.append(f"{prefix}: duplicate id {pid!r}")
            seen_ids.add(pid)

            if not ID_PATTERN.match(pid):
                errors.append(f"{prefix}: invalid id {pid!r}")

            if p["brandId"] not in brand_ids:
                errors.append(f"{prefix}: unknown brandId {p['brandId']!r}")

            if p["brandId"] != brand_dir and brand_dir not in ("_manifest",):
                errors.append(
                    f"{prefix}: brandId {p['brandId']!r} != directory {brand_dir!r}"
                )

            if p["category"] not in VALID_CATEGORY:
                errors.append(f"{prefix}: invalid category {p['category']!r}")

            if p["status"] not in VALID_STATUS:
                errors.append(f"{prefix}: invalid status {p['status']!r}")

        print(f"OK {products_path} ({len(products)} products)")

    manifest_path = OFFICIAL / "_manifest.json"
    if manifest_path.exists():
        json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"OK {manifest_path}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
