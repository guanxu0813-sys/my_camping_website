#!/usr/bin/env python3
"""Notify Google Indexing API about URL updates (see docs/gsc-indexing-api-setup.md)."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
SEO_PATH = ROOT / "data" / "seo.json"
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPE = "https://www.googleapis.com/auth/indexing"
SKIP_FILES = frozenset({"other.html", "etc.html"})


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


def get_access_token() -> str:
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency. Install: pip install google-auth google-auth-oauthlib requests"
        ) from exc

    creds_path = __import__("os").environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path or not Path(creds_path).is_file():
        raise SystemExit(
            "Set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON path.\n"
            "See docs/gsc-indexing-api-setup.md"
        )

    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=[SCOPE]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token


def publish_url(url: str, token: str, dry_run: bool) -> int:
    if dry_run:
        print(f"[dry-run] URL_UPDATED {url}")
        return 0

    import requests

    resp = requests.post(
        INDEXING_ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"url": url, "type": "URL_UPDATED"},
        timeout=30,
    )
    if resp.status_code == 200:
        print(f"OK  {url}")
        return 0
    print(f"ERR {resp.status_code} {url} — {resp.text[:200]}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs to Google Indexing API")
    parser.add_argument("--url", action="append", dest="urls", help="Submit specific URL(s)")
    parser.add_argument("--dry-run", action="store_true", help="Print URLs only, no API calls")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds between requests")
    args = parser.parse_args()

    if args.urls:
        targets = args.urls
    else:
        _, targets = load_pages()

    if not targets:
        print("No URLs to submit.", file=sys.stderr)
        return 1

    token = None
    if not args.dry_run:
        token = get_access_token()

    errors = 0
    for i, url in enumerate(targets):
        errors += publish_url(url, token or "", args.dry_run)
        if not args.dry_run and i + 1 < len(targets):
            time.sleep(args.delay)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
