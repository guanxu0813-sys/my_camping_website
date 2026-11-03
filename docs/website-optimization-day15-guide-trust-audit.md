# Day 15 catch-up: Guide trust-signal audit

Execution date: 2026-11-03

Scheduled date: 2026-11-02

Status: COMPLETED

## Scope

The audit covered nine high-value published assets in the two clusters already supported by search evidence (Naturehike and Big Agnes), plus the existing weight-price data report. It checked:

- organization author in Article structured data;
- visible reviewer/byline;
- visible review date;
- page-specific method and limitations;
- official source links;
- an explicit bottom-line decision.

The row-level audit is in `docs/website-optimization-day15-guide-trust-audit.csv`.

## Findings

- 9/9 have an organization author in Article structured data.
- 9/9 expose official sources or a reproducible source dataset.
- 6/9 have a visible review date before Day 16.
- 6/9 have page-specific method and limitation wording before Day 16.
- 6/9 have an explicit bottom-line decision before Day 16.
- Only 1/9 has a visible reviewer/byline; most identify CampGear Compare only in structured data.

Three pages have the largest combined gaps:

1. `big-agnes-tiger-wall-ul2-vs-copper-spur-ul2.html`
2. `naturehike-cloud-up-models-compared.html`
3. `naturehike-tuye-r5-8-vs-r6-5-vs-r8-8.html`

## Day 16 selection

The Big Agnes UL2 comparison is the safest single-page update because:

- it belongs to an already-supported Big Agnes cluster;
- it has only two official sources, both currently reachable;
- current official records still match the stored 993 g / 1,188 g weights and $499.95 / $599.95 prices;
- the page lacks a review date, visible reviewer, dedicated verdict and page-specific limitations.

The Cloud Up and Tuye pages remain queued. Their broader or variant-heavy source sets must be refreshed before rewriting claims.
