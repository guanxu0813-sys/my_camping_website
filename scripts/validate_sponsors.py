#!/usr/bin/env python3
"""Validate data/sponsors.json campaigns against official product ids."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPONSORS_PATH = ROOT / "data" / "sponsors.json"
OFFICIAL = ROOT / "data" / "official"
VALID_TIERS = frozenset({"table-featured", "modal-featured", "featured"})
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_product_ids() -> set[str]:
    ids: set[str] = set()
    for products_path in OFFICIAL.glob("*/products.json"):
        products = json.loads(products_path.read_text(encoding="utf-8"))
        if not isinstance(products, list):
            continue
        for p in products:
            if isinstance(p, dict) and p.get("id"):
                ids.add(p["id"])
    return ids


def main() -> int:
    if not SPONSORS_PATH.exists():
        print(f"OK {SPONSORS_PATH} (missing, optional)")
        return 0

    data = json.loads(SPONSORS_PATH.read_text(encoding="utf-8"))
    campaigns = data.get("campaigns")
    if not isinstance(campaigns, list):
        print(f"{SPONSORS_PATH}: campaigns must be an array", file=__import__("sys").stderr)
        return 1

    product_ids = load_product_ids()
    errors: list[str] = []
    seen_campaigns: set[str] = set()

    for i, c in enumerate(campaigns):
        prefix = f"{SPONSORS_PATH} campaigns[{i}]"
        if not isinstance(c, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        product_id = c.get("productId")
        if not product_id:
            errors.append(f"{prefix}: missing productId")
            continue
        if product_id not in product_ids:
            errors.append(f"{prefix}: unknown productId {product_id!r}")
        tier = c.get("tier", "table-featured")
        if tier not in VALID_TIERS:
            errors.append(f"{prefix}: invalid tier {tier!r}")
        expires = c.get("expiresAt")
        if expires is not None:
            if not isinstance(expires, str) or not DATE_PATTERN.match(expires):
                errors.append(f"{prefix}: expiresAt must be YYYY-MM-DD")
            else:
                date.fromisoformat(expires)
        campaign_id = c.get("campaignId")
        if campaign_id:
            if campaign_id in seen_campaigns:
                errors.append(f"{prefix}: duplicate campaignId {campaign_id!r}")
            seen_campaigns.add(campaign_id)

    if errors:
        print("\n".join(errors), file=__import__("sys").stderr)
        return 1

    active = sum(1 for c in campaigns if isinstance(c, dict) and c.get("active") is True)
    print(f"OK {SPONSORS_PATH} ({len(campaigns)} campaigns, {active} active)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
