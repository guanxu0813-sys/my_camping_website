# Day 9: Big Agnes cluster internal links

Date: 2026-10-27

Status: COMPLETED

## Goal

Connect the existing Big Agnes guides, brand hubs and product pages into a clear decision path without creating new pages or adding unreviewed claims.

## Changes

- Added `brand_id: big-agnes` to the approved Tiger Wall UL2 vs Copper Spur UL2 comparison metadata.
- Added the comparison guide to the main Big Agnes brand hub and the Big Agnes tents page.
- Added a Big Agnes gear-hub link to the UL2 comparison guide.
- Preserved the existing product-to-guide reverse links for all products covered by the three guides.
- Added regression coverage so the brand and tent hubs must contain exactly the three approved Big Agnes guides, with no duplicate paths.

## Coverage

- Approved Big Agnes guides: 3/3 linked from the brand hub.
- Big Agnes tent guides: 3/3 linked from the tent hub.
- Unique products represented by those guides: 16/16 retain reverse guide links.
- New public URLs: 0.
- Sitemap URL count: unchanged at 863.

## Anchor review

The hub links use specific decision labels rather than generic anchors:

- `Big Agnes Tiger Wall UL2 vs Copper Spur UL2`
- `Big Agnes Copper Spur Models Compared`
- `Big Agnes Tiger Wall Models Compared`

The comparison guide uses `Big Agnes gear hub` for the brand-level route. No repeated `click here` or unrelated cross-category links were added.

## Mobile usability check

- Guide pages with compare links have responsive viewport metadata.
- Guide action buttons stack vertically and use full width below 768 px.
- Wide comparison tables remain horizontally scrollable.
- The category comparison tray and product modal retain their existing mobile layouts.
- These conditions are now checked by `scripts/audit_comparison_funnel.mjs` as part of `npm test`.

## Verification

- `npm test`: passed; analytics smoke test and 14 guide comparison links across 4 category pages passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_growth_tools.py`: 17/17 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_generated_site.py`: 900 HTML files and 863 unique sitemap URLs passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_structured_data.py`: 10/10 samples passed.
- `git diff --check`: passed.

## Remaining user action

No user action is required for the Day 9 site changes. The separate Day 1 request for current GA4/GSC exports remains open; no analytics values were invented for this task.
