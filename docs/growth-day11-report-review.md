# Day 11 Weight and Price Report Review

Date completed: 2026-08-05

## Published dataset scope

- 543 included rows across tents, tarps, sleeping bags, sleeping pads and stoves.
- Category counts: 239 tents, 45 tarps, 146 sleeping bags, 93 sleeping pads and 20 stoves.
- Currency counts: 497 USD, 28 GBP and 18 JPY.
- The CSV records `data_reviewed=2026-08-05` on every row.

## Rules checked

- Include only records in the five report categories.
- Exclude records explicitly removed from summary tables.
- Exclude model names identified as accessories, including footprints, inner
  tents, tent poles, pegs, straps, stuff sacks, pumps and repair parts. This
  refresh removed nine accessory records that had leaked into the prior CSV.
- Require positive representative weight and positive reference price.
- Use all included rows for weight medians.
- Use USD rows only for price medians and the $200 threshold; preserve GBP and
  JPY rows in the CSV without applying an exchange rate.

## Distribution assets

- Report: <https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html>
- CSV: <https://www.campgearcompare.com/data/reports/camping-gear-weight-price-2026.csv>
- Data Is Plural URL: <https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=dataisplural&utm_medium=referral&utm_campaign=camping-gear-weight-price-2026&utm_content=submission>
- Show HN URL: <https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=hackernews&utm_medium=community&utm_campaign=camping-gear-weight-price-2026&utm_content=show_hn>

The Data Is Plural submission is tracked in `docs/outreach-log.csv`. The
ready-to-publish Show HN copy is in `docs/outreach/show-hn-camping-gear-report.md`.
