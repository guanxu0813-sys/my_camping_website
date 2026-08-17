# Day 37: GSC high-value URL inspection

Inspection date: 2026-08-17
GSC report updated: 2026-08-14

## Coverage snapshot

- Indexed: 724
- Not indexed: 168 across 5 reasons
- Crawled, currently not indexed: 8
- Discovered, currently not indexed: 153
- Alternate page with proper canonical: 1
- Duplicate, Google chose a different canonical: 1
- Noindex exclusions: 5

## Ten inspected URLs

| URL | GSC state | Last crawl | Decision |
|---|---|---:|---|
| `/index.html` | Alternate page with proper canonical | 2026-08-07 | Expected: canonical points to `/`; no action. |
| `/legal.html` | Google chose a different canonical | 2026-07-09 | Fix: redirect the old Vercel host to the production host, then wait for recrawl. |
| `/products/big-agnes-sarvis-vst-3.html` | Crawled, not indexed | 2026-08-14 | Keep indexable; manually normalize the draft record before requesting indexing. |
| `/products/naturehike-cloud-up-ul-1-person-ultralight-backpacking-tent.html` | Crawled, not indexed | 2026-08-14 | Keep indexable; it has complete specs and now belongs to a stronger internal-link cluster. Wait for recrawl. |
| `/products/nanga-aurora-tex-light-450dx-1.html` | Crawled, not indexed | 2026-07-26 | Hold indexing request; translate and normalize the Japanese draft content first. |
| `/products/nanga-mat-compatible-bag.html` | Crawled, not indexed | 2026-07-25 | Hold indexing request; translate and normalize the Japanese draft content first. |
| `/products/nanga-aurora-tex-light-350-dx-1.html` | Crawled, not indexed | 2026-07-25 | Hold indexing request; translate and normalize the Japanese draft content first. |
| `/products/nanga-aurora-tex-light-350-spdx-2019.html` | Crawled, not indexed | 2026-07-20 | Hold indexing request; verify whether the legacy `2019` variant still deserves a standalone page. |
| `/products/nanga-level8-10-udd-bag.html` | Crawled, not indexed | 2026-07-17 | Hold indexing request; add normalized English weight and temperature context first. |
| `/products/nanga-level8-13-aurora-tex-light.html` | Crawled, not indexed | 2026-07-12 | Hold indexing request; add normalized English weight and temperature context first. |

## Canonical finding and fix

URL Inspection showed that `/legal.html` declares `https://www.campgearcompare.com/legal.html`, while Google selected `https://my-camping-website.vercel.app/legal.html`. A permanent host redirect was added in `vercel.json` so every old Vercel URL resolves to the matching production URL.

## Next check

- Deploy the redirect, then verify the old-domain response is a permanent redirect.
- Recheck `/legal.html` in GSC after Google recrawls it; do not submit all 10 URLs in bulk.
- Treat the six NANGA pages as one editorial-quality cluster before any indexing requests.
