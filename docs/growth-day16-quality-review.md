# Day 16 Quality Baseline Review

Date completed: 2026-08-07 (two days ahead of the V2 calendar)

## Scope and method

Twenty pages were selected from the Day 15 sample: 10 A/B pages, 5 C pages
and 5 D pages. Each page was reviewed for search intent, data accuracy, unique
value, source traceability and a useful next step. This was a rendered-page
review, not a word-count test.

The five D products were checked against their current official product pages.
No URL was deleted, no `noindex` was added and no indexing request was made.

Machine-readable audit:
[`growth-page-audit-2026-08-07.json`](../data/reports/growth-page-audit-2026-08-07.json)

## Baseline

| Measure | Result | Meaning |
| --- | ---: | --- |
| Pages with an inaccurate rendered claim | 8/20 (40%) | All eight sampled product pages use an invalid mixed-currency price benchmark; four also have direct source mismatches. |
| Pages with direct official-source mismatches | 4/20 (20%) | NANGA, Naturehike Morning View, Montbell and Lanshan 1 Pro need record-level correction. |
| Pages passing all five criteria | 2/20 (10%) | The two complete comparison guides, S02 and S08, are the quality reference. |
| Pages without a direct official link | 10/20 (50%) | One shortlist guide, six category pages and three brand pages require an extra click through a product page to reach the source. |
| Pages with a clear next step | 20/20 (100%) | Internal navigation is the strongest shared quality signal. |

The factual error rate is page-based: a page counts once if any rendered claim
is contradicted by an official source or is generated with an invalid method.
This avoids making a page with several bad fields dominate the percentage.

## Confirmed source mismatches

| Page | Local claim | Official evidence | Decision |
| --- | --- | --- | --- |
| NANGA Level 8 -20 | 0.75 kg; -20 C comfort | About 1.54 kg total; -11 C comfort and -20 C lower limit | Correct before further promotion. |
| Naturehike Morning View King | 1-person; 5.8 kg without qualification | 200 x 180 cm king size; prose says 5.9 kg while variant data says 5.8 kg | Remove the 1-person value and disclose the weight basis. |
| Montbell Burrow Bag #5 Long | Down fill; no temperature rating | EXCELOFT synthetic; 8 C comfort and 4 C lower limit | Correct fill and add both temperature labels. |
| 3F UL Gear Lanshan 1 Pro | Highlight says double-wall; 169 USD | Official page says single-wall; current product options reach 179 USD | Correct the highlight and refresh price with variant context. |

The Big Agnes page's current 699.95 USD price and two-person positioning were
confirmed. Its source page did not expose a readable weight specification in
this review, so the local 0.99 kg value is not marked confirmed or disproved.

## Repeated content patterns

1. All eight sampled product pages repeat the same generated summary,
   percentile paragraph, similar-weight table and related-model block.
2. The price paragraph compares raw numbers across USD, GBP and JPY, then labels
   the mixed median using the current product's currency.
3. The six category pages are dominated by a large table using the same shell;
   row-level source dates and official links are absent.
4. The three brand pages mostly repeat a short introduction, product list and
   cross-category links, with little brand-specific decision guidance.
5. Scraped official descriptions are often copied or truncated instead of
   being converted into consistently labelled comparison fields.

## Five highest-risk issues

| Priority | Risk | Evidence | Next action |
| --- | --- | --- | --- |
| P0 | Mixed-currency price claims are mathematically invalid | 8/8 sampled product pages | Remove the claim until medians are currency-normalized or currency-specific. |
| P0 | Semantic extraction can pass validation while remaining wrong | 4/5 D products have a confirmed mismatch | Add checks for total versus fill weight, comfort versus limit temperature, capacity and construction type. |
| P1 | Large tables lack row-level source traceability | 10/20 pages have no direct official link | Add compact source/date access without overwhelming the comparison workflow. |
| P1 | Brand pages provide too little unique decision value | 3/3 sampled brand pages are mostly generated lists | Add verified brand scope, strongest categories and meaningful model-group guidance only where evidence exists. |
| P1 | Category pages present volume before guidance | Six sampled category pages open into 21-276 model tables | Add concise filters, data-date context and intent-specific entry points before expanding inventory. |

## Day 15 correction

Day 15 described the five selected D records as lacking normalized comparison
fields. Day 16 found that all five do contain normalized weight, price and
currency fields. Their real problem is semantic accuracy, freshness and weak
validation, not simple field absence. The D tier remains useful as an audit
queue, but it must not be interpreted as a missing-field label.

## Day 17 handoff

Keep the four directly inaccurate D products out of new editorial promotion
until their records are corrected. Use the complete 28-day GSC export to build
query clusters, but do not let impressions override these quality findings.
The product price benchmark is a maintenance fix, not a title experiment.
