# CampGear Compare — Sponsorship Pricing Sheet

**Effective:** June 2026  
**Currency:** USD  
**Contact:** [guanxu0813@gmail.com](mailto:guanxu0813@gmail.com)

All prices are **per calendar month** unless noted. Prices exclude applicable taxes. Invoices due **Net 15** unless otherwise agreed in writing.

---

## Standard placements

| SKU | Placement | Includes | List price (USD/mo) | Best for |
|-----|-----------|----------|--------------------:|----------|
| **SP-TABLE** | Table Featured Row | First row in one category compare table; “Sponsored” badge; row highlight; Modal disclosure on that SKU | **$400** | Flagship tent/tarp/sleeping bag launch |
| **SP-MODAL** | Modal Featured | Sponsored badge + disclosure in product modal only (no table pin) | **$200** | Secondary SKU or long-tail model |
| **SP-BANNER** | Brand Banner | Logo + short copy + CTA on home or one category page header | **$650** | Brand awareness, collection push |
| **SP-INSIGHT** | Category Insights Report | One-time PDF: spec/price landscape + optional site mention | **$1,200** | Product planning, retail decks |

### Category multipliers (Table Featured)

Base price **SP-TABLE** = $400/mo. Adjust by category traffic potential:

| Category | Multiplier | Adjusted SP-TABLE |
|----------|:----------:|------------------:|
| Tents | 1.0× | $400 |
| Sleeping bags | 0.9× | $360 |
| Tarps | 0.75× | $300 |
| Furniture | 0.75× | $300 |

---

## Bundles *(recommended)*

| Bundle | Contents | List price | You save |
|--------|----------|-------------:|---------:|
| **Launch Pack** | SP-TABLE (1 category) + SP-MODAL (1 additional SKU) | **$520/mo** | ~13% |
| **Category Domination** | SP-TABLE × 2 categories (e.g. tent + sleeping bag) | **$720/mo** | 10% |
| **Brand Presence** | SP-BANNER + SP-TABLE (1 category) | **$950/mo** | ~12% |
| **Quarterly Table** | SP-TABLE × 1 category × 3 months prepaid | **$1,080** | 10% |

---

## Founding Partner pilot *(first 3 brands)*

| Benefit | Detail |
|---------|--------|
| Discount | **25% off** list price, months 1–3 |
| Add-on | **Free SP-MODAL** with any SP-TABLE booking |
| Term | 3-month minimum; converts to standard pricing unless renewed |
| Example | Tents Table Featured: $400 → **$300/mo** + free Modal on second SKU |

Pilot slots are allocated **first signed, first served**.

---

## Add-ons

| Add-on | Price | Notes |
|--------|------:|-------|
| Extra pinned SKU (same category) | +$150/mo | Max 2 sponsored rows per category table |
| Category Insights Report | $1,200 | Standalone or bundled at $999 with 6+ mo sponsorship |
| Dedicated outbound UTM + monthly stats email | $0 | Included for all paid campaigns |
| Rush launch (< 3 business days) | +$100 one-time | Subject to asset readiness |

---

## Eligibility & exclusions

**Eligible**

- Brand must have products in our official catalog for the chosen category.
- Sponsored SKU must use **verified** or **published** data where possible.
- Brand provides written approval for campaign assets (see agreement §4).

**Not eligible / we reserve the right to decline**

- Placements that imply false “#1” rankings or altered specs.
- Categories we do not yet publish (unless pre-agreed launch date).
- Competitor bidding war on the same single row *(first contract wins; waitlist available)*.

---

## Campaign mechanics (technical)

| Field | Purpose |
|-------|---------|
| `productId` | Official catalog ID for pinned SKU |
| `tier` | `table-featured` or `modal-featured` |
| `label` | Default `Sponsored` (custom label by request, e.g. `Partner`) |
| `expiresAt` | Auto-removal date (YYYY-MM-DD) |
| `campaignId` | Your internal PO / campaign reference |

Config lives in `data/sponsors.json`; changes propagate within one deploy cycle.

---

## Payment & cancellation

| Term | Policy |
|------|--------|
| **Billing** | Monthly in advance, or quarterly prepay (10% discount) |
| **Payment methods** | Bank transfer (USD), PayPal, Wise *(specify in agreement)* |
| **Cancellation** | Either party: **14 days’ written notice** before next billing period |
| **Early termination by Publisher** | Pro-rata refund for unused full months if we cannot deliver placement |
| **Early termination by Sponsor** | No refund for current period; optional kill fee for custom creative |

---

## Rate card summary (quick reference)

| Placement | Low | Mid *(list)* | High |
|-----------|----:|-------------:|-----:|
| Table Featured / category / mo | $300 | **$400** | $500 |
| Modal Featured / mo | $150 | **$200** | $300 |
| Brand Banner / mo | $500 | **$650** | $800 |
| Insights Report / project | $1,000 | **$1,200** | custom |

*Mid column = default quote. Use category multipliers and bundles when preparing proposals.*

---

## Related documents

- One-pager for brands: [`media-kit-one-pager.md`](./media-kit-one-pager.md)
- Contract template: [`sponsorship-agreement-template.md`](./sponsorship-agreement-template.md)
- Internal roadmap: [`../monetization-plan.md`](../monetization-plan.md)
