# Day 4 Product Quality Review

Review date: 2026-08-01  
Input: top 25 rows from `data/reports/product-quality-audit.csv` generated before corrections.

## Outcome

- Reviewed: 25/25 records against each product's official URL.
- Corrected: 20 records, covering weight, price, capacity, temperature, or product type.
- No change: 5 records where the stored value matched the visible official page or the page did not expose a reliable replacement value.
- Indexing rule: a complete tent sold with an included footprint is no longer treated as a footprint accessory.

## Review Log

| # | Product | Decision | Evidence and action |
|---:|---|---|---|
| 1 | Naturehike Giling Pro 1 | No change | Official title and stored tent type/specs agree. |
| 2 | Naturehike Snowbird SP700 | Corrected | Official size table lists M at 1,200 g and variants from $159 to $199.99; changed weight and price range. |
| 3 | Naturehike Mongar Base 3 | No change | Official page agrees with the stored three-person tent record. |
| 4 | Naturehike PeakLite YL01 table | Corrected | Official copy lists 3.9 lb and $59.99; changed 2.15 kg to 1.77 kg and price to $59.99. |
| 5 | Naturehike Mongar Pro 1 | No change | Official page agrees with the stored one-person tent record. |
| 6 | Naturehike Snowbird SP550 | Corrected | Product title states 29.3°F / -1.5°C; fixed the truncated `3°F` temperature value. |
| 7 | Sea to Summit Ground Control Light Pegs, used | Corrected | Official page lists six 7 g pegs and $0 for an unavailable used item; changed pack weight to 0.042 kg and type to accessory. Kept zero price because it is the official displayed state. |
| 8 | Flame's Creed 210 x 150 groundsheet | Corrected | Official page identifies a 0.3 kg groundsheet; added weight/description and changed type from tarp to accessory. Price remains zero because no reliable current sale price is shown. |
| 9 | Sea to Summit Alto TR1 stuff sack | Corrected | Official breadcrumb and copy identify a $35 replacement stuff sack; changed type to spare part and removed it from comparison surfaces. |
| 10 | Sea to Summit Alto TR2 stuff sack | Corrected | Same verified spare-part treatment as TR1. |
| 11 | Sea to Summit Ground Control Tent Pegs | Corrected | Official page lists an eight-pack at 14 g per peg and $33.95; changed pack weight to 0.112 kg and type to accessory. |
| 12 | Sea to Summit Ground Control Light Pegs | Corrected | Official page lists six 7 g pegs and $21.95; changed pack weight to 0.042 kg and type to accessory. |
| 13 | Sea to Summit Telos TR2 stuff sack | Corrected | Official page identifies a $35 replacement stuff sack; changed type to spare part and removed it from comparison surfaces. |
| 14 | Sea to Summit Telos TR3 stuff sack | Corrected | Official page identifies a $35 replacement stuff sack; changed type to spare part and removed it from comparison surfaces. |
| 15 | Flame's Creed Glamping Tarp Screen | No change | Official URL was checked but did not expose stable weight or price data; retained the record for a later source refresh rather than inventing values. |
| 16 | Flame's Creed 90% duck-down sleeping bag | No change | Official URL was checked but did not expose a reliable variant weight/price; variants cannot safely share one inferred value. |
| 17 | Flame's Creed Taiji 2 | Corrected | Official specifications list 2.5 kg and two users; added weight, capacity, and a concise description. |
| 18 | Flame's Creed TrailStar | Corrected | Official specifications list 0.5 kg and one-to-two-person use; added weight and capacity. |
| 19 | Flame's Creed 20D zippered rainfly/tarp tent | Corrected | Official specifications list 0.75 kg and one-to-two-person use; added weight and capacity. |
| 20 | AEGISMAX sleeping-bag stuff sack | Corrected | Official title/copy explicitly say the sleeping bag is not included; changed type to accessory and removed it from comparison surfaces. Weight remains unset because the page gives no reliable value. |
| 21 | Flame's Creed Lanshan 2 | Corrected | Official description lists 1,155 g and two-person capacity; added both structured values. |
| 22 | Flame's Creed Lanshan 1 | Corrected | Official description lists 845 g and one-person capacity; added both structured values. |
| 23 | Flame's Creed Lanshan 2 Pro | Corrected | Official description lists 1,050 g and two-person capacity; added both structured values. |
| 24 | NEMO Aurora Backpacking Tent & Footprint | Corrected | Official page sells a complete 2- or 3-person tent with a footprint included; kept it as a tent, added capacity, and exempted this bundle wording from accessory detection. Weight remains unset because the visible page does not provide a stable value. |
| 25 | NEMO Dragonfly Bikepack OSMO Footprint | Corrected | Official page identifies a standalone 1- or 2-person footprint; changed type to accessory and removed it from comparison surfaces. Weight remains unset because the visible page does not provide it. |

## Official Sources

- Naturehike: product URLs recorded on each reviewed row in the audit CSV.
- Sea to Summit: `seatosummit.com/products/...` URLs recorded in the audit CSV.
- Flame's Creed and AEGISMAX: official store product URLs recorded in the audit CSV.
- NEMO Aurora and Dragonfly Footprint: official `nemoequipment.com/products/...` pages recorded in the audit CSV.
