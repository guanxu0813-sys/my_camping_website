# Day 21–22 Controlled CTR Experiment

Experiment: `EXP-2026-08-10-CTR-02`

## Baseline

- Source: Google Search Console Web performance export saved under
  `data/gsc/2026-08-10/`.
- Window: 2026-07-12 through 2026-08-08, the latest complete 28 days.
- Property totals: 62 clicks, 3,090 impressions, 2.0% CTR and average position
  15.7.
- Eligibility: B-tier pages with zero clicks and average position 21–50.
- Exclusion: every page already changed by the Day 10 experiment.

Both cohorts contain six tent product pages, two sleeping-pad product pages and
two sleeping-bag product pages. Treatment had 127 baseline impressions and an
impression-weighted average position of 28.7. Control had 105 impressions and
an impression-weighted average position of 29.9. Baseline CTR was 0% for both.

## Frozen pairs

| Pair | Treatment page | Impressions / position | Unchanged control page | Impressions / position | Match reason |
| --- | --- | ---: | --- | ---: | --- |
| 1 | `/products/naturehike-mongar-ul-2-person-ultralight-backpacking-tent.html` | 30 / 23.9 | `/products/naturehike-cloud-up-base-2-person-ultralight-backpacking-tent.html` | 20 / 23.7 | Naturehike two-person backpacking tents with nearly identical rank. |
| 2 | `/products/onetigris-coco-nest-solo-hot-tent.html` | 17 / 26.7 | `/products/snow-peak-amenity-dome-m-ivory.html` | 16 / 27.5 | Tent product pages with adjacent impression and rank bands. |
| 3 | `/products/naturehike-cloud-up-ul-2-person-ultralight-backpacking-tent.html` | 12 / 24.1 | `/products/naturehike-mongar-2-person-ultralight-backpacking-tent.html` | 14 / 23.7 | Naturehike two-person tent pages with adjacent rank and demand. |
| 4 | `/products/3f-ul-gear-lanshan-1.html` | 13 / 43.8 | `/products/3f-ul-gear-lanshan-2.html` | 11 / 42.6 | Same brand and tent family with adjacent rank and demand. |
| 5 | `/products/naturehike-cloud-up-pro-1-person-ultralight-backpacking-tent.html` | 9 / 21.3 | `/products/snow-peak-land-lock.html` | 7 / 23.6 | Tent product pages near the top of the B-tier rank band. |
| 6 | `/products/naturehike-cloud-up-2-person-ultralight-backpacking-tent.html` | 8 / 36.1 | `/products/snow-peak-land-lock-tent-set.html` | 9 / 35.4 | Tent product pages with nearly identical rank and demand. |
| 7 | `/products/sea-to-summit-comfort-light-insulated-pad.html` | 13 / 32.5 | `/products/nemo-roamer.html` | 12 / 40.0 | Sleeping-pad product pages with adjacent demand. |
| 8 | `/products/therm-a-rest-neoloft-sleeping-pad.html` | 7 / 28.7 | `/products/sea-to-summit-camp-self-inflating-pad.html` | 5 / 28.4 | Sleeping-pad product pages with nearly identical rank. |
| 9 | `/products/sea-to-summit-ascent-womens-down-sleeping-bag.html` | 11 / 31.3 | `/products/big-agnes-greystone-thirty.html` | 7 / 34.0 | Sleeping-bag product pages in the same rank band. |
| 10 | `/products/big-agnes-anthracite-thirty.html` | 7 / 24.7 | `/products/aegismax-aegismax-wind-hard-twilight-10d-5-degree-800fp-down-sleeping-bag-ultralight.html` | 4 / 21.2 | Sleeping-bag product pages near the top of B tier. |

## Treatment

Only the HTML title and meta description are changed. Each treatment puts the
exact model, product type and verified decision specifications earlier. H1,
body copy, product data, canonical URLs, internal links and structured product
facts remain generated from the same source records.

Control titles and descriptions are frozen. The Day 10 cohort is also excluded
from both groups so its earlier change cannot be mistaken for this experiment.

## Decision rule

- Start date: 2026-08-10 production deployment.
- Earliest decision: 2026-09-07.
- Primary metric: group-level GSC CTR over a comparable 28-day window.
- Guardrails: group impressions and impression-weighted average position.
- Minimum sample: 300 impressions per cohort and at least three pages with a
  click in each cohort.
- If the time threshold passes without the sample, mark `sample_insufficient`;
  do not force a winner.
