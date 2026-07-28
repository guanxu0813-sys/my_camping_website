#!/usr/bin/env python3
"""Create a review queue of repeated product families; never publishes pages."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

import build_guides as guides
import build_sitemap as catalog

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "data" / "reports" / "guide-candidates.csv"
GENERIC_TOKENS = frozenset(
    {
        "the",
        "and",
        "with",
        "camping",
        "backpacking",
        "ultralight",
        "lightweight",
        "tent",
        "tents",
        "sleeping",
        "bag",
        "pad",
        "table",
        "chair",
        "stove",
        "person",
        "used",
        "new",
    }
)


def model_tokens(product: dict) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", str(product.get("model") or "").lower())
    brand_tokens = set(
        re.findall(r"[a-z0-9]+", str(product.get("brandId") or "").replace("-", " "))
    )
    return [
        token
        for token in tokens
        if token not in GENERIC_TOKENS
        and token not in brand_tokens
        and not token.isdigit()
        and len(token) > 1
    ]


def family_key(product: dict) -> str | None:
    tokens = model_tokens(product)
    if not tokens:
        return None
    return " ".join(tokens[:2] if len(tokens) > 1 else tokens)


def approved_slugs() -> set[str]:
    return {
        guide["slug"]
        for guide in [
            *guides.all_comparison_guides(),
            *guides.all_collection_guides(),
        ]
    }


def slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def build_candidates(limit: int) -> list[dict]:
    products = [
        product
        for product in catalog.load_official_products()
        if not catalog.is_low_value_accessory(product)
        and product.get("inSummaryTable") is not False
    ]
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for product in products:
        family = family_key(product)
        if family:
            grouped[(product.get("brandId", ""), product.get("category", ""), family)].append(
                product
            )

    existing = approved_slugs()
    candidates = []
    for (brand_id, category, family), rows in grouped.items():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda product: (product.get("model") or "").lower())
        slug = slugify(f"{brand_id}-{family}-models-compared")
        if slug in existing:
            continue
        complete = sum(
            1
            for product in rows
            if catalog.parse_weight_kg(product) is not None
            and catalog.parse_price(product) is not None
        )
        score = min(len(rows), 10) * 3 + complete * 2
        candidates.append(
            {
                "score": score,
                "review_status": "candidate",
                "suggested_type": "collection" if len(rows) > 3 else "comparison",
                "slug": slug,
                "brand_id": brand_id,
                "category": category,
                "family": family.title(),
                "product_count": len(rows),
                "complete_weight_price": complete,
                "suggested_query": f"{brand_id.replace('-', ' ')} {family} models compared",
                "product_ids": "|".join(product["id"] for product in rows[:12]),
                "editorial_note": "Verify search intent, variants, facts and takeaways before approval.",
            }
        )
    candidates.sort(
        key=lambda row: (-row["score"], -row["complete_weight_price"], row["slug"])
    )
    return candidates[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()
    rows = build_candidates(args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    print(f"Wrote {len(rows)} review-only guide candidates to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
