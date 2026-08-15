# Day 36 Structured Data Audit

Date: 2026-08-15  
Status: **Complete**

## Result

Ten representative pages passed the reusable audit in
`scripts/audit_structured_data.py`. The machine-readable result is stored at
`data/reports/growth-day36-structured-data-2026-08-15.json`.

| Sample | Expected structured data | Result |
| --- | --- | --- |
| 4 product pages | Product + BreadcrumbList | Pass |
| 4 guide pages | Article + BreadcrumbList | Pass |
| Naturehike tent brand page | CollectionPage + BreadcrumbList | Pass |
| Tent category page | CollectionPage + ItemList + BreadcrumbList | Pass |

The audit verifies canonical URLs, visible H1/name or headline agreement,
positive Offer prices, three-letter currencies, HTTPS offer URLs, article
author and dates, breadcrumb completeness, and the absence of unsupported
rating or review fields.

## Corrections Made

- 3F UL Gear Lanshan 1 Pro: updated the official reference price from $169 to
  $179 and corrected the old `double-wall` highlight to `single-wall`.
- Big Agnes Tiger Wall 2 Platinum: updated the official list/reference price
  from $699.95 to $649.95 and synchronized the reviewed Tiger Wall guide.
- Naturehike Mongar Base 3 remains at the $159 list/reference price; the
  manufacturer's temporary $149 sale is not presented as the stable reference
  price.

Official pages checked:

- https://3fulgear.com/product/ultralight-tent/lanshan-1-pro/
- https://www.bigagnes.com/products/tiger-wall-platinum-two-tent
- https://www.naturehike.com/products/mongartm-base-3-person-ultralight-backpacking-tent
- https://www.naturehike.com/products/giling-protm-1-person-backpacking-tent

## Guardrail

No `aggregateRating`, `review` or `ratingValue` is emitted for these samples.
CampGear Compare does not convert manufacturer reviews into its own rating.
