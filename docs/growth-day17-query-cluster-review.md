# Day 17 Query Clusters and Opportunity Queue

Date completed: 2026-08-09 (one day ahead of the V2 calendar)

## Data window

- Source: Google Search Console Search results, Web search.
- Window: 2026-07-11 through 2026-08-07, the current 28-day preset.
- Report freshness: GSC showed an update approximately four hours before the
  review.
- Property totals: 57 clicks, 2,901 impressions, 2.0% CTR and average position
  16.1.
- Visible query table: 355 queries, 10 clicks and 622 impressions.

GSC suppresses some low-volume queries for privacy. The visible query table
therefore represents 17.5% of total clicks and 21.4% of total impressions. The
clusters below describe the visible query evidence; they are not a complete
allocation of every property impression.

Machine-readable outputs:

- [`gsc-query-clusters-2026-08-09.csv`](../data/reports/gsc-query-clusters-2026-08-09.csv)
- [`growth-opportunity-queue-2026-08-09.csv`](../data/reports/growth-opportunity-queue-2026-08-09.csv)

## Brand and non-brand split

Queries were classified in three mutually exclusive groups. An explicit brand
query contains a company name. A model-brand query omits the company but names
a proprietary family such as Mongar, Snowbird or Amenity Dome. Everything else
is non-brand.

| Intent | Queries | Clicks | Impressions | CTR | Avg. position |
| --- | ---: | ---: | ---: | ---: | ---: |
| Explicit brand | 220 | 6 | 406 | 1.5% | 21.8 |
| Model-brand | 43 | 3 | 101 | 3.0% | 18.6 |
| Non-brand | 92 | 1 | 115 | 0.9% | 29.4 |

Explicit and model-brand intent account for 507 of 622 visible impressions
(81.5%). The site is currently discovered mainly for exact brands and models,
not broad camping advice. This supports improving existing product families
before publishing broad informational content.

## Strongest specific clusters

| Cluster | Queries | Clicks | Impressions | CTR | Position | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Naturehike Mongar | 22 | 2 | 72 | 2.8% | 11.5 | Strongest combination of depth, clicks and near-page-one rank. |
| NEMO tarp and shelter | 6 | 0 | 30 | 0% | 24.3 | Existing demand, but the brand page has sparse specifications. |
| Naturehike Snowbird | 7 | 1 | 27 | 3.7% | 9.4 | Existing guide and product winner; refresh rather than expand. |
| Naturehike Cloud Up | 13 | 0 | 20 | 0% | 34.3 | Broad family demand, but ranking is too weak for a CTR-only change. |
| Naturehike Yugu | 5 | 0 | 18 | 0% | 9.8 | Close ranking with multiple variants; data audit comes first. |
| Naturehike FC pads | 8 | 0 | 18 | 0% | 11.0 | FC01 and FC10 intent may require clearer family navigation. |
| Mobi Garden Lunta | 2 | 2 | 16 | 12.5% | Early winner with too little volume to justify changing it. |
| Snow Peak Amenity Dome | 6 | 0 | 14 | 0% | Existing guide should remain stable while the sample grows. |
| Naturehike Massif | 4 | 0 | 11 | 0% | Clear model family and comparison potential, but no click yet. |
| Montbell Rera Dome | 1 | 0 | 8 | 0% | Position 5 is promising, but one query and eight impressions are insufficient. |

## Opportunity scoring

The V2 18-point model was applied without changing its six dimensions. For
repeatability, search demand used visible cluster impressions: 0 for no signal,
1 for 1-4, 2 for 5-14, 3 for 15-29, 4 for 30-59 and 5 for 60 or more. Ranking
proximity scored 3 at positions 4-15, 2 at 15.1-30, 1 at 30.1-50 and 0 outside
that range. The remaining dimensions were reviewed against local official
records, existing pages and the Day 16 quality findings.

The score is an opportunity signal, not automatic permission to publish. New
guides still require at least 11 total points, data completeness of at least 2,
source review and a distinct decision job.

## Action queue

### Update five existing pages

1. **Naturehike Mongar, 18/18:** strengthen the Mongar Base 3 winner and link
   the family by capacity and variant.
2. **Naturehike Snowbird, 16/18:** refresh the existing SP700 vs SP550 guide;
   do not create another Snowbird URL.
3. **NEMO tarp and shelter, 13/18:** improve the existing brand page, but its
   data completeness score of 1 blocks a new guide.
4. **Montbell Down Hugger 650, 14/18:** perform Day 19's source and
   decision-value refresh. Its search-demand score is only 1, so this is a
   quality task rather than evidence of breakout demand.
5. **Big Agnes Tiger Wall, 10/18:** carry out the pre-scheduled Day 18 controlled
   improvement. The low score must be recorded; this is not a new-content win.

### Observe five pages

1. Mobi Garden Lunta, 15/18: protect the current winner.
2. Naturehike Yugu, 15/18: audit variants before considering a family guide.
3. Naturehike FC pads, 15/18: wait for clearer FC01 versus FC10 query intent.
4. Snow Peak Amenity Dome, 14/18: keep the existing guide stable.
5. Montbell Rera Dome, 13/18: wait for more than eight impressions.

### New-guide candidates

Only two candidates were retained, and neither was generated or approved:

1. **Naturehike Mongar Base 2 vs 3, 18/18.** The cluster has 72 visible
   impressions, two clicks and 22 queries. Recheck both official listings and
   confirm that a capacity decision is not already satisfied by the product
   pages before Day 25.
2. **Naturehike Massif 2 vs 4, 15/18.** Both records have weight, capacity,
   price, currency and official sources. Confirm distinct comparison intent;
   the cluster currently has no click.

## Day 18 handoff

Use the existing Big Agnes Tiger Wall guide as the treatment page and the
similar Copper Spur range guide as a contextual control candidate. Change one
primary variable only, record the hypothesis in the experiment register and do
not treat the weak Tiger Wall query sample as proof of demand.
