#!/usr/bin/env python3
"""Scrape official brand catalogs into data/official/{brandId}/products.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    BROWSER_USER_AGENT,
    OFFICIAL_DIR,
    RateLimiter,
    USER_AGENT,
    classify_furniture,
    fetch_shopify_all_products,
    fetch_shopify_collection_products,
    load_config,
    matches_filter,
    normalize_shopify_product,
    read_json,
    update_manifest,
    write_json,
)


def resolve_user_agent(cfg: dict) -> str:
    if cfg.get("useBrowserUserAgent"):
        return BROWSER_USER_AGENT
    return cfg.get("userAgent") or USER_AGENT


def scrape_shopify_brand(brand_key: str, cfg: dict) -> int:
    limiter = RateLimiter(float(cfg.get("rateLimitSeconds", 1.0)))
    user_agent = resolve_user_agent(cfg)
    base_url = cfg["baseUrl"]
    brand_id = cfg["brandId"]
    by_handle: dict[str, dict] = {}
    errors: list[str] = []

    for collection in cfg.get("collections") or []:
        handle = collection["handle"]
        category = collection.get("category")
        subcategory = collection.get("subcategory")
        try:
            raw_products = fetch_shopify_collection_products(
                base_url, handle, limiter, user_agent=user_agent
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(f"collection {handle}: {exc}")
            continue
        for product in raw_products:
            title_lower = (product.get("title") or "").lower()
            skip = False
            for bad in collection.get("excludeTitleKeywords") or []:
                if bad.lower() in title_lower:
                    skip = True
                    break
            if skip:
                continue
            if collection.get("classifyFurniture"):
                furniture_cat = classify_furniture(product)
                if not furniture_cat:
                    continue
                category = furniture_cat
            elif not category:
                continue
            item = normalize_shopify_product(
                product,
                brand_id=brand_id,
                source_site=cfg["sourceSite"],
                base_url=base_url,
                category=category,
                subcategory=subcategory,
                currency=cfg.get("currency", "USD"),
            )
            by_handle[item["id"]] = item

    filters = cfg.get("allProductsFilters") or []
    all_products_failed = False
    if filters:
        try:
            all_products = fetch_shopify_all_products(base_url, limiter, user_agent=user_agent)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"all_products: {exc}")
            all_products = []
            all_products_failed = True
        for flt in filters:
            category = flt["category"]
            for product in all_products:
                if not matches_filter(product, flt):
                    continue
                item = normalize_shopify_product(
                    product,
                    brand_id=brand_id,
                    source_site=cfg["sourceSite"],
                    base_url=base_url,
                    category=category,
                    subcategory=flt.get("subcategory", category),
                    currency=cfg.get("currency", "USD"),
                )
                by_handle[item["id"]] = item

    out_path = OFFICIAL_DIR / brand_id / "products.json"
    if all_products_failed and filters and out_path.exists():
        filter_categories = {flt["category"] for flt in filters}
        for item in read_json(out_path):
            if item.get("category") in filter_categories and item.get("id") not in by_handle:
                by_handle[item["id"]] = item

    products = sorted(by_handle.values(), key=lambda p: p["model"].lower())
    if not products and errors:
        print(f"Skipped write to {out_path}: 0 products and {len(errors)} error(s)", file=sys.stderr)
        if out_path.exists():
            existing = read_json(out_path)
            print(f"Keeping existing file ({len(existing)} products)", file=sys.stderr)
        update_manifest(brand_id, 0, errors)
        return 0
    write_json(out_path, products)
    update_manifest(brand_id, len(products), errors)
    print(f"Wrote {out_path} ({len(products)} products)")
    if errors:
        print("Warnings:", "; ".join(errors), file=sys.stderr)
    return len(products)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape official brand product catalogs")
    parser.add_argument("brand", help="Brand key from config.yaml (e.g. naturehike, snow-peak)")
    args = parser.parse_args()

    brands = load_config()
    if args.brand not in brands:
        print(f"Unknown brand {args.brand!r}. Available: {', '.join(brands)}", file=sys.stderr)
        return 1

    cfg = brands[args.brand]
    adapter = cfg.get("adapter", "shopify")
    if adapter != "shopify":
        print(f"Unsupported adapter {adapter!r}", file=sys.stderr)
        return 1

    scrape_shopify_brand(args.brand, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
