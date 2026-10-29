#!/usr/bin/env python3
"""Build the review-only sample for a cold-weather sleeping-bag data asset."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = DATA / "reports" / "winter-sleeping-bag-candidate-sample.csv"
sys.path.insert(0, str(ROOT / "scripts"))

import build_sitemap

CELSIUS_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*°?C\b", re.IGNORECASE)
FAHRENHEIT_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*°?F\b", re.IGNORECASE)
MAX_COMFORT_C = 5.0
MAX_F_C_DIFFERENCE = 2.0


def parse_comfort_label(label: str) -> tuple[float | None, str]:
    celsius_match = CELSIUS_RE.search(label)
    fahrenheit_match = FAHRENHEIT_RE.search(label)
    if not celsius_match:
        return None, "missing_celsius"
    celsius = float(celsius_match.group(1))
    if fahrenheit_match:
        fahrenheit_c = (float(fahrenheit_match.group(1)) - 32) * 5 / 9
        if abs(fahrenheit_c - celsius) > MAX_F_C_DIFFERENCE:
            return celsius, "temperature_mismatch"
    return celsius, ""


def build_rows(products: list[dict], brands: dict[str, dict]) -> list[dict]:
    rows = []
    for product in products:
        if product.get("category") != "sleeping-bag":
            continue
        specs = product.get("specs") or {}
        comfort_label = str(specs.get("comfortTemp") or "").strip()
        if not comfort_label:
            continue

        comfort_c, reason = parse_comfort_label(comfort_label)
        weight = build_sitemap.parse_weight_kg(product)
        price = build_sitemap.parse_price(product)
        if not reason and (weight is None or weight <= 0):
            reason = "missing_weight"
        if not reason and (price is None or price <= 0):
            reason = "missing_price"
        if not reason and not product.get("sourceUrl"):
            reason = "missing_source"
        if not reason and comfort_c is not None and comfort_c > MAX_COMFORT_C:
            reason = "above_5c_scope"

        brand_id = str(product.get("brandId") or "")
        rows.append(
            {
                "product_id": product.get("id", ""),
                "brand": build_sitemap.brand_display_name(
                    brands.get(brand_id), brand_id
                ),
                "model": product.get("model", ""),
                "comfort_label": comfort_label,
                "comfort_c": "" if comfort_c is None else comfort_c,
                "lower_limit_label": specs.get("lowerLimitTemp", ""),
                "weight_kg": "" if weight is None else weight,
                "reference_price": "" if price is None else price,
                "currency": str(product.get("currency") or "USD").upper(),
                "catalog_status": product.get("status", ""),
                "official_source": product.get("sourceUrl", ""),
                "eligibility": "eligible" if not reason else "excluded",
                "exclusion_reason": reason,
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            row["eligibility"] != "eligible",
            float(row["comfort_c"]) if row["comfort_c"] != "" else 999,
            row["brand"],
            row["model"],
        ),
    )


def write_sample(rows: list[dict], output: Path = OUTPUT) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    products = build_sitemap.load_official_products()
    brands_data = build_sitemap.load_json(DATA / "brands.json")
    brands = build_sitemap.brand_map(
        brands_data if isinstance(brands_data, list) else []
    )
    rows = build_rows(products, brands)
    write_sample(rows)
    eligible = [row for row in rows if row["eligibility"] == "eligible"]
    reasons = Counter(row["exclusion_reason"] for row in rows if row["exclusion_reason"])
    print(
        f"Wrote {OUTPUT}: {len(rows)} temperature-labelled records, "
        f"{len(eligible)} eligible; exclusions={dict(sorted(reasons.items()))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
