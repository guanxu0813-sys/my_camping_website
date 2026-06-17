#!/usr/bin/env bash
# Smoke-test SEO URLs for production domain (read-only).
set -euo pipefail
BASE="${1:-https://campgearcompare.com}"
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

echo "--- done ---"
