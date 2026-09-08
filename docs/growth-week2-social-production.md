# Week 2 — Social Asset Production

Completed: 2026-08-24

## Deliverables

- 15 Pinterest PNGs: 1000 × 1500, three per guide.
- 10 silent caption-first MP4s: 720 × 1280, H.264, 15 seconds, two per guide.
- Five original image-generated backgrounds with deterministic text overlays.
- Rebuild scripts and a single source-of-truth content manifest.

The selected guides cover five distinct distribution hooks: original dataset, lightweight shortlist, head-to-head tent decision, model-family confusion, and cold-weather sleeping-pad decision.

| Asset slug | Destination guide | Pinterest hook | Video hooks |
| --- | --- | --- | --- |
| `gear-report` | `/guides/camping-gear-weight-price-report-2026.html` | 543-product report, weight and $200 benchmarks | category weight gap; tarp median counterexample |
| `tents-under-2kg` | `/guides/2-person-backpacking-tents-under-2kg.html` | 14-model shortlist and lightest records | shortlist summary; weight-filter limitation |
| `lanshan-1-vs-pro` | `/guides/lanshan-1-vs-lanshan-1-pro.html` | 230 g trade-off and wall design | quick verdict; three-step decision |
| `cloud-up-models` | `/guides/naturehike-cloud-up-models-compared.html` | 12-model family and UL 2 | suffix explainer; two-person weight comparison |
| `xlite-vs-xtherm` | `/guides/thermarest-neoair-xlite-vs-xtherm-nxt.html` | 110 g and cold-use trade-off | quick verdict; weight/price comparison |

## Publishing copy

### Gear report

**Pinterest description:** What does “lightweight” actually mean across camping categories? We analyzed 543 catalog products and compared representative weight and reference-price patterns for tents, tarps, sleeping bags, sleeping pads and stoves. Open the methodology and full table.

**Short-video caption:** 543 camping products, five categories, and one important lesson: a weight threshold only makes sense inside its category. Full methodology and downloadable data at CampGear Compare. #campinggear #backpackinggear #outdoordata

### Two-person tents under 2 kg

**Pinterest description:** A data-backed starting list of 14 two-person backpacking tents with listed weights under 2 kg. Compare structure, representative weight and official reference price—then verify floor area, doors, vents and included components.

**Short-video caption:** We found 14 two-person tent records under 2 kg. Weight gets you onto the shortlist; livability and the exact included setup should make the final decision. #ultralight #backpackingtent #campinggear

### Lanshan 1 vs Lanshan 1 Pro

**Pinterest description:** Lanshan 1 or Lanshan 1 Pro? Compare the double-wall standard model with the lighter single-wall Pro, including representative weights, seam preparation and condensation trade-offs.

**Short-video caption:** The Pro can start roughly 230 g lighter, but the real decision is wall design and wet-weather management. Compare the exact fabric and season variant before buying. #lanshan #ultralighttent #backpacking

### Naturehike Cloud Up models

**Pinterest description:** Cloud Up is a model family, not one tent. Compare 12 Base, standard, Pro, UL and EXT records by capacity, representative weight and current official reference price.

**Short-video caption:** First choose 1P, 2P or 3P. Then compare the suffix. Base, Pro, UL and EXT are distinct configurations—not a simple upgrade ladder. #naturehike #cloudup #tentcomparison

### XLite NXT vs XTherm NXT

**Pinterest description:** XLite NXT or XTherm NXT? Compare representative weight, reference price and official positioning. Start with expected overnight temperatures, then decide whether the 110 g difference matters.

**Short-video caption:** XLite NXT is the lighter all-season option; XTherm NXT targets colder-use warmth-to-weight performance. Temperature needs first, grams second. #thermarest #sleepingpad #wintercamping

## UTM convention

Pinterest destination:

```text
https://www.campgearcompare.com/guides/{guide}?utm_source=pinterest&utm_medium=organic_social&utm_campaign=week2_guide_distribution&utm_content={slug}_pin_01
```

Short-video profile or description link:

```text
https://www.campgearcompare.com/guides/{guide}?utm_source={youtube|instagram|tiktok}&utm_medium=organic_video&utm_campaign=week2_guide_distribution&utm_content={slug}_video_01
```

Change only the source, asset number and slug. Keep the campaign name fixed so GA4 can compare channels in one campaign report.

## Seven-day release sequence

1. Day 1: gear-report pin 1 and video 1.
2. Day 2: tents-under-2kg pins 1–2.
3. Day 3: Lanshan pin 1 and video 1.
4. Day 4: Cloud Up pins 1–2 and video 1.
5. Day 5: XLite/XTherm pin 1 and video 1.
6. Day 6: publish the five remaining data/decision pins.
7. Day 7: publish each guide's second video; record impressions, outbound sessions, engaged sessions and key events by UTM content.

Do not publish all variants to the same board or platform at once. Space them out and keep the unposted variants for creative testing.

## Rebuild

```bash
python3 scripts/build_week2_social.py
python3 scripts/encode_week2_social.py
```

The visual backgrounds were generated with the built-in image generation tool. Text and data are rendered locally from `assets/social/week2/content.json`, keeping model names and statistics deterministic.
