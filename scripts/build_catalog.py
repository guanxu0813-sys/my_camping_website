#!/usr/bin/env python3
"""Bundle data/*.json into data/catalog.js for file:// preview."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts" / "scrape"))

from common import is_visible_on_site  # noqa: E402


def load_official_products() -> list:
    products: list = []
    official = DATA / "official"
    index_path = official / "index.json"
    if index_path.exists():
        brand_ids = json.loads(index_path.read_text(encoding="utf-8")).get("brandIds", [])
    else:
        brand_ids = [p.name for p in official.iterdir() if p.is_dir() and (p / "products.json").exists()]

    for brand_id in brand_ids:
        path = official / brand_id / "products.json"
        if not path.exists():
            continue
        batch = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(batch, list):
            products.extend(p for p in batch if isinstance(p, dict) and is_visible_on_site(p))
    return products


def main() -> None:
    brands = json.loads((DATA / "brands.json").read_text(encoding="utf-8"))
    products = load_official_products()
    site = json.loads((DATA / "site.json").read_text(encoding="utf-8"))
    sponsors_path = DATA / "sponsors.json"
    sponsors = (
        json.loads(sponsors_path.read_text(encoding="utf-8"))
        if sponsors_path.exists()
        else {"campaigns": []}
    )
    payload = {
        "brands": brands,
        "products": products,
        "site": site,
        "sponsors": sponsors,
        "source": "official",
    }
    out = DATA / "catalog.js"
    header = "// Auto-generated from data/official — run: python3 scripts/build_catalog.py\n"
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    out.write_text(header + "window.CAMPGEAR_DATA = " + body + ";\n", encoding="utf-8")
    print(f"Wrote {out} ({len(products)} official products, {len(brands)} brands)")


if __name__ == "__main__":
    main()
