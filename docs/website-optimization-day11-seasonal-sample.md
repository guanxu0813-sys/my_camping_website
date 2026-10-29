# Day 11: Seasonal data asset topic and sample

Date: 2026-10-29

Status: COMPLETED — draft sample only, not approved for publication

## Selected topic

**Cold-weather sleeping bags with an explicit comfort label at or below 5°C**

The proposed asset would compare listed comfort temperature and representative weight, while keeping USD, GBP and JPY prices in separate currency groups. It must not call a product “best,” treat lower-limit temperature as routine comfort, or compare prices across currencies.

## Why this topic was selected

Three autumn/winter ideas were checked against the current catalog:

| Candidate | Structured sample | Decision |
| --- | ---: | --- |
| Cold-weather sleeping bags | 48 records with a comfort label; 27 pass the draft filter | Selected for a review-only draft |
| High-R sleeping pads | 11 records across 3 brands and 7 listed R-values | Too narrow for a standalone asset now |
| Four-season tents | 0 structured season fields; 38 descriptions mention a season | Rejected because text matching would mix inconsistent marketing language |

The sleeping-bag topic has the strongest structured sample and fits autumn/winter intent without creating a new product category or inventing performance claims.

## Reproducible sample rule

The generator reads existing official product records and includes a candidate only when:

- the category is `sleeping-bag`;
- the record has an explicit Celsius comfort value;
- Fahrenheit and Celsius labels, when both exist, agree within 2°C;
- comfort temperature is 5°C or colder;
- weight, price and official source URL are present;
- currencies remain unconverted.

Output: `data/reports/winter-sleeping-bag-candidate-sample.csv`

## Sample quality

- Temperature-labelled records inspected: 48.
- Eligible draft candidates: 27.
- Eligible brands: Naturehike 12, NANGA 11, Montbell 4.
- Eligible currencies: USD 12, JPY 11, GBP 4.
- Catalog review status: 4 verified, 23 draft.
- Eligible rows with a separate lower-limit label: 4.
- Eligible rows with an official source URL: 27/27.

Exclusions:

- 12 are warmer than the 5°C scope.
- 5 lack a usable weight.
- 3 have conflicting Fahrenheit/Celsius labels.
- 1 has no Celsius comfort value (`850°F`, which appears to be fill power placed in the temperature field).

## Publication gate

The sample is large enough to build a private Day 12 draft, but **not ready to publish**. Only 4 of 27 eligible rows currently carry verified catalog status, and only 4 include a separate lower-limit value.

Before publication:

1. Day 12 may build a local draft table and methodology from the 27 eligible rows.
2. Day 13 must verify all 27 official source pages or reduce the asset to a fully checked subset.
3. Any source error rate of 5% or more blocks publication.
4. Prices must stay separated by currency; no exchange-rate conversion is allowed.
5. The final copy must distinguish comfort labels from lower-limit labels and state that individual warmth varies.

## Verification

- The generator produced 48 deterministic rows and 27 eligible candidates.
- Regression coverage freezes candidate count, exclusion reasons, status mix and currency boundaries.
- No HTML page, sitemap entry, RSS item or public URL was created.
- `npm test`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_growth_tools.py`: 19/19 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_generated_site.py`: 900 HTML files and 863 unique sitemap URLs passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_structured_data.py`: 10/10 samples passed.
- `git diff --check`: passed.

## Next action

Day 12 can create a private, non-indexed draft artifact from this sample. Current GA4/GSC exports remain a separate user action and were not estimated.
