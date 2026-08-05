# Show HN Draft: Camping Gear Weight and Price Dataset

## Title

Show HN: I analyzed weight and price data for 543 camping products

## Post

I built a downloadable dataset from official product pages to make camping gear
specifications easier to compare across brands.

The cleaned sample has 543 tents, tarps, sleeping bags, sleeping pads and
stoves. One result that surprised me: 68 of the 146 sleeping bags with usable
weight and price data weigh 1 kg or less.

Report and interactive catalog:
https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=hackernews&utm_medium=community&utm_campaign=camping-gear-weight-price-2026&utm_content=show_hn

Download the CSV:
https://www.campgearcompare.com/data/reports/camping-gear-weight-price-2026.csv?utm_source=hackernews&utm_medium=community&utm_campaign=camping-gear-weight-price-2026&utm_content=show_hn_csv

Method: I kept records with positive representative weight and price values,
removed obvious accessories and non-product rows, normalized weights to kg and
retained each price's original currency. Price medians use USD rows only, so GBP
and JPY values are not compared as if they were dollars.

The site is static HTML plus generated catalog pages. I would especially value
feedback on useful filters, questionable normalization choices and additional
export fields.
