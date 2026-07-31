#!/usr/bin/env python3
"""Validate official catalog records and produce a prioritized quality audit."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = ROOT / "data" / "official"
BRANDS_PATH = ROOT / "data" / "brands.json"
PRIORITY_PATH = ROOT / "data" / "gsc-priority-urls.json"

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
    {
        "tent",
        "tarp",
        "sleeping-bag",
        "sleeping-pad",
        "stove",
        "backpack",
        "table",
        "chair",
        "other",
    }
)
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
ACCESSORY_PATTERN = re.compile(
    r"\b(footprint|groundsheet|inner tent|replacement|spare part|repair kit|"
    r"stuff sack|storage bag|pump sack|pole set|pole kit|tent pole|"
    r"stake set|peg set|tent pegs?|tent stakes?|rainfly only|fly only|liner)\b",
    re.IGNORECASE,
)
WEIGHT_RANGES = {
    "tent": (0.2, 30),
    "tarp": (0.05, 20),
    "sleeping-bag": (0.1, 10),
    "sleeping-pad": (0.05, 10),
    "stove": (0.005, 10),
    "backpack": (0.1, 10),
    "table": (0.1, 30),
    "chair": (0.1, 30),
}
REPORT_FIELDS = [
    "priority",
    "risk_score",
    "id",
    "brand_id",
    "category",
    "model",
    "issues",
    "source_url",
]


def numeric_value(product: dict, key: str) -> float | None:
    value = product.get(key)
    if value is None and isinstance(product.get("specs"), dict):
        value = product["specs"].get(key)
    return float(value) if isinstance(value, (int, float)) else None


def capacity_value(product: dict) -> int | None:
    value = product.get("capacity")
    if value is None and isinstance(product.get("specs"), dict):
        value = product["specs"].get("capacity")
    match = re.search(r"\d+", str(value or ""))
    return int(match.group()) if match else None


def normalized_model(product: dict) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(product.get("model") or "").lower()).strip()


def priority_ids() -> dict[str, int]:
    if not PRIORITY_PATH.exists():
        return {}
    data = json.loads(PRIORITY_PATH.read_text(encoding="utf-8"))
    urls = data.get("urls", []) if isinstance(data, dict) else []
    return {
        Path(str(url).split("?", 1)[0]).stem: index
        for index, url in enumerate(urls, start=1)
        if "/products/" in str(url)
    }


def quality_issues(product: dict) -> list[tuple[int, str]]:
    issues: list[tuple[int, str]] = []
    category = product.get("category")
    model = str(product.get("model") or "")
    weight = numeric_value(product, "weightKg")
    price_min = numeric_value(product, "priceMin")
    price = numeric_value(product, "price")
    price_value = price_min if price_min is not None else price
    price_max = numeric_value(product, "priceMax")
    currency = product.get("currency")

    if weight is None:
        issues.append((2, "missing weight"))
    elif category in WEIGHT_RANGES:
        low, high = WEIGHT_RANGES[category]
        if not low <= weight <= high:
            issues.append((4, f"suspicious weight {weight:g} kg"))
    if category == "tent" and (capacity_value(product) or 0) >= 3 and weight is not None and weight < 0.8:
        issues.append((4, "3+ person tent below 0.8 kg; verify variant"))

    if price_value is None:
        issues.append((1, "missing price"))
    elif price_value <= 0:
        issues.append((4, "non-positive price"))
    if price_min is not None and price_max is not None and price_max < price_min:
        issues.append((4, "priceMax below priceMin"))
    if price_value is not None and (not isinstance(currency, str) or not CURRENCY_PATTERN.match(currency)):
        issues.append((3, "missing or invalid ISO currency"))

    if not str(product.get("description") or "").strip():
        issues.append((1, "missing description"))
    is_tent_bundle = re.search(r"\btent\s*&\s*footprint\b", model, re.IGNORECASE)
    if ACCESSORY_PATTERN.search(model) and not is_tent_bundle:
        score = 4 if product.get("inSummaryTable") is not False else 2
        issues.append((score, "accessory candidate; review indexability"))
    if not str(product.get("sourceUrl") or "").startswith("https://"):
        issues.append((4, "source URL is not HTTPS"))
    return issues


def write_report(rows: list[dict], destination: Path, limit: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(rows[:limit])
    print(f"Wrote quality audit: {destination} ({min(limit, len(rows))} rows)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quality-report", type=Path, help="Write prioritized audit CSV")
    parser.add_argument("--limit", type=int, default=100, help="Audit row limit")
    parser.add_argument(
        "--strict-quality",
        action="store_true",
        help="Fail when any non-fatal quality warning remains",
    )
    args = parser.parse_args(argv)

    brand_ids = {b["id"] for b in json.loads(BRANDS_PATH.read_text(encoding="utf-8"))}
    priorities = priority_ids()
    errors: list[str] = []
    warnings: list[str] = []
    report_rows: list[dict] = []
    duplicate_models: dict[tuple[str, str, str], list[str]] = defaultdict(list)

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
        for index, product in enumerate(products):
            prefix = f"{products_path}[{index}]"
            if not isinstance(product, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            missing = REQUIRED - product.keys()
            if missing:
                errors.append(f"{prefix}: missing fields {sorted(missing)}")
                continue

            product_id = product["id"]
            if product_id in seen_ids:
                errors.append(f"{prefix}: duplicate id {product_id!r}")
            seen_ids.add(product_id)
            if not ID_PATTERN.match(product_id):
                errors.append(f"{prefix}: invalid id {product_id!r}")
            if product["brandId"] not in brand_ids:
                errors.append(f"{prefix}: unknown brandId {product['brandId']!r}")
            if product["brandId"] != brand_dir and brand_dir != "_manifest":
                errors.append(
                    f"{prefix}: brandId {product['brandId']!r} != directory {brand_dir!r}"
                )
            if product["category"] not in VALID_CATEGORY:
                errors.append(f"{prefix}: invalid category {product['category']!r}")
            if product["status"] not in VALID_STATUS:
                errors.append(f"{prefix}: invalid status {product['status']!r}")

            key = (product["brandId"], product["category"], normalized_model(product))
            duplicate_models[key].append(product_id)
            issues = quality_issues(product)
            if issues:
                warnings.extend(f"{product_id}: {message}" for _, message in issues)
            report_rows.append(
                {
                    "priority": priorities.get(product_id, ""),
                    "risk_score": sum(score for score, _ in issues),
                    "id": product_id,
                    "brand_id": product["brandId"],
                    "category": product["category"],
                    "model": product["model"],
                    "issues": "; ".join(message for _, message in issues) or "no issue detected",
                    "source_url": product["sourceUrl"],
                }
            )
        print(f"OK {products_path} ({len(products)} products)")

    for (brand_id, category, model), ids in duplicate_models.items():
        if model and len(ids) > 1:
            warning = f"{brand_id}/{category}: duplicate normalized model {model!r}: {ids}"
            warnings.append(warning)
            for row in report_rows:
                if row["id"] in ids:
                    row["risk_score"] += 2
                    row["issues"] += "; duplicate normalized model"

    manifest_path = OFFICIAL / "_manifest.json"
    if manifest_path.exists():
        json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"OK {manifest_path}")

    report_rows.sort(
        key=lambda row: (
            row["priority"] == "",
            row["priority"] if row["priority"] != "" else 999999,
            -int(row["risk_score"]),
            row["id"],
        )
    )
    if args.quality_report:
        write_report(report_rows, args.quality_report, args.limit)

    print(f"Quality warnings: {len(warnings)} across {len(report_rows)} products")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if args.strict_quality and warnings:
        print("\n".join(warnings), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
