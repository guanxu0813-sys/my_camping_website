#!/usr/bin/env python3
"""Build a private, non-indexed draft of the winter sleeping-bag data asset."""

from __future__ import annotations

import csv
import html
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "data" / "reports" / "winter-sleeping-bag-candidate-sample.csv"
OUTPUT = ROOT / "docs" / "drafts" / "winter-sleeping-bag-data-asset.html"
SNAPSHOT_DATE = "2026-10-29"
DRAFT_DATE = "2026-10-30"
CURRENCY_SYMBOLS = {"USD": "$", "GBP": "£", "JPY": "¥"}
BRAND_COLORS = {"Naturehike": "#24735b", "NANGA": "#b44b36", "Montbell": "#345aa8"}


def load_eligible_rows(path: Path = SAMPLE) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    return [row for row in rows if row["eligibility"] == "eligible"]


def temperature_band(value: float) -> str:
    if value <= -10:
        return "≤ -10°C"
    if value <= -5:
        return "-9.9 to -5°C"
    if value <= 0:
        return "-4.9 to 0°C"
    return "0.1 to 5°C"


def format_price(row: dict) -> str:
    currency = row["currency"]
    price = float(row["reference_price"])
    decimals = 0 if currency == "JPY" else 2
    return f"{CURRENCY_SYMBOLS.get(currency, '')}{price:,.{decimals}f} {currency}"


def scatter_chart(rows: list[dict]) -> str:
    width, height = 760, 390
    left, right, top, bottom = 64, 22, 28, 54
    plot_width = width - left - right
    plot_height = height - top - bottom
    min_temp, max_temp = -25.0, 5.0
    min_weight, max_weight = 0.5, 3.1

    def x_pos(value: float) -> float:
        return left + (value - min_temp) / (max_temp - min_temp) * plot_width

    def y_pos(value: float) -> float:
        return top + (max_weight - value) / (max_weight - min_weight) * plot_height

    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Listed comfort temperature and weight</title>',
        '<desc id="chart-desc">Scatter plot of 27 draft candidates. Each point represents one product and is colored by brand.</desc>',
        f'<rect x="{left}" y="{top}" width="{plot_width}" height="{plot_height}" fill="#fbfbf8" stroke="#c7c9c3"/>',
    ]
    for temp in (-25, -20, -15, -10, -5, 0, 5):
        x = x_pos(float(temp))
        parts.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" stroke="#dedfd9"/>')
        parts.append(f'<text x="{x:.1f}" y="{height-bottom+23}" text-anchor="middle">{temp}°C</text>')
    for weight in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        y = y_pos(weight)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#dedfd9"/>')
        parts.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end">{weight:.1f}</text>')
    parts.append(f'<text x="18" y="{top + plot_height/2:.1f}" transform="rotate(-90 18 {top + plot_height/2:.1f})" text-anchor="middle">Weight (kg)</text>')
    for row in rows:
        temp = float(row["comfort_c"])
        weight = float(row["weight_kg"])
        color = BRAND_COLORS.get(row["brand"], "#555")
        label = html.escape(f'{row["brand"]} {row["model"]}: {temp:g}°C, {weight:g} kg')
        parts.append(f'<circle cx="{x_pos(temp):.1f}" cy="{y_pos(weight):.1f}" r="5" fill="{color}" fill-opacity="0.8"><title>{label}</title></circle>')
    parts.append('</svg>')
    return "".join(parts)


