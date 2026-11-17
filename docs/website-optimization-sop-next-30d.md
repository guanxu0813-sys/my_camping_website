# CampGear Compare Next 30-Day Optimization Plan

- Proposed cycle: 2026-11-18 through 2026-12-17
- Operating mode: `FOCUS`
- Activation: Draft only; do not schedule or execute automatically until the owner approves a new cycle
- Primary principle: measurement recovery first, low-risk usability/performance second, acquisition expansion only after evidence gates pass

## Cycle Objectives

1. Import one aligned recent 28-day GA4, GSC, and referring-domain window and close the blocked Day 17, 23, and 28 decisions.
2. Keep generation, internal links, RSS, structured data, comparison behavior, and analytics tests passing.
3. Isolate the current catalog/affiliate/generator work before any data correction or loading refactor.
4. Fix the confirmed 36 x 36 px Modal close target and establish a reproducible category-payload baseline.
5. Refresh at most 20 high-risk official-source records and change only explicit, verified facts.
6. Publish at most one new guide, with a default target of zero. Publication requires a current query cluster that passes the gate.
7. Resume at most one external channel test only after a qualified attributable outcome or a deliberately approved fresh test.
8. Keep affiliate links disabled until account approval and the existing 100 high-intent-session or 50 Modal-open threshold are documented.

## Non-Negotiable Gates

- **Measurement gate:** no traffic winner, loser, CTR treatment, cluster expansion, or channel expansion without a current aligned window.
- **New-guide gate:** at least 100 current cluster impressions, one click, three related queries, clear intent, and unique decision value.
- **CTR gate:** at least 14 days and the registered sample threshold; otherwise retain `sample_insufficient`.
- **Data gate:** sampled fact error rate below 5%, with method, source, date, and limitations complete.
- **Channel gate:** at least one attributable qualified site event, relevant reply, or citation within 14 days.
- **Affiliate gate:** documented account approval plus 100 high-intent sessions or 50 Modal opens.
- **Cleanup gate:** at most 10 URLs per batch, with evidence, rollback list, and post-change observation.
- **Permission gate:** login, sending, publishing, outreach, paid work, account changes, affiliate activation, and destructive index changes remain `NEEDS_USER`.

## Daily Plan

| Day | Date | Task | Completion standard |
| ---: | --- | --- | --- |
| 1 | 11-18 | Data intake check | Locate a recent aligned GA4/GSC/referring-domain window; if absent, record one blocker and do not substitute old data |
| 2 | 11-19 | Normalize measurement files | Validate dates, dimensions, event names, and totals; reject mixed or partial windows |
| 3 | 11-20 | Rebuild current baseline | Update metrics/status only from accepted exports and preserve the old baseline separately |
| 4 | 11-21 | Close monthly gate | Recalculate traffic, cluster, intent-event, and referring-domain gates; retain `FOCUS` unless evidence passes |
| 5 | 11-22 | Build current GSC queue | Select at most five page/query opportunities from current data; otherwise keep the queue frozen |
| 6 | 11-23 | DABAN experiment review | Judge only if the earliest date and 300-impression threshold are met; otherwise mark sample-insufficient |
| 7 | 11-24 | Week 1 review | Confirm that no growth conclusion used stale or mixed-window data |
| 8 | 11-25 | Working-tree ownership audit | Separate active catalog/affiliate/generator work from maintenance candidates; do not absorb unrelated changes |
| 9 | 11-26 | Modal accessibility fix | Raise the close target to at least 44 x 44 px and verify keyboard, mobile, and visual behavior |
| 10 | 11-27 | Category payload baseline | Record compressed transfer, request count, hydration readiness, and available field CWV evidence |
| 11 | 11-28 | Loading design decision | Compare current loading with a category-scoped or deferred design; choose only a reversible, tested option |
| 12 | 11-29 | Loading prototype or hold | Implement one isolated prototype only if ownership and regression coverage are clear; otherwise document a hold |
| 13 | 11-30 | Performance regression check | Validate deep links, filters, compare state, Modal, analytics, desktop/mobile layout, and resource errors |
| 14 | 12-01 | Week 2 review | Keep or revert the prototype using measured readiness and guardrails, not a single score |
| 15 | 12-02 | Deferred correction source check | Revalidate the Montbell/Aegismax candidates against current official sources |
| 16 | 12-03 | High-risk data sample | Review up to 20 price, weight, availability, and source records across categories |
| 17 | 12-04 | Low-risk data corrections | Correct at most 10 explicit facts; do not infer missing values |
| 18 | 12-05 | Report and page regeneration | Regenerate affected outputs and confirm sitemap/RSS dates only where content truly changed |
| 19 | 12-06 | Image-rights decision packet | Prepare the first high-value guide image specification; image approval or generation remains user-controlled |
| 20 | 12-07 | Discover image implementation or hold | Implement one approved image set with OG/Twitter/Article/max-preview signals, or record `NEEDS_USER` |
| 21 | 12-08 | Week 3 review | Verify data corrections and image work did not alter unrelated pages or index controls |
| 22 | 12-09 | Current CTR experiment setup | Freeze two or three treatment pages only if the Day 5 queue has sufficient current evidence |
| 23 | 12-10 | Search snippet implementation or hold | Apply registered treatments only; if the gate fails, make no substitute bulk rewrite |
| 24 | 12-11 | Citation asset review | Recheck the weight-price report's sources, download, method, and outreach status |
| 25 | 12-12 | Single-channel decision | Resume one channel only if attribution evidence or a fresh owner-approved test exists; otherwise remain stopped |
| 26 | 12-13 | Return-path and crawl check | Validate RSS order, summaries, internal entry points, canonical links, and sitemap inclusion |
| 27 | 12-14 | Production mobile/performance review | Recheck key paths, console/resource errors, touch targets, and available field CWV |
| 28 | 12-15 | Monthly evidence gate | Compare the accepted window with its fixed predecessor; classify metrics without causal overclaiming |
| 29 | 12-16 | Keep/stop/expand audit | Expand only tactics with clicks, qualified use, replies, or citations; list unresolved risks |
| 30 | 12-17 | Next-cycle decision | Produce the final review and ask the owner whether to schedule another cycle |

## Stop List Until Evidence Changes

- Broad product or guide generation.
- A third content cluster.
- New Pinterest/YouTube batches.
- The stale winter sleeping-bag asset.
- Bulk snippet rewriting.
- Large-scale deletion, `noindex`, merging, or redirects.
- Affiliate-link activation or monetization claims.
- Automated email lists, outreach, social posts, or community submissions.

## Expected Deliverables

- Accepted 28-day measurement package or a single explicit `NEEDS_USER` blocker.
- Updated baseline and gate decision when data exists.
- One scoped accessibility fix.
- A category-loading baseline and either one tested prototype or a documented hold.
- Up to 10 verified data corrections.
- At most one approved Discover image implementation.
- At most one registered CTR treatment and one channel test, both conditional.
- Final keep/stop/expand review with no fabricated outcomes.

## Activation Decision

This plan is intentionally not scheduled by Day 30. The owner should choose whether to create a new automation after reviewing the final cycle report and deciding how the GA4/GSC exports will be supplied.
