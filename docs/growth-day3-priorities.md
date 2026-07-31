# Day 3 GSC Priority Analysis

Date: 2026-07-31

Status: Complete

## Source Data

- GSC period: 2026-07-02 through 2026-07-29 (past 28 days).
- Raw export: 192 query rows and 306 page rows in `data/gsc/2026-07-31/`.
- Current period: 26 clicks, 1,320 impressions, 2.0% CTR, average position 16.1.
- Previous 28 days: 2 clicks and 15 impressions, observed with the GSC previous-period comparison.
- Sitewide impression growth: 8,700%. Because the previous period is extremely small, this is treated as an emergence signal rather than a stable growth rate.

## Selection Method

Pages were selected when they met at least one of these conditions:

1. Average position 4-15 with weak CTR relative to the available impressions.
2. Average position 16-30 while the site moved from 15 to 1,320 impressions.
3. A matching exact-model query cluster showed measurable impressions and the page can support a factual comparison.

Guide themes also had to have matching product records and could not duplicate an already published guide.

## Ten Priority URLs

| Priority | URL | Clicks | Impressions | CTR | Position | Opportunity |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `/tent.html` | 0 | 97 | 0% | 10.89 | Highest-impression page with page-one visibility and no clicks. |
| 2 | `/products/naturehike-giling-protm-1-person-backpacking-tent.html` | 0 | 46 | 0% | 9.57 | Page-one exact-model visibility; supported by a 13-impression Giling Pro query cluster. |
| 3 | `/sleeping-bag.html` | 1 | 44 | 2.27% | 24.68 | Category page in the 16-30 improvement band during sitewide impression growth. |
| 4 | `/products/naturehike-snowbird-sp700-down-mummy-sleeping-bag.html` | 2 | 42 | 4.76% | 9.38 | Strongest exact-model page; use it to strengthen the existing SP700 vs SP550 guide and sibling links. |
| 5 | `/sleeping-pad.html` | 0 | 34 | 0% | 19.12 | Category page in the 16-30 band with no clicks. |
| 6 | `/products/naturehike-mongartm-base-3-person-ultralight-backpacking-tent.html` | 1 | 30 | 3.33% | 8.63 | Exact-model demand; matching Mongar Base queries produced 14 impressions. |
| 7 | `/products/naturehike-peaklite-yl01-ultralight-folding-camping-table.html` | 0 | 28 | 0% | 7.07 | High position and zero clicks; prioritize title and snippet review. |
| 8 | `/products/naturehike-mongartm-pro-1-person-ultralight-backpacking-tent.html` | 0 | 25 | 0% | 11.76 | Improve snippet and links from the existing Giling Pro vs Mongar Pro guide. |
| 9 | `/products/naturehike-snowbirdtm-sp550-down-mummy-sleeping-bag-29-3-f-1-5-c.html` | 0 | 24 | 0% | 12.25 | Improve snippet and links from the existing Snowbird comparison. |
| 10 | `/brands/nemo-tarp.html` | 0 | 24 | 0% | 16.46 | The matching `nemo tarp tents` query had 19 impressions at position 17.47. |

## Three Confirmed Guide Themes

1. `naturehike-giling-pro-models-compared` - **Naturehike Giling Pro 1 vs 2**
   Evidence: five matching queries produced 13 impressions. The Giling Pro 1 page had 46 impressions at position 9.57 with no clicks, and both model records are present.

2. `naturehike-mongar-base-models-compared` - **Naturehike Mongar Base 2 vs 3**
   Evidence: three matching queries produced 14 impressions. The Mongar Base 3 page had 30 impressions and one click at position 8.63, and both model records are present.

3. `nemo-tarps-and-shelters-compared` - **NEMO tarps and shelters compared**
   Evidence: `nemo tarp tents` had 19 impressions at position 17.47, while the NEMO tarp hub had 24 impressions at position 16.46. Three published NEMO tarp or shelter records are available for comparison.

## Topics Not Selected

- Snowbird SP700 vs SP550 already has a published guide, so its signal should drive an update and stronger internal links rather than a duplicate article.
- Giling Pro 1 vs Mongar Pro 1 already has a published guide. The new Giling theme compares capacities within the same product line instead.
- PeakLite tables remain a future candidate, but the export contains no matching PeakLite query cluster, so the topic is not confirmed for next week.

## Day 4 Handoff

- Use these ten URLs as the next-page optimization queue.
- Keep all three guide themes in editorial review until official specifications and comparison takeaways are checked.
- Do not bulk-publish generated guide candidates.
