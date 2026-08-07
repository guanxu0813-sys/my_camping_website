# Six-Month Growth Operations

This is the operating checklist for
[`六个月流量增长计划-v2.md`](./六个月流量增长计划-v2.md). It separates code
automation from actions that require the site owner's accounts or editorial
judgment. The V1 cadence stopped after Day 13.

## V2 baseline

Baseline date: 2026-08-06. The source details are recorded in
[`growth-day13-weekly-review.md`](./growth-day13-weekly-review.md).

| Metric | Baseline | Source and scope |
| --- | ---: | --- |
| Total sessions | 39/week (5.57/day) | GA4 past 7 days viewed 2026-08-06 |
| Organic sessions | 17/week (2.43/day) | GA4 Organic Search |
| GSC clicks | 25/week | 2026-07-29 through 2026-08-04 |
| GSC impressions | 1,270/week | Same complete GSC window |
| GSC CTR | 2.0% | Clicks divided by impressions in GSC |
| GSC average position | 16.6 | Property aggregate; not a page decision metric |
| Valid indexed URLs | 453 | Latest available GSC coverage count |
| Local sitemap URLs | 864 | Unique URLs in the three generated child sitemaps |
| Referring domains | 2 | GSC linking sites |
| Published guides | 16 | Guide HTML files excluding the guide index |
| Guide index views | 6 | GA4 views for `/guides/` |
| Product modal opens | 6 | GA4 `product_modal_open` event count |
| Outbound clicks | 6 | GA4 `outbound_click` event count |

The event counts do not share a verified session-level denominator. In
particular, 6 modal opens and 6 outbound clicks must not be reported as a 100%
conversion rate.

## Metric definitions

- **Total sessions/day:** GA4 Sessions for the selected seven days divided by
  seven. Store both the weekly total in notes and the daily rate in
  `total_visits`.
- **Organic sessions/day:** GA4 Sessions where Session default channel group is
  Organic Search, divided by seven.
- **Qualified organic sessions:** Organic Search sessions that land on a guide,
  category, product or comparison page and are engaged or trigger
  `compare_selected`, `product_modal_open` or `outbound_click`. Until the GA4
  exploration is available, report organic sessions and high-intent event
  counts separately.
- **GSC clicks, impressions, CTR and position:** Property-level Web search
  metrics for the fixed complete window. Use page/query rows only for page or
  cluster decisions.
- **Valid indexed URLs:** The latest GSC Page indexing count. Record its report
  date because it can lag deployment.
- **Known URLs:** Unique URLs in `sitemap-core.xml`, `sitemap-brands.xml` and
  `sitemap-products.xml`; this is inventory, not an indexing success metric.
- **Referring domains:** Unique external linking sites shown by GSC Links. Keep
  the external link count in notes.
- **Published guides:** Guide HTML files excluding `/guides/index.html`.
- **Guide entrances:** Until a landing-page exploration is configured, use
  `/guides/` index views and label the metric `guide index views`; do not call
  it landing sessions.
- **Product modal opens / outbound clicks:** GA4 custom event counts for the
  same reporting window. Calculate rates only after a shared session-level
  denominator is available.

## Reporting windows

- Weekly reviews run on Thursday and use the complete Wednesday-to-Tuesday GSC
  window. The first V2 review is 2026-08-13 for 2026-08-05 through 2026-08-11,
  compared with 2026-07-29 through 2026-08-04.
- If GSC has not finished processing Tuesday, shift both seven-day windows back
  by the same number of days and record the actual dates.
- Monthly reviews compare adjacent, non-overlapping 28-day windows ending on a
  Tuesday. Do not sum overlapping weekly rows to create a month.
- Keep search type, country, device and page filters identical across the two
  compared GSC windows. Apply equivalent filters in GA4 where available.
- Always record absolute counts. Percentage change is supporting context and is
  not a decision by itself when the earlier count is small.

