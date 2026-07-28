#!/usr/bin/env python3
"""Notify IndexNow about changed public HTML URLs."""

from __future__ import annotations

import argparse
import json
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SEO_PATH = ROOT / "data" / "seo.json"
KEY_FILE = "indexnow-key.txt"
ENDPOINT = "https://api.indexnow.org/IndexNow"
SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
EXCLUDED_HTML = frozenset(
    {
        "404.html",
        "etc.html",
        "google552523522ea8ca31.html",
        "baidu_verify_codeva-VQKdFWFhmk.html",
    }
)


def site_url() -> str:
    seo = json.loads(SEO_PATH.read_text(encoding="utf-8"))
    return seo["siteUrl"].rstrip("/")


def key_value() -> str:
    path = ROOT / KEY_FILE
    if not path.exists():
        raise SystemExit(f"Missing IndexNow key file: {path}")
    value = path.read_text(encoding="utf-8").strip()
    if not (8 <= len(value) <= 128) or not value.replace("-", "").isalnum():
        raise SystemExit(f"Invalid IndexNow key in {path}")
    return value


def html_path_to_url(file_name: str, base: str) -> str | None:
    normalized = file_name.strip().replace("\\", "/").lstrip("./")
    if not normalized.endswith(".html"):
        return None
    if Path(normalized).name in EXCLUDED_HTML:
        return None
    if normalized == "index.html":
        return f"{base}/"
    if normalized.endswith("/index.html"):
        return f"{base}/{normalized[:-10]}"
    return f"{base}/{normalized}"


def changed_files(before: str, after: str) -> list[str]:
    if not before or set(before) == {"0"}:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACDMRT", before, after],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        print(result.stderr.strip(), file=sys.stderr)
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def sitemap_urls(base: str) -> list[str]:
    urls: list[str] = []
    for name in ("sitemap-core.xml", "sitemap-brands.xml", "sitemap-products.xml"):
        path = ROOT / name
        if not path.exists():
            continue
        document = ET.parse(path).getroot()
        urls.extend(
            node.text.strip()
            for node in document.findall("s:url/s:loc", SITEMAP_NS)
            if node.text and node.text.strip().startswith(f"{base}/")
        )
    return urls


def normalize_targets(values: list[str], base: str) -> list[str]:
    expected_host = urlparse(base).netloc
    targets = []
    for value in values:
        parsed = urlparse(value)
        if parsed.scheme != "https" or parsed.netloc != expected_host:
            raise SystemExit(f"Refusing non-site URL: {value}")
        targets.append(value)
    return sorted(set(targets))


def submit(targets: list[str], base: str, key: str, dry_run: bool) -> int:
    if not targets:
        print("No changed public HTML URLs to submit.")
        return 0
    if dry_run:
        for url in targets:
            print(f"[dry-run] {url}")
        return 0

    payload = json.dumps(
        {
            "host": urlparse(base).netloc,
            "key": key,
            "keyLocation": f"{base}/{KEY_FILE}",
            "urlList": targets,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        print(f"IndexNow error {exc.code}: {exc.read().decode()[:300]}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, ssl.SSLCertVerificationError):
            fallback = subprocess.run(
                [
                    "curl",
                    "--fail",
                    "--silent",
                    "--show-error",
                    "--request",
                    "POST",
                    "--header",
                    "Content-Type: application/json; charset=utf-8",
                    "--data-binary",
                    payload.decode("utf-8"),
                    ENDPOINT,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if fallback.returncode == 0:
                print(f"IndexNow accepted {len(targets)} changed URL(s) via curl.")
                return 0
            print(f"IndexNow curl fallback failed: {fallback.stderr[:300]}", file=sys.stderr)
            return 1
        print(f"IndexNow request failed: {exc}", file=sys.stderr)
        return 1

    if status not in (200, 202):
        print(f"Unexpected IndexNow status: {status}", file=sys.stderr)
        return 1
    print(f"IndexNow accepted {len(targets)} changed URL(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", default=[], help="Specific site URL")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed repo path")
    parser.add_argument("--git-before", default="", help="Previous git SHA")
    parser.add_argument("--git-after", default="HEAD", help="Current git SHA")
    parser.add_argument("--all", action="store_true", help="Submit every sitemap URL")
    parser.add_argument("--dry-run", action="store_true", help="Print targets only")
    args = parser.parse_args()

    base = site_url()
    values = list(args.url)
    if args.all:
        values.extend(sitemap_urls(base))
    else:
        files = list(args.changed_file)
        if args.git_before:
            files.extend(changed_files(args.git_before, args.git_after))
        values.extend(
            url
            for file_name in files
            if (url := html_path_to_url(file_name, base)) is not None
        )
    targets = normalize_targets(values, base)
    return submit(targets, base, key_value(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
