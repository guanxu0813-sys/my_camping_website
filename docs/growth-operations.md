# Six-Month Growth Operations

This is the operating checklist for the approved growth plan. It separates code
automation from actions that require the site owner's accounts or editorial
judgment.

## Weekly cadence

### Monday — measurement

1. Export the latest GSC pages and queries.
2. Record Plausible total and organic visits.
3. Add one row to `docs/growth-metrics.csv`.
4. Run `python3 scripts/growth_report.py --month N`.
5. Select three topics only from queries or product families already showing
   demand.

### Tuesday to Thursday — editorial production

1. Run `python3 scripts/discover_guide_candidates.py`.
2. Review candidate sources, variants and search intent.
3. Move only approved topics into `data/guide-approvals.json`.
4. Add original takeaways and limitations; do not publish a raw generated table.
5. Run the catalog and sitemap builds before deployment.

### Friday — quality and CTR

1. Run:
   `python3 scripts/validate_official.py --quality-report data/reports/product-quality-audit.csv`.
2. Verify the highest-risk and GSC-priority records against official sources.
3. Update up to ten high-impression, low-CTR entries in
   `data/seo-overrides.json`.
4. Record the change date; evaluate after four weeks, not the next day.

### Weekend — distribution

1. Answer two relevant community questions without unsolicited link drops.
2. Send up to five personalized editor or brand emails.
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

- If GSC impressions have not grown at least 30% across the last four comparable
  weeks, stop broad page expansion.
- If a cluster has no impressions after eight weeks, update or merge it rather
  than creating more variants.
- If a cluster reaches positions 8–30, prioritize better copy, internal links and
  relevant citations.
- Expand a cluster only when it produces impressions, qualified referral visits,
  backlinks or repeat visitors.

## Manual account actions

The following cannot be completed by repository code:

- Submit and inspect sitemaps inside Google Search Console.
- Import the site into Bing Webmaster Tools and inspect IndexNow receipts.
- Send email from the owner's mailbox.
- Publish Reddit, forum, Product Hunt or other community posts.
- Read Plausible's private dashboard.

Do not store account passwords, API credentials or email subscriber addresses in
the repository.
