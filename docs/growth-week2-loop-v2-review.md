# Week 2 Loop-v2 Review

Date: 2026-08-27

## Acceptance gates

1. Pinterest headline remains readable at a simulated 160 px mobile width.
2. Each pin contains one decision, one supporting statistic or rule, and one CTA.
3. Every Short opens with a question, mistake, risk, or counterintuitive fact during the first three seconds.
4. Every Short contains continuous background motion, animated text entry/exit, four distinct information stages and a progress bar.
5. Every factual phrase listed in `source_checks` must occur verbatim in its destination guide before the build starts.
6. All 15 images and all 10 videos must be visually inspected. All videos must also decode end-to-end.
7. Each asset has an independent UTM content value and an explicit test variable.

## Loop record

### Round 1 — audit

- Found that the first delivery optimized for asset count rather than user decisions.
- Pinterest cards contained report-style headings and too much secondary copy.
- Videos were static slides stored in MP4 containers, not meaningfully animated Shorts.
- No deterministic source gate or per-asset experiment matrix existed.

Result: failed; full redesign required.

### Round 2 — data gate and rebuild

- Rewrote 15 pins around explicit choices, trade-offs or buying risks.
- Added exact-string source validation against all five guide files.
- The first build stopped when one tent-livability validation phrase did not exactly match the guide.
- Corrected the source check without weakening it and rebuilt.
- Replaced slide videos with 18-second, 12 fps animated sequences using continuous pan/zoom, text transitions, four stages and progress indication.

Result: implementation passed; visual review still required.

### Round 3 — camper and marketer review

- Downscaled every pin to 160 px wide and inspected all 15 together.
- Decoded all 10 videos from start to finish and inspected four moments from each video.
- Camper view: decisions were clearer, but several opening hooks still read like report titles.
- Marketer view: first-three-second questions existed, but loss-aversion and myth-breaking hooks could be stronger.

Result: failed messaging gate; hook revision required.

### Round 4 — hook revision and final QA

- Replaced generic hooks with mistake, risk or counterintuitive framing.
- Added 25 platform-specific publishing rows with copy, UTMs and test hypotheses.
- Rebuilt every affected asset and repeated mobile, motion, duration and decode checks.

Result: passed.

- All 15 pins remained readable in the 160 px mobile-width contact sheet.
- All 10 videos decoded end-to-end and were visually reviewed at four points in their timelines.
- All videos are 720 × 1280, H.264 and exactly 18 seconds.
- Same-scene pixel-motion checks passed for all 10 videos using textured top and bottom background regions.
- The source gate passed for every declared fact across all five guides.
- The publishing matrix contains 25 rows and 25 unique `utm_content` URLs.
- Site analytics tests, 14 Python growth-tool tests, generated-site validation and `git diff --check` passed.

No fifth loop was needed because every acceptance gate passed in Round 4.

## Experiment interpretation

- Pinterest A/B/C primarily compares decision framing, numerical proof and risk/myth framing.
- Shorts A/B compares counterintuitive or loss-avoidance hooks against direct question/rule hooks.
- Primary metric: outbound engaged sessions by `utm_content`.
- Secondary metrics: saves for Pinterest; three-second retention and average percentage viewed for Shorts.
- Do not choose a winner from impressions alone.
