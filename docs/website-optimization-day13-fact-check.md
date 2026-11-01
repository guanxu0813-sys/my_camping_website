# Day 13 catch-up: Seasonal asset fact check

Execution date: 2026-11-01

Scheduled date: 2026-10-31

Status: NEEDS_USER — publication gate failed

## Result

Five of the 27 draft rows were checked against current official product pages. Two failed, producing a **40% row-level error rate**. The SOP publication threshold requires an error rate below 5%, so checking stopped and the asset remains private.

| Result | Count |
| --- | ---: |
| Pass | 3 |
| Fail | 2 |
| Checked | 5 |

Detailed evidence is recorded in `docs/website-optimization-day13-fact-check.csv`.

## Failures

1. **Naturehike Snowbird SP1000:** the stored row says comfort `-10°C`, weight `1.9 kg`, and price `$249.99`. The current official specification table lists comfort `-10.8°C`, model weights around `1.51–1.54 kg`, and price `$239.99`. The page title still uses the rounded `-10°C`, which is not sufficient to validate the underlying row.
2. **Montbell Down Hugger 650 #2 Regular:** the stored official product URL now returns 404. A row with an unavailable primary source cannot remain in a publishable evidence table without a verified replacement URL.

The three passing Montbell rows matched their stored comfort, lower-limit and rounded packed-weight values. One has a current sale price, while the stored value matches the displayed regular reference price.

## Method issue corrected

All 27 underlying catalog records were fetched on **2026-07-03**, not 2026-10-29. Day 12 used the sample-generation date as the source snapshot date. The candidate CSV and draft generator now preserve and display the actual source snapshot date.

## Decision

- Do not publish the winter sleeping-bag asset.
- Do not add it to navigation, sitemap or RSS.
- Do not silently overwrite the remaining 22 unchecked records.
- Keep the local `noindex` draft as an audit artifact.

## User decision needed

Choose whether the next cycle should spend time refreshing all 27 records from official sources or shelve this asset and focus on already-performing Naturehike and Big Agnes pages. Until that decision, no publication work should continue.
