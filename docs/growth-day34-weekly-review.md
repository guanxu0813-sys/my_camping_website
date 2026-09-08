# Day 34 Weekly Review

Review completed: 2026-08-29
Status: **COMPLETED**
Decision: **FOCUS**

## Fixed-window comparison

Both products use the complete August 19-25 window and compare it with August
12-18. GSC excludes the latest processing days; GA4 uses the same fixed dates.

| Metric | Aug 12-18 | Aug 19-25 | Change |
| --- | ---: | ---: | ---: |
| GA4 sessions | 39 | 47 | +20.5% |
| GA4 organic-search sessions | 20 | 24 | +20.0% |
| GA4 engaged sessions | 18 | 15 | -16.7% |
| GA4 events | 174 | 223 | +28.2% |
| GA4 key events | 0 | 2 | +2 |
| GSC clicks | 22 | 33 | +50.0% |
| GSC impressions | 1,360 | 1,456 | +7.1% |
| GSC CTR | 1.6% | 2.3% | +0.7 pp |
| GSC average position | 14.4 | 18.0 | worsened 3.6 |

GA4 also recorded 46 active users, 46 new users and 16 seconds of average
engagement time per active user. GSC covered through August 25 when reviewed.

## Search and cluster interpretation

- Clicks recovered by 11 and impressions increased by 96. CTR also recovered
  from 1.6% to 2.3%.
- Average position worsened from 14.4 to 18.0. The extra visibility is not yet
  evidence of more stable first-page rankings.
- The visible query table exposed only one non-anonymized row for this weekly
  window (`naturehike cw280`, 9 impressions, 0 clicks, position 9.4). GSC
  privacy suppression makes the table too incomplete for a reliable weekly
  Mongar, Big Agnes, Montbell or other cluster allocation.
- No cluster is approved for expansion from these property totals. Cluster
  decisions remain tied to a complete 28-day query export or the existing
  six-week/100-impression/one-click/three-query gate.

## High-intent and authority checks

- Organic Search produced 24 sessions and 11 engaged sessions, but landing-page
  scope was not validated, so the 11 sessions are not automatically classified
  as qualified organic visits.
- GA4 recorded `product_modal_open` 0, `compare_selected` 0 and
  `outbound_click` 2 across all channels. Organic Search recorded 0 key events;
  the two outbound clicks came from Direct traffic.
- GSC Links showed 14 external links from 2 referring domains: `github.com`
  and `pinterest.com`. The referring-domain count is unchanged from baseline.
- Traffic improved, but the absence of an organic high-intent event and the
  weaker average position keep the decision at **FOCUS**.

## Experiment status

All active experiments remain `observing`:

| Experiment | Earliest decision | Day 34 status |
| --- | --- | --- |
| `EXP-2026-08-05-CTR-01` | 2026-09-02 | observing; do not decide early |
| `EXP-2026-08-09-TIGER-01` | 2026-09-07 | observing; pages remain frozen |
| `EXP-2026-08-10-CTR-02` | 2026-09-07 | observing; cohorts remain frozen |
| `EXP-2026-08-12-DATA-01` | 2026-09-23 | observing; outreach sample remains below threshold |

The recovered property-level CTR is not attributed to an experiment because
it mixes treatment, control, unchanged pages, new pages and anonymized queries.

## Next actions

1. Keep broad URL expansion paused and improve intent matching on pages already
   earning impressions.
2. Recheck `EXP-2026-08-05-CTR-01` on or after September 2 with its full 28-day
   window; do not modify its treatment pages before then.
3. Inspect the organic landing pages behind the 11 engaged sessions and improve
   the path from guide conclusion to comparison or outbound action.
