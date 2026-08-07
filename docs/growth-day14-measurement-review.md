# Day 14 Measurement Protocol Review

Date completed: 2026-08-06 (one day ahead of the V2 calendar)

## Work completed

- Copied the Day 13 GA4, GSC, indexing, sitemap, guide and referring-domain
  baseline into `growth-operations.md`.
- Defined every weekly metric, including the temporary distinction between
  `/guides/` index views and true guide landing sessions.
- Fixed the weekly GSC window to Wednesday through Tuesday, reviewed on
  Thursday, with equal date shifts when reporting is delayed.
- Fixed monthly comparison to adjacent, non-overlapping 28-day windows.
- Documented the filter, denominator and low-base rules that prevent misleading
  percentage or conversion claims.
- Created `growth-experiments.md` with hypothesis, treatment, comparison, start
  date, earliest decision date, sample threshold, status and result fields.
- Registered the Day 10 title/description change as a pre-V2 observation. It has
  no matched control and therefore cannot be presented as a controlled A/B
  result.
- Added maintenance reason codes so factual, legal and technical fixes do not
  need invented growth hypotheses.

## Next fixed measurement

- Review date: 2026-08-13.
- Current GSC window: 2026-08-05 through 2026-08-11.
- Comparison GSC window: 2026-07-29 through 2026-08-04.
- If August 11 is incomplete in GSC, shift both windows backward equally and
  record the dates actually used.

## Day 14 completion check

Day 14 is complete. Future search-facing changes now require either an
experiment ID or a documented maintenance reason before deployment.

Day 15 can begin with the 50-URL A/B/C/D page inventory sample; it should not
apply bulk `noindex` decisions during sampling.
