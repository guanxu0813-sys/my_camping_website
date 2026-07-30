# Day 3 GSC Priority Analysis

Date: 2026-07-31

## Inputs Reviewed

- `docs/growth-metrics.csv`: baseline row has 16 GSC clicks, 879 impressions, 1.82% CTR, 15.28 average position, 453 indexed URLs, 14 published guides.
- `docs/growth-status.md`: M1 decision is `BASELINE`; collect seven complete GA4 days before applying the traffic gate.
- `docs/gsc-indexing-log.csv`: GSC child sitemap discovery is 26 core / 66 brands / 769 products; Bing sitemap submission is successful; IndexNow key and manual submit are verified.
- `data/gsc-priority-urls.json`: 2026-07-28 GSC performance export lists 6 product URLs with search signal.
- `data/reports/guide-candidates.csv`: review-only guide candidates are available; they must be verified before approval.

## Data Limitation

The repository does not contain the full past-28-day GSC query/page export. The current analysis therefore uses the recorded GSC URL export plus product-family siblings that can support focused internal linking. Before publishing any new guide, export GSC Performance data by query and by page for the same 28-day window and confirm the query intent.

## Ten Priority URLs

| Priority | URL | Why it is prioritized | Day 3 action |
| --- | --- | --- | --- |
| 1 | `/products/naturehike-giling-protm-1-person-backpacking-tent.html` | Present in the GSC priority export; commercial solo tent comparison intent. | Review title/meta against queries; add stronger internal links from tent and guide pages. |
| 2 | `/products/naturehike-mongartm-pro-1-person-ultralight-backpacking-tent.html` | Present in the GSC priority export; already supports the Giling Pro vs Mongar Pro guide. | Check CTR snippet and strengthen links from relevant Naturehike tent guide sections. |
| 3 | `/products/naturehike-snowbirdtm-sp550-down-mummy-sleeping-bag-29-3-f-1-5-c.html` | Present in the GSC priority export; clear temperature/model comparison intent. | Link from sleeping bag category and Snowbird comparison content. |
| 4 | `/products/naturehike-suntherm-m300-synthetic-sleeping-bag.html` | Present in the GSC priority export; synthetic sleeping bag model intent. | Compare title/meta with SunTherm M180/M400 sibling wording. |
| 5 | `/products/naturehike-peaklite-yl01-ultralight-folding-camping-table.html` | Present in the GSC priority export; commercial table query intent. | Review whether table copy answers size, weight, price and use-case differences. |
| 6 | `/products/asta-gear-astagear-vista-2-person-lightweight-tent-outdoor-hiking-camping-shelter-rainproof-wind-resistant.html` | Present in the GSC priority export; lightweight 2-person tent intent and already published. | Check page title length and internal links from lightweight tent content. |
| 7 | `/products/naturehike-giling-protm-2-person-backpacking-tent.html` | Same product family as priority URL 1; needed for a reviewed 1-vs-2 comparison. | Add to review queue; do not publish a guide until query data confirms demand. |
| 8 | `/products/naturehike-mongar-pro-2-person-ultralight-backpacking-tent.html` | Same product line as priority URL 2; supports Mongar Pro model exploration. | Use as supporting internal-link target from the existing Mongar/Giling guide. |
| 9 | `/products/naturehike-snowbird-sp700-down-mummy-sleeping-bag.html` | Close sibling to priority URL 3 and already used in an approved SP700 vs SP550 guide. | Verify snippet and add cross-links among Snowbird records. |
| 10 | `/products/naturehike-suntherm-m400-synthetic-sleeping-bag.html` | Close sibling to priority URL 4; useful for M300 vs warmer M400 intent. | Prepare comparison notes, then validate with query export before guide approval. |

## Three Guide Themes To Review

1. `naturehike-giling-pro-1-vs-2`: compare Giling Pro 1-person vs 2-person by capacity, listed weight, price and intended use. This expands from an existing GSC product URL without creating a broad unvalidated cluster.
2. `naturehike-snowbird-models-compared`: compare Snowbird SP400, SP550, SP700 and SP1000 by temperature label, listed weight, fill amount and price. This builds around the SP550 URL already seen in GSC and can link to the existing SP700 vs SP550 guide.
3. `naturehike-peaklite-tables-compared`: compare PeakLite FT07, FT08, L02, Y01 and YL01 tables by weight, price and packed-use case. This is a narrower furniture/table opportunity anchored by the YL01 GSC URL.

## Day 4 Handoff

- Export GSC Performance for the past 28 days by `Queries` and by `Pages`.
- Match queries to the 10 priority URLs above, then sort by impressions first and clicks second.
- Only approve a guide theme if at least one matching query cluster shows real impressions or a clear near-match commercial intent.
- Keep `data/reports/guide-candidates.csv` as a review queue, not a publishing queue.
