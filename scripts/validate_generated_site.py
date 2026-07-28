#!/usr/bin/env python3
"""Validate generated HTML links, sitemaps, feeds and SEO essentials."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import build_sitemap

ROOT = Path(__file__).resolve().parent.parent
SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.canonical = ""
        self.title = ""
        self.in_title = False
        self.schemas: list[str] = []
        self.in_schema = False
        self.schema_parts: list[str] = []
        self.has_script = False
        self.robots = ""
        self.main_nav = ""
        self.in_main_nav = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href") or ""
        if tag == "meta" and values.get("name") == "robots":
            self.robots = values.get("content") or ""
        if tag == "title":
            self.in_title = True
        if tag == "script" and values.get("type") == "application/ld+json":
            self.in_schema = True
            self.schema_parts = []
        if tag == "script" and values.get("src") == "/script.js":
            self.has_script = True
        if tag == "ul" and "nav__links--categories" in (values.get("class") or ""):
            self.in_main_nav = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_schema:
            self.schemas.append("".join(self.schema_parts))
            self.in_schema = False
        if tag == "ul" and self.in_main_nav:
            self.in_main_nav = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.in_schema:
            self.schema_parts.append(data)
        if self.in_main_nav:
            self.main_nav += data


def local_target(source: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:", "#", "javascript:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    target = ROOT / path.lstrip("/") if path.startswith("/") else source.parent / path
    if path.endswith("/"):
        target /= "index.html"
    return target


def main() -> int:
    errors: list[str] = []
    html_files = list(ROOT.rglob("*.html"))
    for path in html_files:
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        parser = DocumentParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        for href in parser.hrefs:
            target = local_target(path, href)
            if target is not None and not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link target {href}")
        for schema in parser.schemas:
            try:
                json.loads(schema)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid JSON-LD: {exc}")
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith(("products/", "brands/", "guides/")):
            if not parser.title or not parser.canonical:
                errors.append(f"{relative}: missing title or canonical")
            if not parser.has_script:
                errors.append(f"{relative}: missing /script.js")
        if relative in {"index.html", "tent.html", "tarp.html"} and "Guides" not in parser.main_nav:
            errors.append(f"{relative}: main navigation missing Guides")

    all_urls: list[str] = []
    for name in ("sitemap-core.xml", "sitemap-brands.xml", "sitemap-products.xml"):
        root = ET.parse(ROOT / name).getroot()
        urls = [
            node.text.strip()
            for node in root.findall("s:url/s:loc", SITEMAP_NS)
            if node.text
        ]
        if len(urls) != len(set(urls)):
            errors.append(f"{name}: duplicate URL")
        all_urls.extend(urls)
    if len(all_urls) != len(set(all_urls)):
        errors.append("duplicate URL across child sitemaps")
    ET.parse(ROOT / "feed.xml")

    for product in build_sitemap.load_official_products():
        if not build_sitemap.is_low_value_accessory(product):
            continue
        product_file = ROOT / build_sitemap.product_path(product).lstrip("/")
        if not product_file.exists():
            errors.append(f"accessory fallback page missing: {product_file.relative_to(ROOT)}")
            continue
        parser = DocumentParser()
        parser.feed(product_file.read_text(encoding="utf-8", errors="replace"))
        if "noindex" not in parser.robots:
            errors.append(f"accessory page is indexable: {product_file.relative_to(ROOT)}")
        url = f"https://www.campgearcompare.com{build_sitemap.product_path(product)}"
        if url in all_urls:
            errors.append(f"accessory page appears in sitemap: {url}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"OK generated site: {len(html_files)} HTML files, "
        f"{len(all_urls)} unique sitemap URLs, valid RSS and internal links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
