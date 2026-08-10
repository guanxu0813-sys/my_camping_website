# Growth Experiment and Maintenance Register

This register is the audit trail for search-facing changes made under the V2
growth plan. Add the record before deployment, keep the original hypothesis
unchanged, and append results rather than rewriting expectations after seeing
the data.

## Status values

- `planned`: scope is frozen but not deployed.
- `observing`: deployed; the earliest decision date or sample threshold has not
  been reached.
- `sample_insufficient`: the time threshold passed without enough observations.
- `winner`: the primary outcome improved without a material guardrail failure.
- `loser`: the primary outcome worsened or a guardrail failed.
- `inconclusive`: treatment and comparison do not support a useful conclusion.
- `retained` / `reverted`: final implementation action after review.

## Experiment register

| ID | Hypothesis | Treatment group | Comparison group | Primary metric | Guardrails | Start date | Earliest decision | Minimum sample | Status | Result / next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-2026-08-05-CTR-01 | Putting model, product type and decision specifications earlier in titles/descriptions will improve search CTR without materially reducing impressions or average position. | 10 pages listed in `growth-day10-ctr-review.md` | None; this change predates the V2 matched-control rule | Page-level GSC CTR | Impressions and average position | 2026-08-05 | 2026-09-02 | 300 impressions per page | observing | Compare adjacent 28-day windows on or after 2026-09-02. Treat the result as pre/post evidence only, not a controlled A/B result. |
| EXP-2026-08-09-TIGER-01 | Rewriting the first-screen conclusion around capacity and the Standard/Platinum/Bikepack decision will improve search-to-content fit and page-level clicks without materially reducing impressions or average position. | `/guides/big-agnes-tiger-wall-models-compared.html` | `/guides/big-agnes-copper-spur-ul1-vs-ul2.html` remains unchanged | Page-level GSC clicks | Impressions and average position | 2026-08-10 | 2026-09-07 | 300 impressions on both treatment and comparison pages | observing | Keep the title, description, table, internal links and comparison page unchanged through the earliest decision date. |
| EXP-2026-08-10-CTR-02 | Moving the exact model, product type and verified decision specifications into product titles and descriptions will improve group-level organic CTR relative to matched unchanged product pages. | 10 product pages in `growth-day21-controlled-ctr-experiment.md` | 10 matched unchanged product pages in the same file | Group-level GSC CTR | Group impressions and impression-weighted average position | 2026-08-10 | 2026-09-07 | 300 impressions per cohort and at least 3 pages with clicks in each cohort | observing | Keep all treatment and control pages frozen through the earliest decision date. Do not combine this result with the uncontrolled Day 10 cohort. |

## Maintenance log

| ID | Date | Reason code | URLs or files | Change | Verification | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Experiment entry template

Use one row per experiment. Treatment and comparison may link to a separate URL
list when the cohort is too large for the table.

Required fields:

- **ID:** `EXP-YYYY-MM-DD-SHORT-NN`.
- **Hypothesis:** one predicted causal effect, written before implementation.
- **Treatment group:** exact URLs receiving the change.
- **Comparison group:** matched unchanged URLs, or an explicit explanation when
  no valid comparison exists.
- **Primary metric:** one outcome used to decide the experiment.
- **Guardrails:** metrics that must not materially worsen.
- **Start date:** production deployment date, not drafting date.
- **Earliest decision:** normally 28 days for snippet changes and 6 weeks for a
  content cluster.
- **Minimum sample:** normally 300 impressions per page for snippet tests, 100
  cluster impressions plus one click and three queries for expansion, or 100
  qualified sessions / 50 modal opens for conversion tests.
- **Status and result:** preserve `sample_insufficient` when the threshold is not
  met; do not force a winner or loser.

## Maintenance entry template

Maintenance work does not need a growth hypothesis, but it must have a reason,
scope and verification. Allowed reasons:

- `DATA_CORRECTION`: fixes an inaccurate product or editorial fact.
- `BROKEN_LINK`: repairs a failed internal, source or purchase URL.
- `LEGAL_COMPLIANCE`: corrects disclosure, privacy, sponsorship or rights text.
- `ACCESSIBILITY`: fixes keyboard, semantic or assistive-technology behavior.
- `RENDERING_FIX`: repairs a visible layout or interaction defect.
- `SOURCE_REFRESH`: replaces stale official-source information without claiming
  a ranking experiment.
- `SECURITY`: addresses a vulnerability or unsafe dependency/configuration.

For routine content improvement intended to increase clicks, ranking,
engagement or conversion, use an experiment entry instead of a maintenance
reason.
