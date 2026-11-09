# Day 22 Image and Discover Readiness Audit

Date: 2026-11-09

## Decision

The nine audited high-value guides are **not image-ready for Google Discover or rich social sharing**. This is a technical and editorial readiness finding, not a prediction that Google Discover will distribute the pages after repair.

## What the audit found

- 9/9 pages declare `twitter:card=summary_large_image`, but 9/9 omit `twitter:image`.
- 9/9 pages omit `og:image`, its dimensions, and an `image` property on Article structured data.
- 9/9 pages omit an explicit `max-image-preview:large` robots directive.
- 8/9 pages have no visible content image, so there is no main-image alt text to evaluate.
- The Mongar Base comparison has two visible images with useful alt text and fixed dimensions, but both are 760x570 remote brand-hosted files. They are below the preferred 1200px width and create availability and rights dependencies.
- The complete URL-level evidence and repair action are in `docs/website-optimization-day22-image-discover-audit.csv`.

## Why this matters

Large, relevant images can improve how eligible pages appear in Discover and social previews. They can also make comparison results easier to scan. Metadata alone does not create eligibility or rankings: the image must be useful, stable, crawlable, and consistent with the page's verified facts.

## Approved implementation order

1. Big Agnes Tiger Wall UL2 vs Copper Spur UL2: the facts and review date were refreshed on Day 16, so it is the safest first implementation.
2. Big Agnes Tiger Wall models compared: historically important to the guide cluster and suitable for one model-matrix image.
3. Naturehike Cloud Up models compared: only after its current official sources are refreshed and approved.
4. Camping Gear Weight and Price Report 2026: use an original chart card generated from the site's own dataset.

The remaining Naturehike pages should not receive promotional graphics until their source refresh is complete. A polished image must not amplify stale specifications.

## Implementation contract

For each approved page, add one meaningful image that:

- is original or properly licensed and at least 1200 pixels wide;
- appears visibly near the page introduction or key conclusion;
- has explicit width and height, descriptive alt text, and a stable first-party URL;
- is referenced by absolute URL in `og:image`, `twitter:image`, and Article `image`;
- includes correct `og:image:width` and `og:image:height` values;
- is paired with `max-image-preview:large` at the shared guide-template level.

Prefer comparison matrices, decision diagrams, and data charts built from verified facts. Do not add generic decorative hero art, copy brand product photography without permission, or depend on third-party hotlinks.

## Boundary and next step

No generated guide HTML or generator was changed today because the guide generation pipeline already contains unrelated uncommitted work. The correct repair belongs in the shared generator plus an approved per-guide image field, not in nine hand-edited output files.

**NEEDS_USER:** finish or commit the concurrent generator work, then approve original/licensed image assets for the first implementation page. Current GA4, GSC, and referring-domain exports are still required before treating these pages as current search winners.
