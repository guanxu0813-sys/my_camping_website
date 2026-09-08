# Week 1 — Conversion Measurement Foundation

Completed: 2026-08-24

## Outcome

The site now measures the actions that matter before active promotion starts:

| User action | GA4 event | Suggested key event? |
| --- | --- | --- |
| Runs a comparison with two or more products | `compare_selected` | Yes |
| Selects or removes an item from comparison | `compare_item_toggle` | No; diagnostic funnel step |
| Clicks a merchant, brand, sponsor, or other external link | `outbound_click` | Yes |
| Opens a product detail modal | `product_modal_open` | No |
| Searches, filters, or sorts the catalog | `catalog_search`, `brand_filter`, `table_sort` | No |
| Requests email updates | `newsletter_signup_intent` | Yes, but treat as an intent until a mailing provider confirms the address |
| Opens another contact email link | `email_contact` | Optional |
| Shares or downloads a guide | `guide_share`, `guide_download` | Optional |

Outbound measurement now covers every external HTTP(S) link rather than only links carrying a small set of CSS classes. Share buttons remain separate so one click is not counted twice. Useful dimensions include `link_type`, `destination_host`, `link_text`, `product_id`, `category`, and `page`.

## Newsletter limitation

There is no mailing-list provider or subscriber database configured in this repository. The footer form therefore opens the visitor's email application with a prefilled opt-in request. The event is deliberately named `newsletter_signup_intent`; it does not claim a confirmed subscription. Replace this handoff with a provider API before scaling paid traffic, then add a server-confirmed `newsletter_signup` event.

## GA4 administration checklist

These settings live in the GA4 property and cannot be applied by static site code:

1. In **Admin → Data display → Events**, confirm the new events arrive after deployment.
2. Mark `compare_selected`, `outbound_click`, and `newsletter_signup_intent` as key events.
3. Create event-scoped custom dimensions for `link_type`, `destination_host`, `product_id`, and `category` if breakdowns are needed in reports.
4. Build a funnel exploration: `page_view` → `product_modal_open` or `compare_item_toggle` → `compare_selected` → `outbound_click`.
5. Keep internal/developer traffic excluded from campaign decisions.

## Campaign reporting rule

Every active-promotion URL should include `utm_source`, `utm_medium`, `utm_campaign`, and `utm_content`. Evaluate channels by engaged sessions and key-event rate, not clicks alone. Paid promotion should wait until production GA4 shows at least one test event for each of the three recommended key events.

## Verification

Run:

```bash
npm test
```

The test loads the local catalog in jsdom, accepts analytics consent, exercises the product modal, outbound click, search, filter, sort, comparison funnel, and newsletter form, then verifies the expected GA4 event names in `dataLayer`. It requires no network connection or local server.
