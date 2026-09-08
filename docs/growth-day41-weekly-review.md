# Day 41 Weekly and M1 Measurement Review

Review completed: 2026-09-07
Weekly window: 2026-08-26 to 2026-09-01
M1 measurement window: 2026-08-05 to 2026-09-01
Decision: **FOCUS**

## Fourth fixed-window review

The weekly windows are adjacent and non-overlapping. GSC data was complete
through September 5 when the export was downloaded on September 7.

| Metric | Aug 19-25 | Aug 26-Sep 1 | Change |
| --- | ---: | ---: | ---: |
| GA4 sessions | 47 | 42 | -10.6% |
| GA4 Organic Search sessions | 24 | 23 | -4.2% |
| GA4 engaged sessions | 15 | 17 | +13.3% |
| GA4 engaged Organic Search sessions | 11 | 13 | +18.2% |
| GA4 events | 223 | 187 | -16.1% |
| GA4 key events | 2 | 2 | no change |
| `product_modal_open` | 0 | 2 | +2 |
| `compare_selected` | 0 | 0 | no change |
| `outbound_click` | 2 | 2 | no change |
| GSC clicks | 33 | 22 | -33.3% |
| GSC impressions | 1,456 | 1,521 | +4.5% |
| GSC CTR | 2.27% | 1.45% | -0.82 pp |
| GSC average position | 18.0 | 19.3 | worsened 1.3 |

The final week added visibility and more engaged organic sessions, but fewer
clicks and a lower CTR. Two modal opens and two outbound clicks are useful
signals, but the report does not prove that those events came from organic
sessions.

## Complete M1 window

This 28-day window is the four complete Wednesday-to-Tuesday weeks used by the
V2 reviews. It is used instead of a partial calendar window so the weekly and
monthly numbers reconcile exactly.

| Metric | M1 absolute result |
| --- | ---: |
| GA4 sessions | 174 |
| GA4 Organic Search sessions | 93 |
| GA4 engaged sessions | 75 |
| GA4 engaged Organic Search sessions | 53 |
| GA4 events | 794 |
| GA4 key events | 6 |
| `product_modal_open` | 2 |
| `compare_selected` | 0 |
| `outbound_click` | 6 |
| GSC clicks | 105 |
| GSC impressions | 5,693 |
| GSC CTR | 1.84% |
| GSC average position | 16.2 |

The three high-intent event rows total eight events, not eight unique sessions.
They must not be added to the 53 engaged organic sessions because sessions can
overlap and event channel attribution has not been validated. Organic Search
recorded two key events during the 28 days.

## Cluster gate

Cluster totals use every GSC page row whose URL belongs to the named brand.
Related-query counts use the visible query export and are privacy-suppressed,
so they establish a minimum rather than a complete query total.

| Cluster | Clicks | Impressions | Weighted position | Related queries visible | Gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Naturehike | 52 | 2,522 | 8.95 | more than 3 | pass |
| Big Agnes | 15 | 434 | 16.81 | more than 3 | pass |
| Montbell | 3 | 52 | 10.46 | 1 | observe |
| 3F UL Gear / Lanshan | 0 | 80 | 54.31 | more than 3 | observe |

Naturehike and Big Agnes both exceed 100 impressions, one click and three
related queries. They are the only clusters approved for M2 expansion.

## Authority and quality guardrails

- GSC Links still shows 14 external links from two referring domains: GitHub
  and Pinterest. Authority did not broaden during M1.
- The broad Day 16 audit found inaccurate rendered claims on 8 of 20 pages
  (40%). The later Day 36 targeted re-audit passed 10 of 10 representative
  pages after two stale price/description corrections, for a current sampled
  error rate of 0%.
- The 0% result is a regression check, not proof that all 864 sitemap URLs are
  accurate. The original broad quality risk remains a reason to cap expansion.
- GSC Page indexing remains 724 indexed URLs from the latest available report;
  current local sitemap inventory is 865 URLs.

## Decision

M1 satisfies the minimum evidence gate for a narrow M2: four fixed-window
reviews exist, two clusters pass the expansion threshold, the latest structured
sample has no errors, and no new severe indexing or structured-data issue was
found. The decision remains **FOCUS**, not broad expansion.