def table_for_currency(currency: str, rows: list[dict]) -> str:
    sorted_rows = sorted(rows, key=lambda row: (float(row["comfort_c"]), row["brand"], row["model"]))
    body = []
    for row in sorted_rows:
        lower = html.escape(row["lower_limit_label"] or "Not listed")
        status = html.escape(row["catalog_status"])
        body.append(
            "<tr>"
            f'<td>{html.escape(row["brand"])}</td>'
            f'<td><a href="{html.escape(row["official_source"], quote=True)}">{html.escape(row["model"])}</a></td>'
            f'<td>{html.escape(row["comfort_label"])}</td>'
            f'<td>{lower}</td>'
            f'<td>{float(row["weight_kg"]):g} kg</td>'
            f'<td>{format_price(row)}</td>'
            f'<td><span class="status status-{status}">{status}</span></td>'
            "</tr>"
        )
    median_price = statistics.median(float(row["reference_price"]) for row in rows)
    median_weight = statistics.median(float(row["weight_kg"]) for row in rows)
    summary_row = {"currency": currency, "reference_price": str(median_price)}
    return (
        f'<section><h2>{currency} records</h2>'
        f'<p>{len(rows)} records. Median listed weight: {median_weight:g} kg. '
        f'Median reference price within {currency}: {format_price(summary_row)}. '
        'This price summary is not compared with other currencies.</p>'
        '<div class="table-wrap"><table><thead><tr><th>Brand</th><th>Model and official source</th>'
        '<th>Listed comfort label</th><th>Lower limit</th><th>Weight</th><th>Reference price</th><th>Review state</th>'
        f'</tr></thead><tbody>{"".join(body)}</tbody></table></div></section>'
    )


