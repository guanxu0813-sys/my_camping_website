#!/usr/bin/env python3
"""Generate robots.txt and sitemap.xml from data/seo.json."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEO_PATH = ROOT / "data" / "seo.json"


def main() -> int:
    seo = json.loads(SEO_PATH.read_text(encoding="utf-8"))
    site_url = seo["siteUrl"].rstrip("/")
    lastmod = date.today().isoformat()

    url_entries = []
    for page in seo["pages"]:
        loc = f"{site_url}{page['path']}"
        url_entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{page['changefreq']}</changefreq>\n"
            f"    <priority>{page['priority']}</priority>\n"
            "  </url>"
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {site_url}/sitemap.xml\n"
    )
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")

    print(f"Wrote sitemap.xml and robots.txt for {site_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
