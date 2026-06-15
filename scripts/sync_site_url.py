#!/usr/bin/env python3
"""Sync siteUrl from data/seo.json to HTML canonicals, sitemap, robots, and docs."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEO_PATH = ROOT / "data" / "seo.json"
CANONICAL_RE = re.compile(
    r'(<link rel="canonical" href=")[^"]+(")',
    re.IGNORECASE,
)
VERCEL_URL = "https://my-camping-website.vercel.app"


def load_site_url() -> str:
    seo = json.loads(SEO_PATH.read_text(encoding="utf-8"))
    site_url = seo.get("siteUrl", "").rstrip("/")
    if not site_url:
        raise SystemExit(f"{SEO_PATH}: missing siteUrl")
    return site_url


def canonical_for_file(site_url: str, path: Path) -> str:
    name = path.name
    if name == "index.html":
        return f"{site_url}/"
    return f"{site_url}/{name}"


def sync_html(site_url: str) -> list[str]:
    updated: list[str] = []
    for html in sorted(ROOT.glob("*.html")):
        if html.name.startswith("google"):
            continue
        text = html.read_text(encoding="utf-8")
        canonical = canonical_for_file(site_url, html)
        new_text, count = CANONICAL_RE.subn(rf'\1{canonical}\2', text, count=1)
        if count:
            html.write_text(new_text, encoding="utf-8")
            updated.append(html.name)
    return updated


def sync_docs(site_url: str, old_url: str) -> list[str]:
    updated: list[str] = []
    docs = ROOT / "docs"
    if not docs.exists():
        return updated
    for md in docs.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if old_url not in text and site_url not in text:
            continue
        new_text = text.replace(old_url, site_url)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            updated.append(str(md.relative_to(ROOT)))
    return updated


def main() -> int:
    site_url = load_site_url()
    old_url = VERCEL_URL
    if len(sys.argv) > 1:
        old_url = sys.argv[1].rstrip("/")

    html_files = sync_html(site_url)
    doc_files = sync_docs(site_url, old_url)

    build = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_sitemap.py")],
        check=False,
    )
    if build.returncode != 0:
        return build.returncode

    print(f"siteUrl: {site_url}")
    if html_files:
        print("Updated canonical:", ", ".join(html_files))
    else:
        print("No HTML canonical changes")
    if doc_files:
        print("Updated docs:", ", ".join(doc_files))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
