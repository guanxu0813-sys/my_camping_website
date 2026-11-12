# Day 25: Pinterest and YouTube attribution review

Date: 2026-11-12
Status: completed; both channels are stop candidates pending current evidence

## Decision

Pause production and publication of new Pinterest and YouTube assets. Keep the seven existing published assets online; do not delete or edit them in bulk. Neither channel has met the SOP continuation gate of at least one attributable qualified event, reply, citation, or documented site visit within 14 days.

This is a **lack-of-evidence decision**, not proof that every asset produced exactly zero sessions. The local records do not contain a GA4 UTM export, so blank `qualified_visits` cells remain unknown rather than being converted to zero.

## What was verified

- Three published Pins and four published YouTube Shorts were consolidated from the publication and execution records. Duplicate execution rows for the Cloud Up Short were treated as one published asset.
- Every asset has a unique `utm_content` value and a specific landing page.
- All seven reconstructed UTM landing URLs returned HTTP 200 on 2026-11-12.
- The three Pinterest records had 11 combined observed views and zero recorded Pin outbound clicks as of 2026-09-20.
- Two YouTube records had 166 combined observed views and zero comments as of 2026-09-20. The later two Shorts have publication confirmation but no saved outcome snapshot.
- No local report verifies Pinterest or YouTube sessions containing `catalog_search`, `product_modal_open`, `compare_selected`, or `outbound_click`.
- The complete asset-level evidence is in `docs/website-optimization-day25-channel-attribution.csv`.

## Attribution gaps

1. The current local GA4 data ends on 2026-09-01, before these assets were published. It cannot measure these campaigns.
2. Pinterest uses multiple historical medium names (`organic`, `organic_social`, and `organic_pin`), while YouTube uses both `shorts` and `organic_video`. This fragments channel reporting even though the individual links are valid.
3. The Cloud Up Short relies on a channel-profile UTM, but the records do not prove how long that exact profile link remained active.
4. Views, saves, comments, and video completion are diagnostic platform metrics. They are not qualified site visits.

Do not retroactively rewrite live campaign links just to make the naming consistent. For any future approved test, freeze one convention before publication: `pinterest / organic_social` and `youtube / organic_video`, with a unique campaign and content value per asset.

## Channel actions

### Pinterest

- Stop creating additional near-duplicate Pins.
- Keep the three published Pins live as passive assets.
- Do not publish the two prepared Big Agnes variants until a current GA4 acquisition export is available and a single new test has a defined measurement window.

### YouTube Shorts

- Pause new Shorts production and do not expand a Short into long-form content yet.
- Keep the four published Shorts live.
- Before another test, use one stable channel-profile landing URL with a unique UTM and record its activation dates. A description URL alone should not be treated as verified referral traffic.

## Required user evidence

Export GA4 for 2026-09-08 through the latest complete date with these dimensions and metrics:

- session source / medium;
- session campaign;
- session manual ad content (UTM content), if available;
- landing page plus query string;
- sessions, engaged sessions and key events;
- `catalog_search`, `product_modal_open`, `compare_selected`, and `outbound_click` counts.

If the export shows at least one qualified event or clearly attributable engaged session for an asset, move only that topic/channel out of `STOP_CANDIDATE`. Otherwise close the channel test and redirect production time to current-source updates, search-intent work, and relevant citations.

Day 17 and Day 23 remain separately blocked by the same missing current GA4/GSC evidence. Day 20 remains blocked by concurrent uncommitted generator work; none of those files were changed in this review.
