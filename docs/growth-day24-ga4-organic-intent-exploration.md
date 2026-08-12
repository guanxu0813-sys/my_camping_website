# Day 24 GA4 Organic Intent Exploration

Completed: 2026-08-12

## Saved exploration

- Property: `CampGear Compare` / `露营对比网站`
- Exploration: `Organic High-Intent Weekly`
- Tab: `Qualified organic sessions`
- URL: <https://analytics.google.com/analytics/web/#/analysis/a401856583p546478938/edit/LiCDofpITGeonWDua6ag1g>
- Window: rolling past 28 days; read it once each Thursday while traffic is sparse

## Configuration

Rows, in order:

1. Landing page + query string
2. Session source / medium
3. Event name

Values:

- Sessions
- Event count

Filters:

- Session default channel group exactly matches `Organic Search`
- Event name matches `^(product_modal_open|compare_selected|outbound_click)$`

This prevents direct, referral, email and other channels from being mixed into
the organic high-intent count. Event name remains a row so Modal, Compare and
Outbound are never combined into one unexplained total.

## First reading

Window shown on 2026-08-12: 2026-07-15 through 2026-08-11.

| Signal | Sessions | Events |
| --- | ---: | ---: |
| Event-confirmed organic total | 4 | 7 |
| `outbound_click` | 4 | 5 |
| `product_modal_open` | 1 | 2 |
| `compare_selected` | 0 | 0 |

The event rows can contain the same session, so their session counts must not
be added. The table total is the repeatable event-confirmed organic-session
count. This is a strict subset of the full plan definition, which also allows
engaged qualified landing sessions; keep that broader count separate until a
session-level OR segment is validated.

## Weekly reading

1. Open the saved exploration; do not remove either filter.
2. Confirm the date is a rolling 28-day window ending on the latest fully
   processed day.
3. Record the table's total Sessions and Event count.
4. Record the three event rows separately, including zeroes.
5. Compare with the prior Thursday reading. Use absolute changes; do not treat
   a large percentage from this small baseline as a stable trend.
