#!/usr/bin/env bash
# Smoke-test SEO URLs for production domain (read-only).
set -euo pipefail
BASE="${1:-https://www.campgearcompare.com}"
BASE="${BASE%/}"

echo "=== $BASE ==="
code_root=$(curl -sI -o /dev/null -w "%{http_code}" "$BASE/")
echo "GET / -> HTTP $code_root"

echo "--- sitemap (first 3 loc) ---"
curl -s "$BASE/sitemap.xml" | grep -m3 '<loc>' || true

echo "--- robots ---"
curl -s "$BASE/robots.txt"

echo "--- canonical tent.html ---"
curl -s "$BASE/tent.html" | grep -o 'rel="canonical" href="[^"]*"' || true

echo "--- og:title tent.html ---"
curl -s "$BASE/tent.html" | grep -o 'property="og:title" content="[^"]*"' || true

echo "--- JSON-LD tent.html ---"
curl -s "$BASE/tent.html" | grep -o 'application/ld+json' | head -1 || true

echo "--- seo crawl paragraph tent.html ---"
curl -s "$BASE/tent.html" | grep -o 'class="seo-crawl"[^>]*>[^<]*' | head -1 || true

echo "--- done ---"
