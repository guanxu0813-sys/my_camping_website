# Day 40 CTR Experiment Review

Review completed: 2026-09-07
Experiment: `EXP-2026-08-05-CTR-01`
Status: **SAMPLE_INSUFFICIENT**
Decision: **DO NOT ROLL OUT OR REVERT AS A GROUP**

## Measurement windows

- Before: 2026-07-08 to 2026-08-04 (28 days)
- After: 2026-08-05 to 2026-09-01 (28 days)
- Source: GSC Performance, Web search, page dimension
- Change deployed: 2026-08-05
- Minimum sample: 300 after-period impressions per page

The windows are adjacent and do not overlap. GSC was updated through September
5 when the report was exported on September 7, so both windows were complete.

## Page results

| Page | Before clicks | Before impr. | Before CTR | Before pos. | After clicks | After impr. | After CTR | After pos. | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `/tent.html` | 0 | 83 | 0% | 14.95 | 3 | 296 | 1.01% | 32.54 | sample insufficient |
| `/guides/2-person-backpacking-tents-under-2kg.html` | 0 | 92 | 0% | 37.89 | 0 | 21 | 0% | 40.52 | sample insufficient |
| `/sleeping-pad.html` | 0 | 61 | 0% | 23.90 | 2 | 183 | 1.09% | 38.19 | sample insufficient |
| `/sleeping-bag.html` | 0 | 59 | 0% | 32.15 | 3 | 221 | 1.36% | 41.76 | sample insufficient |
| `/products/naturehike-giling-protm-1-person-backpacking-tent.html` | 0 | 48 | 0% | 9.71 | 0 | 10 | 0% | 12.40 | sample insufficient |
| `/products/naturehike-peaklite-yl01-ultralight-folding-camping-table.html` | 0 | 28 | 0% | 7.07 | 0 | 2 | 0% | 3.00 | sample insufficient |
| `/products/naturehike-daban-2-person-ultralight-4-season-tunnel-tent.html` | 1 | 31 | 3.23% | 6.29 | 0 | 28 | 0% | 6.57 | sample insufficient |
| `/products/naturehike-mongartm-pro-1-person-ultralight-backpacking-tent.html` | 0 | 25 | 0% | 11.76 | 0 | 10 | 0% | 9.10 | sample insufficient |
| `/products/naturehike-snowbirdtm-sp550-down-mummy-sleeping-bag-29-3-f-1-5-c.html` | 0 | 27 | 0% | 11.85 | 0 | 21 | 0% | 8.62 | sample insufficient |
| `/brands/nemo-tarp.html` | 0 | 25 | 0% | 16.28 | 0 | 8 | 0% | 20.62 | sample insufficient |

## Cohort summary

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Clicks | 1 | 8 | +7 |
| Impressions | 479 | 800 | +67.0% |
| CTR | 0.21% | 1.00% | +0.79 pp |
| Impression-weighted average position | 20.80 | 34.31 | worsened 13.51 |

The aggregate CTR improvement is concentrated in three category pages:
`/tent.html`, `/sleeping-pad.html` and `/sleeping-bag.html`. Those pages gained
all eight after-period clicks, but all three also had materially worse average
positions. The guide, five product pages and one brand page generated no
after-period clicks; the DABAN page lost its single before-period click.

## Decision

1. No page reached the predefined 300-impression minimum. `/tent.html` was
   closest at 296 impressions. The experiment is therefore
   `sample_insufficient`, not a winner or loser.
2. Do not apply the title pattern across the rest of the site. The experiment
   has no control group, ranking mix changed materially and page-level samples
   remain small.
3. Do not revert the ten snippets as a group. Their model, product type and
   decision specifications are still accurate and useful to searchers; lack of
   sample is not evidence that the copy is harmful.
4. Treat the three category pages as directional leads only. Future edits must
   be page-specific and backed by query intent, not by this aggregate result.
5. Close this pre/post experiment as sample insufficient. Any new snippet test
   must use a matched control and a frozen cohort, following
   `EXP-2026-08-10-CTR-02` rather than extending this uncontrolled test.
