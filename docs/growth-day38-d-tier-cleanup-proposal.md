# Day 38 D-Tier Cleanup Proposal

Date: 2026-08-15  
Status: **Proposal complete; no URL changed, merged or noindexed**

## Evidence Limits

- The original 2026-08-07 sample contains no GSC click/impression row for these 15 URLs.
- Exact-URL public web searches on 2026-08-15 returned no result for all 15 URLs. This is a conservative discovery check, not a substitute for a backlink database.
- Internal entrance counts are generated-site link counts. They show that a URL is reachable, not that users visit it.
- Every candidate still has an official source URL and unique model identity, so none should be merged merely because it lacks current GSC evidence.

## Conditional Noindex Candidates

These pages should first receive a targeted correction/enrichment pass. Only
if that cannot be completed should temporary noindex be considered.

| ID | Page | Internal entrances | Reason | Required next action |
| --- | --- | ---: | --- | --- |
| S36 | Nanga Level 8 -20 UDD Bag | 2 | Confirmed weight and temperature errors | Correct from official source, then keep |
| S37 | Naturehike Morning View King mattress | 2 | Capacity and weight conflict | Resolve variant fields, then keep |
| S41 | Montbell Burrow Bag #5 Long | 7 | Fill type is incorrectly shown as down | Correct to synthetic and add temperature limits |
| S43 | NEMO Pulse quilt | 9 | Only three useful specs and no weight | Enrich or temporarily noindex |
| S44 | Nanga Minimarhythm Zero | 2 | Only two useful specs | Enrich or temporarily noindex |
| S47 | Aegismax Wind Hard Tiny quilt | 2 | `0.29 kg` appears to be fill weight, not total weight | Correct weight basis or temporarily noindex |
| S48 | Asta Gear Shanju pyramid tent | 15 | Blank description and only three specs | Add sourced description/specs or temporarily noindex |

## Protected / Hold URLs

S38, S39, S40, S42, S45, S46, S49 and S50 remain protected. They have either
more useful unique data, substantial internal entrances, an active guide
cluster, or a correction that has now been completed. S42 is also inside the
Tiger Wall cluster and must not be changed while its existing experiment is
still being observed.

## Decision Rule

Before any future noindex or merge, refresh GSC page data and external-link
evidence, correct source errors, and wait at least 14 days after the correction.
Merge only when two URLs represent the same search intent and the destination
preserves every useful field. Use a redirect for a true merge; never remove a
URL that has clicks or a verified backlink without a migration plan.
