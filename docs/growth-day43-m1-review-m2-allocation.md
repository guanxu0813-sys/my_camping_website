# Day 43 M1 Review and M2 Allocation

Review completed: 2026-09-07
M1 result: **FOCUS WITH TWO QUALIFIED CLUSTERS**

## Baseline and result

The V2 baseline was a single complete week: 39 sessions, 17 Organic Search
sessions, 25 GSC clicks and 1,270 impressions. M1 uses absolute 28-day totals;
weekly averages are shown only to make the baseline comparison readable.

| Metric | V2 baseline week | M1 total | M1 weekly average | Change vs baseline week |
| --- | ---: | ---: | ---: | ---: |
| GA4 sessions | 39 | 174 | 43.50 | +11.5% |
| GA4 Organic Search sessions | 17 | 93 | 23.25 | +36.8% |
| GSC clicks | 25 | 105 | 26.25 | +5.0% |
| GSC impressions | 1,270 | 5,693 | 1,423.25 | +12.1% |

For the required month-over-month search comparison, the adjacent complete
28-day GSC windows are:

| GSC window | Clicks | Impressions | CTR | Position |
| --- | ---: | ---: | ---: | ---: |
| Jul 8-Aug 4 | 47 | 2,390 | 1.97% | 16.6 |
| Aug 5-Sep 1 | 105 | 5,693 | 1.84% | 16.2 |

Clicks increased by 58 and impressions by 3,303. CTR declined 0.13 percentage
points while average position improved 0.4. The prior GA4 window is not used
for a month-over-month claim because analytics was deployed only on July 30 and
does not cover that full window.

## What worked

- Naturehike reached 52 clicks and 2,522 impressions; Big Agnes reached 15
  clicks and 434 impressions. Both pass the cluster expansion gate.
- M1 produced four consistent weekly reviews and one clean 28-day absolute
  baseline for future comparison.
- Existing guide updates produced 18 clicks from 384 impressions. The single
  new Mongar Base guide added 3 clicks from 57 impressions without opening a
  broad publishing pipeline.
- The latest 10-page structured-data and visible-content re-audit passed after
  two stale facts were corrected.

## Experiments and failures

- All three CTR/content experiments that reached their decision date lacked
  the predefined sample. None is called a winner, and no pattern is rolled out
  site-wide.
- `compare_selected` recorded zero events during the 28-day M1 window. The site
  has engagement, but the compare workflow has not yet shown measurable use.
- Nine logged emails and four community answers produced no verified reply or
  acquired link. One Email session was not engaged.
- Referring-domain breadth stayed at two. Search growth is not yet supported by
  broader editorial authority.
- The initial broad audit found a 40% sampled factual-error rate. A later 0%
  targeted re-audit reduces immediate risk but does not clear the entire URL
  inventory.

## M2 scope

Only **Naturehike** and **Big Agnes** enter the M2 growth queue. Montbell,
Lanshan/3F UL Gear and other topics remain in maintenance or observation.

| Allocation | Share | M2 work |
| --- | ---: | --- |
| Naturehike cluster | 35% | Update proven guides and decision paths first; publish at most two scored adjacent guides. |
| Big Agnes cluster | 25% | Improve pages already ranking and earning clicks; publish at most two scored adjacent guides. |
| Data quality and technical health | 20% | Re-audit high-risk product facts, schema, canonicals and indexing exceptions. |
| Measurement and experiment design | 15% | Weekly fixed windows, high-intent attribution and one properly powered test at a time. |
| Evidence-led distribution | 5% | Respond to real replies and pitch only a directly relevant improved asset; no recurring cold-volume target. |

The hard M2 cap remains four new guides, no more than two per qualified cluster.
A guide still needs an opportunity score of at least 11/18 and data completeness
of at least 2/3. If weekly capacity falls below eight hours, new guides are the
first work removed.

## M2 decision targets

1. Increase the next complete 28-day qualified organic result from the M1
   baseline of 93 organic sessions and 53 engaged organic sessions; do not add
   event counts to sessions.
2. Obtain clicks in both selected clusters while preserving data accuracy.
3. Broaden relevant referring domains beyond two before entering M3.
4. Validate compare-flow tracking and investigate why `compare_selected` is
   zero before attempting an affiliate CTA expansion.

M2 is therefore an evidence-limited expansion, not permission to generate four
guides automatically.

## Closeout

M1 operational work is closed. Affiliate approval, the September 23 data-asset
experiment read and any later D-tier cleanup are trigger-based M2/later work,
not unfinished Day 14-43 tasks. Their exact safe states and next actions are in
`growth-m1-closeout.md`.