## Change accountability

Every search-facing change must have one of these records before deployment:

1. An experiment ID in [`growth-experiments.md`](./growth-experiments.md), with
   a hypothesis, treatment, comparison, start date and earliest decision date.
2. A maintenance entry in the same document using one of these reason codes:
   `DATA_CORRECTION`, `BROKEN_LINK`, `LEGAL_COMPLIANCE`, `ACCESSIBILITY`,
   `RENDERING_FIX`, `SOURCE_REFRESH` or `SECURITY`.

Routine regeneration that produces no source or rendered-content change does
not need an entry. If a change has both maintenance and growth goals, record it
as an experiment and mention the maintenance reason in its notes.

## Weekly cadence

### Thursday — fixed-window measurement

1. Use a complete Wednesday-to-Tuesday GSC window and compare it with the
   immediately preceding, non-overlapping seven days.
2. Record GA4 total, organic and qualified organic sessions with matching
   filters where available.
3. Add one row to `docs/growth-metrics.csv` and run
   `python3 scripts/growth_report.py --month N`.
4. Record absolute values as well as percentages; do not treat low-base growth
   percentages as stable trends.
5. Update each active experiment as observing, sample-insufficient, winner or
   loser.

### Monday to Wednesday — winner improvement

1. Run `python3 scripts/discover_guide_candidates.py`.
2. Improve pages already earning impressions, clicks, relevant links or
   high-intent events before creating a new page.
3. Score candidate topics with the V2 18-point opportunity model.
4. Approve at most one new guide per week, only at 11 points or higher with no
   data blocker.
5. Add original takeaways, authorship, methodology, sources and limitations;
   never publish a raw generated table.

### Friday — quality and CTR

1. Run:
   `python3 scripts/validate_official.py --quality-report data/reports/product-quality-audit.csv`.
2. Verify the highest-risk and GSC-priority records against official sources.
3. Change only the pages assigned to an active experiment; preserve matched
   controls.
4. Evaluate title and description changes only after 28 days and at least 300
   impressions per page. Otherwise mark the result sample-insufficient.

### Weekend — distribution

1. Answer one or two relevant community questions without unsolicited link
   drops.
2. Send up to three personalized editor or brand emails tied to one useful
   asset or data point.
3. Update `docs/outreach-log.csv` immediately.
4. Refresh one existing guide or the downloadable data report.

## UTM convention

Use lowercase values and retain the same campaign name for one asset:

- `utm_source`: `reddit`, `hackernews`, `dataisplural`, `indiehackers`,
  `brand_email`, `editor_email`, or the referring publication.
- `utm_medium`: `social`, `community`, `referral`, or `email`.
- `utm_campaign`: stable asset slug, for example
  `camping-gear-weight-price-2026`.
- `utm_content`: post, comment, email or placement identifier.

Example:

`https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=dataisplural&utm_medium=referral&utm_campaign=camping-gear-weight-price-2026&utm_content=submission`

## Monthly decision gate

- Compare adjacent, non-overlapping 28-day windows; do not use a weekly peak as
  the monthly result.
- Expand a cluster only after six weeks or once it has at least 100 impressions,
  one click and three related queries.
- If a cluster has no signal after eight weeks, update, merge or stop it rather
  than creating more variants.
- Judge an outreach channel only after 20 high-quality attempts or four weeks.
- Evaluate a conversion experiment only after 100 qualified sessions or 50
  product modal opens.
- Keep sitemap size separate from effective indexing and search demand.

## Manual account actions

The following cannot be completed by repository code:

- Submit and inspect sitemaps inside Google Search Console.
- Import the site into Bing Webmaster Tools and inspect IndexNow receipts.
- Send email from the owner's mailbox.
- Publish Reddit, forum, Product Hunt or other community posts.
- Read the private GA4 dashboard.

Do not store account passwords, API credentials or email subscriber addresses in
the repository.
