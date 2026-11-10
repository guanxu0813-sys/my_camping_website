# Day 24: citable-data editorial shortlist

Prepared: 2026-11-11 (Asia/Shanghai)
Status: offline drafts only; no contact made

## Asset and limits

- Public report: https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html
- Downloadable CSV: https://www.campgearcompare.com/data/reports/camping-gear-weight-price-2026.csv
- Both URLs were checked as available on 2026-11-11 (report readable; CSV returned HTTP 200).
- The report covers **541 catalog records** from the **2026-08-15** snapshot. Prices and product availability may have changed. It is not a market-representative survey or hands-on testing. USD price calculations exclude non-USD records.
- Three different publications are listed below; none appears in `docs/outreach-log.csv` as a previous recipient. A prepared draft is not a sent message, a reply, or an earned backlink.

## Shortlist and tailored drafts

### 1. SectionHiker (Philip Werner)

Fit: Its [2026 double-wall backpacking tent guide](https://sectionhiker.com/ultralight-backpacking-double-wall-tent-guide-2026/) tabulates model weight and price. The independent catalog sample could be useful as background on why a category-wide tent median should not be read as an ultralight tent median. Its [contact page](https://sectionhiker.com/got-a-backpacking-hiking-or-camping-question/) allows serious gear/media inquiries but explicitly rejects paid links and guest-post pitches. **Do not frame this as a link request.**

Draft for manual review, not submitted:

> Subject: A catalog-data caveat for tent weight comparisons
>
> Hi Philip, I run CampGear Compare. Your double-wall tent guide makes the weight/price trade-off easy to inspect. I built a downloadable catalog snapshot that includes 239 tent records, with a 2.65 kg median representative weight. That figure deliberately includes car-camping and larger shelters, so it should **not** be treated as a benchmark for ultralight backpacking tents. The underlying rows and category filters may still be useful if you are researching how product mix changes a comparison.
>
> Report: https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=sectionhiker&utm_medium=contact_form&utm_campaign=camping-gear-data-2026&utm_content=day24_data_note
>
> CSV: https://www.campgearcompare.com/data/reports/camping-gear-weight-price-2026.csv
>
> This is an August 15 catalog snapshot from brand listings, not field testing or a current price feed. No action needed if it is not useful. Best, Guanxu

### 2. GearLab (Zach Lovell / camping-gear editors)

Fit: Its [2026 backpacking tent review](https://www.outdoorgearlab.com/topics/camping-and-hiking/best-backpacking-tent) reports **measured** trail and packaged weights. That is materially different from our brand-listed representative weights, so the pitch offers a comparison caveat, not an attempt to replace their testing. Its [feedback route](https://www.outdoorgearlab.com/feedback) accepts comments and has CAPTCHA; submission requires the owner.

Draft for manual review, not submitted:

> Subject: Brand-listed versus measured tent weights: a small data note
>
> Hi GearLab team, I run CampGear Compare and appreciated that your 2026 tent review separates measured minimum trail weight from packaged weight. Our downloadable August 15 catalog snapshot records brand-listed representative weights and USD reference prices for 239 tents. It is a different kind of evidence and should not be substituted for your measured values, but the rows may help show why weight labels and product mix need careful interpretation.
>
> Report and limits: https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=gearlab&utm_medium=contact_form&utm_campaign=camping-gear-data-2026&utm_content=day24_data_note
>
> CSV: https://www.campgearcompare.com/data/reports/camping-gear-weight-price-2026.csv
>
> No placement or link is requested. If useful for future background research, the underlying rows are open to inspect. Best, Guanxu

### 3. BIKEPACKING.com (gear editorial desk)

Fit: Its [Dragonfly Bikepack OSMO tent review](https://bikepacking.com/gear/2026-nemo-dragonfly-bikepack-osmo-tent-review/) discusses packed weight, price and the practical value of a handlebar-specific bag. Our dataset cannot evaluate bikepacking fit, but it provides a separately labeled catalog price/weight backdrop. Its [content suggestion form](https://bikepacking.com/contribute/suggestions/) accepts gear-related tips, requires CAPTCHA and notes a mailing-list opt-in; owner must decide whether to submit.

Draft for manual review, not submitted:

> Subject: A limited catalog reference for tent weight and price
>
> Hi BIKEPACKING.com gear team, I run CampGear Compare. Your Dragonfly Bikepack OSMO review makes clear that packed weight alone does not capture pole length, handlebar storage, or riding practicality. I maintain a downloadable 2026-08-15 snapshot of listed weights and USD reference prices across camping categories. It cannot answer those bikepacking-specific questions or replace field testing, but the tent rows may provide background when contrasting bikepacking-specific models with general shelters.
>
> Report and method: https://www.campgearcompare.com/guides/camping-gear-weight-price-report-2026.html?utm_source=bikepacking&utm_medium=contact_form&utm_campaign=camping-gear-data-2026&utm_content=day24_data_note
>
> CSV: https://www.campgearcompare.com/data/reports/camping-gear-weight-price-2026.csv
>
> The catalog is not a current price feed or a representative market survey. Please ignore if it does not fit your coverage. Best, Guanxu

## Release gate

Do not submit these as a batch. Before any individual contact, the owner should check the publication's current submission rules, inspect the relevant sample rows and source URLs, and decide whether the August snapshot is still useful. One appropriate note per recipient at most; no paid placement, reciprocal-link request, or automatic follow-up. If approved and sent, add a real `sent` row with date and actual channel to `docs/outreach-log.csv`; otherwise leave it untouched.

Day 23's search-title experiment has no completed log row. The latest local GSC window still ends 2026-09-01, so its high-impression/low-CTR treatment group cannot be chosen as a current experiment. Do not label Day 23 complete or start its 14-day clock from this draft. Day 17's GA4/GSC/referring-domain gate and Day 20's isolated data corrections remain blocked for the reasons in their respective reports.
