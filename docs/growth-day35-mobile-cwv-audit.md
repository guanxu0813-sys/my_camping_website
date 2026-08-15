# Day 35 Mobile Experience and CWV Signal Audit

Date: 2026-08-15  
Status: **Complete**

## Scope

Tested at a 390 x 844 mobile viewport, with representative desktop checks at
1280 x 800:

- Core: `/index.html`, `/guides/index.html`
- Category: `/tent.html`, `/sleeping-pad.html`
- Guide: `/guides/camping-gear-weight-price-report-2026.html`, `/guides/naturehike-giling-pro-1-vs-mongar-pro-1.html`
- Product: `/products/naturehike-mongartm-base-3-person-ultralight-backpacking-tent.html`, `/products/montbell-seamless-alpine-burrow-bag-5-long-blue-ridge.html`

## Results

- All eight mobile samples stayed within the 390 px document width.
- Wide comparison tables remained inside their intentional horizontal scroll wrappers.
- Above-the-fold images rendered in the representative category and product checks.
- No console errors were recorded on the eight samples.
- The four representative desktop checks had no unintended document-level horizontal overflow.

## Core Mobile Flow

On `/tent.html`, searched for `Mongar`, selected two exact products, and used
`Compare selected`. The result changed to a two-row comparison and the control
changed to `Show all`. The workflow is complete on a phone without a blocked
action.

## CWV Signal Note

Google PageSpeed Insights was requested for the live homepage on 2026-08-15,
but the public API returned HTTP 429 `RESOURCE_EXHAUSTED` before providing field
or Lighthouse data. This audit therefore does not invent LCP, INP or CLS values.
The available proxy checks found no layout overflow, visible image failure,
console error or interaction blocker. Field CWV must still be read from GSC or
PageSpeed Insights when Google exposes enough data.

## Decision

No broad CSS or JavaScript refactor is justified by this sample. Preserve the
current responsive table pattern and revisit only if GSC field CWV or user
sessions identify a specific failing template.
