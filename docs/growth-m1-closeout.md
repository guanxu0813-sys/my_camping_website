# M1 Closeout and Trigger Register

Closed: 2026-09-07
Scope: Day 14 through Day 43
Status: **M1 operational work complete**

## Closeout result

All repository, measurement, editorial, technical and review deliverables in
M1 are complete. The remaining items below are not daily work left undone.
They depend on an external decision, a future measurement date or a later plan
phase. No time should be spent repeatedly checking them before their trigger.

| Item | Current safe state | Trigger | One next action |
| --- | --- | --- | --- |
| AliExpress affiliate activation | Disabled; empty Tracking ID; zero product mappings; official-brand links remain active | Portal or official email confirms approval, and a valid Tracking ID is available | Manually match 5-10 exact products, test one tracked link and verify GA4 product/platform parameters before enabling anything |
| `EXP-2026-08-12-DATA-01` | Passive observation; three tailored contacts, zero verified replies and zero acquired links | 2026-09-23, or an earlier direct reply/link notification | Read replies, acquired links and report entrances once; mark winner, loser or sample insufficient without sending generic follow-ups |
| D-tier cleanup proposal | Seven conditional candidates; no URL was removed or noindexed | M4 cleanup phase, or a confirmed factual/duplicate-page incident | Refresh GSC and link evidence, correct the source record first, then assess one small batch |
| Prepared social assets | Built and locally QA-checked; publication is not an M1 acceptance criterion | An authenticated publishing session and an approved M2 release slot | Publish one variant at a time and record its UTM result; do not bulk-post all variants |

## Verified safeguards

- `data/affiliates.json` keeps Amazon and AliExpress disabled.
- `data/affiliate-links.json` contains no product mappings.
- The site falls back to official manufacturer destinations when no verified
  affiliate mapping exists.
- Closed outreach and community items are notification-only; recurring manual
  inbox and thread checks have been removed from the operating cadence.
- M2 content expansion is limited to Naturehike and Big Agnes, with a hard cap
  of four new guides and the normal opportunity/data-quality gates.

## Definition of done

M1 is closed without pretending that an external approval or future experiment
result already exists. Any triggered item becomes M2 work and receives a new
dated record. It does not reopen Day 14-43.
