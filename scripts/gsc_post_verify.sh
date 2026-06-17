#!/usr/bin/env bash
# Post-GSC-verification: ping sitemaps + print indexing URLs for manual GSC submission.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_URL="$(python3 -c "import json; print(json.load(open('$ROOT/data/seo.json'))['siteUrl'].rstrip('/'))")"
SITEMAP="$SITE_URL/sitemap.xml"

echo "Site: $SITE_URL"
echo "Sitemap: $SITEMAP"
echo ""

echo "=== Bing sitemap ping ==="
bing_code=$(curl -s -o /dev/null -w "%{http_code}" "https://www.bing.com/ping?sitemap=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITEMAP', safe=''))")")
echo "HTTP $bing_code (200 = accepted)"

echo ""
echo "=== GSC: submit sitemap manually ==="
echo "  Search Console → 站点地图 → 添加: sitemap.xml"
echo ""
echo "=== GSC: request indexing (网址检查) ==="
python3 << PY
import json
from pathlib import Path
seo = json.loads(Path("$ROOT/data/seo.json").read_text())
base = seo["siteUrl"].rstrip("/")
for p in seo["pages"]:
    path = p["path"]
    if path in ("/other.html", "/etc.html"):
        continue
    file = p.get("file", "")
    if file in ("other.html", "etc.html"):
        continue
    print(f"  {base}{path if path != '/' else '/'}")
PY

echo ""
echo "=== Live checks ==="
bash "$ROOT/scripts/check_site_seo.sh" "$SITE_URL"
