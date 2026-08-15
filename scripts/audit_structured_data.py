#!/usr/bin/env python3
"""Audit representative generated pages for visible/JSON-LD consistency."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://www.campgearcompare.com"
REPORT_PATH = ROOT / "data" / "reports" / "growth-day36-structured-data-2026-08-15.json"
SAMPLES = [
    ("products/naturehike-mongartm-base-3-person-ultralight-backpacking-tent.html", ("Product", "BreadcrumbList")),
    ("products/naturehike-giling-protm-1-person-backpacking-tent.html", ("Product", "BreadcrumbList")),
    ("products/3f-ul-gear-lanshan-1-pro.html", ("Product", "BreadcrumbList")),
    ("products/big-agnes-tiger-wall-platinum-two-tent.html", ("Product", "BreadcrumbList")),
    ("guides/camping-gear-weight-price-report-2026.html", ("Article", "BreadcrumbList")),
    ("guides/naturehike-giling-pro-1-vs-mongar-pro-1.html", ("Article", "BreadcrumbList")),
    ("guides/fire-maple-fms-300t-vs-hornet-ii.html", ("Article", "BreadcrumbList")),
    ("guides/2-person-backpacking-tents-under-2kg.html", ("Article", "BreadcrumbList")),
    ("brands/naturehike-tent.html", ("CollectionPage", "BreadcrumbList")),
    ("tent.html", ("CollectionPage", "ItemList", "BreadcrumbList")),
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonical = ""
        self.h1 = ""
        self._h1_depth = 0
        self._h1_parts: list[str] = []
        self._json_ld = False
        self._json_parts: list[str] = []
        self.objects: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "link" and attr.get("rel") == "canonical":
            self.canonical = attr.get("href") or ""
        if tag == "h1":
            self._h1_depth = 1
        elif self._h1_depth:
            self._h1_depth += 1
        if tag == "script" and attr.get("type") == "application/ld+json":
            self._json_ld = True
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if self._h1_depth:
            self._h1_depth -= 1
            if tag == "h1":
                self.h1 = " ".join("".join(self._h1_parts).split())
                self._h1_parts = []
                self._h1_depth = 0
        if tag == "script" and self._json_ld:
            data = json.loads("".join(self._json_parts))
            self.objects.extend(data.get("@graph", [data]) if isinstance(data, dict) else data)
            self._json_ld = False

    def handle_data(self, data: str) -> None:
        if self._h1_depth:
            self._h1_parts.append(data)
        if self._json_ld:
            self._json_parts.append(data)


def has_forbidden_rating(value: object) -> bool:
    if isinstance(value, dict):
        if any(key in value for key in ("aggregateRating", "review", "ratingValue")):
            return True
        return any(has_forbidden_rating(item) for item in value.values())
    if isinstance(value, list):
        return any(has_forbidden_rating(item) for item in value)
    return False


def object_type(value: dict) -> str:
    raw = value.get("@type", "")
    return raw[0] if isinstance(raw, list) and raw else str(raw)


def names_are_consistent(h1: str, schema_name: str) -> bool:
    def normalize(value: str) -> set[str]:
        return {
            token[:-1] if token.endswith("s") and len(token) > 3 else token
            for token in re.findall(r"[a-z0-9]+", value.lower())
            if token not in {"a", "an", "the", "and", "by"}
        }

    h1_tokens = normalize(h1)
    schema_tokens = normalize(schema_name)
    return bool(h1_tokens) and len(h1_tokens & schema_tokens) / len(h1_tokens) >= 0.6


def audit_page(path: str, expected_types: tuple[str, ...]) -> dict:
    parser = PageParser()
    parser.feed((ROOT / path).read_text(encoding="utf-8"))
    canonical = f"{SITE_URL}/{path}"
    by_type = {object_type(item): item for item in parser.objects}
    issues: list[str] = []

    if parser.canonical != canonical:
        issues.append("canonical_mismatch")
    for expected in expected_types:
        if expected not in by_type:
            issues.append(f"missing_{expected}")
    if has_forbidden_rating(parser.objects):
        issues.append("unsupported_rating_or_review")

    product = by_type.get("Product")
    if product:
        if product.get("name") != parser.h1 or product.get("url") != canonical:
            issues.append("product_visible_content_mismatch")
        offer = product.get("offers", {})
        if not isinstance(offer.get("price"), (int, float)) or offer.get("price", 0) <= 0:
            issues.append("invalid_offer_price")
        if not re.fullmatch(r"[A-Z]{3}", str(offer.get("priceCurrency", ""))):
            issues.append("invalid_offer_currency")
        if urlparse(str(offer.get("url", ""))).scheme != "https":
            issues.append("invalid_offer_url")

    article = by_type.get("Article")
    if article:
        if not names_are_consistent(parser.h1, str(article.get("headline", ""))) or article.get("url") != canonical:
            issues.append("article_visible_content_mismatch")
        author = article.get("author", {})
        if author.get("@type") != "Organization" or author.get("name") != "CampGear Compare":
            issues.append("invalid_article_author")
        for field in ("datePublished", "dateModified"):
            if not re.match(r"^\d{4}-\d{2}-\d{2}", str(article.get(field, ""))):
                issues.append(f"invalid_{field}")

    breadcrumb = by_type.get("BreadcrumbList")
    if breadcrumb and len(breadcrumb.get("itemListElement", [])) < 2:
        issues.append("incomplete_breadcrumb")

    collection = by_type.get("CollectionPage")
    if collection and (
        not names_are_consistent(parser.h1, str(collection.get("name", "")))
        or collection.get("url") != canonical
    ):
        issues.append("collection_visible_content_mismatch")

    return {
        "path": path,
        "h1": parser.h1,
        "canonical": parser.canonical,
        "types": sorted(by_type),
        "expectedTypes": list(expected_types),
        "issues": issues,
        "result": "pass" if not issues else "fail",
    }


def main() -> int:
    pages = [audit_page(path, expected) for path, expected in SAMPLES]
    report = {
        "generated": "2026-08-15",
        "sampleSize": len(pages),
        "passed": sum(page["result"] == "pass" for page in pages),
        "failed": sum(page["result"] == "fail" for page in pages),
        "pages": pages,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("sampleSize", "passed", "failed")}))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
