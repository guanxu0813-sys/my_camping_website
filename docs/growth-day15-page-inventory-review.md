# Day 15 Page Inventory and Tier Sample

Date completed: 2026-08-07 (one day ahead of the V2 calendar)

## Sources

- Local indexable inventory: 864 unique URLs from the three generated child
  sitemaps (28 core, 66 brand and 770 product URLs).
- GSC performance: 2026-07-08 through 2026-08-04, Web search, 403 page rows with
  at least one reported impression.
- GSC Page indexing: 453 valid indexed URLs; example groups showed 89
  `Crawled - currently not indexed` and 303 `Discovered - currently not
  indexed` URLs.
- The Page indexing report was last updated 2026-07-24. Its example URLs were
  read on 2026-08-07, so these statuses are retained as dated snapshots rather
  than claimed as live inspection results.

Machine-readable sample:
[`growth-page-sample-2026-08-07.json`](../data/reports/growth-page-sample-2026-08-07.json)

## Sample design

The 50-URL sample deliberately mixes page types and evidence states:

| Dimension | Count |
| --- | ---: |
| Guides | 8 |
| Core/category pages | 7 |
| Brand pages | 8 |
| Product pages | 27 |
| Search-visible through GSC impressions | 35 |
| Older not-indexed coverage examples | 15 |

The 35 search-visible pages are the highest-impression pages within the chosen
type quotas. The 15 coverage examples include 10 crawled and 5 discovered
product URLs that had no row in the complete 28-day performance table.

## Initial tiers

| Tier | Count | Day 15 interpretation |
| --- | ---: | --- |
| A | 22 | Existing click or at least 10 impressions at positions 4-20 |
| B | 6 | At least 10 impressions, no click and positions 21-50 |
| C | 7 | Fewer than 10 impressions; sample is too small for action |
| D | 15 | No performance row, older not-indexed example and incomplete normalized data |

These are sampling tiers, not permanent SEO directives. In particular, D does
not authorize `noindex`, deletion or sitemap removal. Day 16 must manually
review quality, intent, source completeness and uniqueness before recommending
any action.

## Notable signals

- Product pages account for 345 of the 403 GSC page rows, while only 12 guide
  pages and 37 brand pages had impressions. Product discovery is broad, but
  most rows remain very small.
- The strongest sampled guide is Fire-Maple FMS-300T vs Hornet II with 2 clicks,
  13 impressions and 15.4% CTR at position 9.5.
- The strongest sampled product is Naturehike Mongar Base 3 with 4 clicks and
  82 impressions at position 8.6.
- The home page averaged position 5.3 across 76 impressions but had no click;
  its query mix must be checked before treating this as a snippet problem.
- Ten of the 15 D pages were crawled examples. Several descriptions contain
  specifications that have not been normalized into comparison fields, which
  gives Day 16 a concrete quality-audit target.

## Day 16 handoff

Review 20 pages without changing indexability:

1. Ten A/B pages with the largest impressions or clearest search opportunity.
2. Five C pages to determine whether low volume is normal or caused by weak
   intent coverage.
3. Five D pages to verify data accuracy, source quality, uniqueness and whether
   the page deserves to remain indexable.

Record factual error rate, duplicate patterns and the five highest-risk issues.
Do not use URL Inspection on all sample pages and do not request bulk indexing.
