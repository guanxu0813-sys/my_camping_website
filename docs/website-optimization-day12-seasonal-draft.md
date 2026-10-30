# Day 12: Seasonal data asset draft

Date: 2026-10-30

Status: COMPLETED — private `noindex` draft, not approved for publication

## What was built

A reproducible local HTML draft was generated from the 27 eligible Day 11 candidates:

- `scripts/build_winter_sleeping_bag_draft.py` reads the reviewed candidate CSV.
- `docs/drafts/winter-sleeping-bag-data-asset.html` contains the draft page, temperature-band summary, accessible scatter chart, currency-separated tables, official source links, methodology and limitations.
- The HTML carries `noindex,nofollow,noarchive`, a visible private-draft warning and no production canonical URL.

The draft is intentionally stored under `docs/drafts/`. It was not added to the public guide generator, navigation, sitemap or RSS.

## Descriptive output

- Draft candidates: 27.
- Brands: Naturehike 12, NANGA 11, Montbell 4.
- Currencies: USD 12, JPY 11, GBP 4; price summaries remain separated by currency.
- Catalog status: 4 verified, 23 draft.
- Rows with a distinct lower-limit label: 4.

The chart plots the stored comfort value against representative catalog weight. It does not rank warmth, value, or product performance. The copy explicitly separates comfort labels from lower-limit labels and explains that actual warmth varies.

## Publication gate

The draft remains blocked from publication because 23 of 27 candidate rows still carry draft catalog status. Day 13 must manually verify all 27 official source pages or reduce the asset to a completely checked subset. A factual error rate of 5% or more blocks publication.

No account access, external contact, sitemap submission, or public release occurred.

## Verification

- The generator rebuilt the draft deterministically from the Day 11 CSV.
- Regression coverage verifies candidate count, brand/currency boundaries, `noindex`, draft warning, method copy, currency separation and absence from sitemap/RSS.
- `npm test`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_growth_tools.py`: 20/20 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_generated_site.py`: 901 HTML files and 863 unique sitemap URLs passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_structured_data.py`: 10/10 samples passed.
- `git diff --check`: passed.

## Next action

Day 13 should open every retained official source, record the observed comfort/lower-limit label, weight, price/currency and availability, then calculate the factual error rate. The separate GA4/GSC export request remains `NEEDS_USER` and was not estimated.