def render_html(rows: list[dict]) -> str:
    brands = Counter(row["brand"] for row in rows)
    currencies = Counter(row["currency"] for row in rows)
    statuses = Counter(row["catalog_status"] for row in rows)
    bands = Counter(temperature_band(float(row["comfort_c"])) for row in rows)
    lower_limit_count = sum(bool(row["lower_limit_label"]) for row in rows)
    legend = "".join(
        f'<span><i style="background:{color}"></i>{html.escape(brand)} ({brands[brand]})</span>'
        for brand, color in BRAND_COLORS.items()
        if brand in brands
    )
    band_items = "".join(
        f'<li><strong>{html.escape(label)}</strong><span>{bands[label]} records</span></li>'
        for label in ("≤ -10°C", "-9.9 to -5°C", "-4.9 to 0°C", "0.1 to 5°C")
    )
    currency_tables = "".join(
        table_for_currency(currency, [row for row in rows if row["currency"] == currency])
        for currency in ("USD", "GBP", "JPY")
        if currencies[currency]
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>Draft: Cold-weather sleeping bags by comfort label and weight</title>
  <style>
    :root {{ color-scheme: light; --ink:#1f2521; --muted:#5c655f; --line:#d8dad5; --paper:#fff; --wash:#f3f5f1; --accent:#24735b; --warning:#8b3f2c; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; color:var(--ink); background:var(--wash); font:16px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ width:min(1180px,calc(100% - 32px)); margin:0 auto; padding:32px 0 64px; }}
    .draft-banner {{ padding:12px 16px; border:2px solid var(--warning); background:#fff1ed; font-weight:750; }}
    header,section {{ padding:28px 0; border-bottom:1px solid var(--line); }} h1 {{ max-width:880px; margin:14px 0 10px; font-size:clamp(2rem,4vw,3.4rem); line-height:1.05; }} h2 {{ font-size:1.55rem; }}
    .lede {{ max-width:850px; color:var(--muted); font-size:1.08rem; }} .facts {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin:24px 0; }}
    .fact {{ padding:16px; border-left:4px solid var(--accent); background:var(--paper); }} .fact strong {{ display:block; font-size:1.55rem; }} .fact span {{ color:var(--muted); }}
    .bands {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; padding:0; list-style:none; }} .bands li {{ padding:14px; background:var(--paper); border:1px solid var(--line); }} .bands span {{ display:block; color:var(--muted); }}
    .chart {{ overflow:auto; padding:12px; background:var(--paper); border:1px solid var(--line); }} .chart svg {{ display:block; min-width:680px; width:100%; height:auto; }} .chart text {{ fill:#4e5651; font-size:12px; }}
    .legend {{ display:flex; flex-wrap:wrap; gap:16px; margin:12px 0; }} .legend span {{ display:flex; align-items:center; gap:7px; }} .legend i {{ width:12px; height:12px; border-radius:50%; }}
    .table-wrap {{ overflow-x:auto; border:1px solid var(--line); background:var(--paper); }} table {{ width:100%; min-width:1040px; border-collapse:collapse; }} th,td {{ padding:10px 12px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }} th {{ background:#e9eee9; }} a {{ color:#145d49; }}
    .status {{ white-space:nowrap; font-weight:700; }} .status-draft {{ color:var(--warning); }} .status-verified {{ color:var(--accent); }} .note {{ padding:16px; border-left:4px solid var(--warning); background:#fff8f4; }} code {{ background:#e8ebe7; padding:2px 5px; }}
    @media (max-width:760px) {{ main {{ width:min(100% - 20px,1180px); padding-top:12px; }} .facts,.bands {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} h1 {{ font-size:2rem; }} }}
  </style>
</head>
<body><main>
  <div class="draft-banner">PRIVATE DRAFT — NOT APPROVED FOR PUBLICATION</div>
  <header>
    <p>Seasonal data asset · draft built {DRAFT_DATE}</p>
    <h1>Cold-weather sleeping bags by listed comfort label and weight</h1>
    <p class="lede">A reproducible review draft covering products with an explicit comfort label of 5°C or colder. It describes the current catalog; it does not rank warmth, value, or real-world performance.</p>
    <div class="facts">
      <div class="fact"><strong>{len(rows)}</strong><span>draft candidates</span></div>
      <div class="fact"><strong>{len(brands)}</strong><span>brands</span></div>
      <div class="fact"><strong>{statuses['verified']}</strong><span>catalog-verified rows</span></div>
      <div class="fact"><strong>{lower_limit_count}</strong><span>separate lower-limit labels</span></div>
    </div>
    <p class="note"><strong>Review gate:</strong> {statuses['draft']} of {len(rows)} rows still have draft catalog status. Do not publish, cite, or use this page for purchase claims until Day 13 source verification is complete and the factual error rate is below 5%.</p>
  </header>
  <section>
    <h2>What the labels show</h2>
    <ul class="bands">{band_items}</ul>
    <p>Comfort labels are copied from stored official product records. A lower-limit label is shown separately when available and must not be presented as routine sleeping comfort. Individual warmth varies with shelter, pad insulation, clothing, humidity, physiology, and test method.</p>
  </section>
  <section>
    <h2>Comfort label and listed weight</h2>
    <div class="legend">{legend}</div>
    <div class="chart">{scatter_chart(rows)}</div>
    <p>The chart is descriptive only. Weight and a listed temperature do not establish insulation quality or suitability for a person or trip.</p>
  </section>
  {currency_tables}
  <section>
    <h2>Method and limitations</h2>
    <ol>
      <li>Read the existing official-product catalog snapshot and keep sleeping bags with an explicit Celsius comfort value.</li>
      <li>Reject Fahrenheit/Celsius pairs differing by more than 2°C, records warmer than 5°C, and records missing positive weight, price, or official source URL.</li>
      <li>Keep USD, GBP, and JPY records separate. No exchange-rate conversion or cross-currency price ranking is performed.</li>
      <li>Plot listed comfort temperature against representative catalog weight; preserve the original temperature label in the table.</li>
    </ol>
    <p><strong>Source snapshot:</strong> {SNAPSHOT_DATE}. <strong>Draft generated:</strong> {DRAFT_DATE}. Rebuild with <code>python3 scripts/build_winter_sleeping_bag_draft.py</code>.</p>
    <p><strong>Known limitations:</strong> this is a selected catalog, not a complete market sample. Product variants, regional availability, testing standards, fit, fill characteristics, and current prices may differ. Official links are retained for manual Day 13 verification.</p>
  </section>
</main></body></html>
'''


def write_draft(rows: list[dict], output: Path = OUTPUT) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(rows), encoding="utf-8")


def main() -> int:
    rows = load_eligible_rows()
    if not rows:
        raise SystemExit("No eligible rows found; run the Day 11 sample generator first")
    write_draft(rows)
    print(
        f"Wrote {OUTPUT}: {len(rows)} draft candidates, "
        f"{len({row['brand'] for row in rows})} brands, "
        f"currencies={dict(sorted(Counter(row['currency'] for row in rows).items()))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
