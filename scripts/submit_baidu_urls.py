#!/usr/bin/env python3
"""Push URLs to Baidu ordinary indexing API (see docs/baidu-setup-campgearcompare.md)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
SEO_PATH = ROOT / "data" / "seo.json"
BAIDU_API = "http://data.zz.baidu.com/urls"
SKIP_FILES = frozenset({"other.html", "etc.html"})
MAX_URLS_PER_REQUEST = 2000


def load_pages() -> tuple[str, list[str]]:
    seo = json.loads(SEO_PATH.read_text(encoding="utf-8"))
    base = seo["siteUrl"].rstrip("/") + "/"
    urls: list[str] = []
    for page in seo.get("pages", []):
        file_name = page.get("file", "")
        if file_name in SKIP_FILES:
            continue
        path = page.get("path", "/")
        urls.append(urljoin(base, path.lstrip("/")))
    return base, urls


def baidu_site_domain(seo: dict) -> str:
    explicit = seo.get("baiduSite", "").strip()
    if explicit:
        return explicit.lstrip("https://").lstrip("http://").rstrip("/")
    host = urlparse(seo["siteUrl"]).netloc
    if not host:
        raise SystemExit(f"{SEO_PATH}: cannot derive baiduSite from siteUrl")
    return host


def push_urls(urls: list[str], site: str, token: str, dry_run: bool) -> int:
    if not urls:
        print("No URLs to submit.", file=sys.stderr)
        return 1

    if dry_run:
        print(f"[dry-run] site={site} count={len(urls)}")
        for url in urls:
            print(f"  {url}")
        return 0

    try:
        import requests
    except ImportError as exc:
        raise SystemExit("Missing dependency. Install: pip install requests") from exc

    errors = 0
    for i in range(0, len(urls), MAX_URLS_PER_REQUEST):
        batch = urls[i : i + MAX_URLS_PER_REQUEST]
        resp = requests.post(
            BAIDU_API,
            params={"site": site, "token": token},
            data="\n".join(batch).encode("utf-8"),
            headers={"Content-Type": "text/plain"},
            timeout=30,
        )
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text[:300]}

        if resp.status_code == 200 and body.get("success"):
            print(f"OK  pushed {body.get('success', len(batch))} URL(s)")
            remain = body.get("remain")
            if remain is not None:
                print(f"    remain quota today: {remain}")
        else:
            errors += 1
            print(
                f"ERR {resp.status_code} site={site} — {body}",
                file=sys.stderr,
            )
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs to Baidu indexing API")
    parser.add_argument("--url", action="append", dest="urls", help="Submit specific URL(s)")
    parser.add_argument("--dry-run", action="store_true", help="Print URLs only, no API calls")
    args = parser.parse_args()

    seo = json.loads(SEO_PATH.read_text(encoding="utf-8"))
    site = baidu_site_domain(seo)

    if args.urls:
        targets = args.urls
    else:
        _, targets = load_pages()

    token = os.environ.get("BAIDU_PUSH_TOKEN", "").strip()
    if not args.dry_run and not token:
        raise SystemExit(
            "Set BAIDU_PUSH_TOKEN (from ziyuan.baidu.com → 普通收录 → API提交).\n"
            "See docs/baidu-setup-campgearcompare.md"
        )

    return push_urls(targets, site, token, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
