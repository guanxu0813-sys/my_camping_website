#!/usr/bin/env python3
"""Render monthly growth gates from the manually updated metrics CSV."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "docs" / "growth-metrics.csv"
DEFAULT_OUTPUT = ROOT / "docs" / "growth-status.md"
VISIT_GATES = {
    1: (20, 50),
    2: (50, 150),
    3: (150, 400),
    4: (300, 800),
    5: (600, 1500),
    6: (1000, 3000),
}


def number(row: dict, key: str) -> float | None:
    value = str(row.get(key, "")).strip().replace("%", "")
    try:
        return float(value) if value else None
    except ValueError:
        return None


def percent_change(current: float | None, previous: float | None) -> str:
    if current is None or previous in (None, 0):
        return "n/a"
    return f"{((current - previous) / previous) * 100:+.1f}%"


def gate_decision(rows: list[dict], month: int) -> tuple[str, list[str]]:
    latest = rows[-1]
    previous = rows[-2] if len(rows) > 1 else {}
    notes: list[str] = []
    partial_period = "partial" in str(latest.get("period", "")).lower()
    visits = number(latest, "total_visits")
    low, high = VISIT_GATES.get(month, VISIT_GATES[6])
    if partial_period:
        notes.append(
            "GA4 covers only a partial baseline period: collect seven complete days "
            "before applying the M1 traffic gate."
        )
    elif visits is None:
        notes.append("Fill total_visits from GA4 before making a traffic decision.")
    elif visits < low:
        notes.append(
            f"Traffic is below the M{month} lower gate ({low}/day): pause broad page expansion."
        )
    elif visits <= high:
        notes.append(f"Traffic is inside the M{month} target range ({low}–{high}/day).")
    else:
        notes.append("Traffic is above the monthly stretch gate; expand the winning cluster.")

    current_impressions = number(latest, "gsc_impressions")
    previous_impressions = number(previous, "gsc_impressions")
    if (
        current_impressions is not None
        and previous_impressions not in (None, 0)
        and current_impressions < previous_impressions * 1.3
    ):
        notes.append(
            "GSC impressions grew less than 30%: prioritize quality, intent and relevant links."
        )
    clicks = number(latest, "gsc_clicks")
    if month >= 3 and clicks is not None and clicks < 200:
        notes.append(
            "M3+ search clicks are below the plan gate: stop publishing unvalidated clusters."
        )
    decision = "BASELINE" if partial_period else "CONTINUE" if not any(
        phrase in " ".join(notes)
        for phrase in ("pause broad", "stop publishing")
    ) else "FOCUS"
    return decision, notes


def render(rows: list[dict], month: int) -> str:
    latest = rows[-1]
    previous = rows[-2] if len(rows) > 1 else {}
    decision, notes = gate_decision(rows, month)
    metrics = [
        ("Total visits/day", number(latest, "total_visits"), number(previous, "total_visits")),
        ("Organic visits/day", number(latest, "organic_visits"), number(previous, "organic_visits")),
        ("GSC clicks", number(latest, "gsc_clicks"), number(previous, "gsc_clicks")),
        ("GSC impressions", number(latest, "gsc_impressions"), number(previous, "gsc_impressions")),
        ("Indexed URLs", number(latest, "indexed_urls"), number(previous, "indexed_urls")),
        ("Referring domains", number(latest, "referring_domains"), number(previous, "referring_domains")),
        ("Published guides", number(latest, "published_guides"), number(previous, "published_guides")),
    ]
    metric_lines = "\n".join(
        f"- {label}: {current if current is not None else 'not entered'} "
        f"(change {percent_change(current, prior)})"
        for label, current, prior in metrics
    )
    action_lines = "\n".join(f"- {note}" for note in notes)
    return (
        "# CampGear Compare Growth Status\n\n"
        f"Generated: {date.today().isoformat()}\n"
        f"Measurement row: {latest.get('date', '')} ({latest.get('period', '')})\n"
        f"Plan month: M{month}\n"
        f"Decision: **{decision}**\n\n"
        "## Metrics\n"
        f"{metric_lines}\n\n"
        "## Gate actions\n"
        f"{action_lines}\n\n"
        "## Operating rule\n"
        "Expand only clusters that already earn impressions, clicks, qualified referral "
        "traffic, or relevant links. If the decision is FOCUS, spend the next cycle on "
        "data quality, intent matching, CTR and distribution instead of URL growth.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--month", type=int, choices=range(1, 7), default=1)
    args = parser.parse_args()
    with args.input.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"No measurement rows in {args.input}")
    args.output.write_text(render(rows, args.month), encoding="utf-8")
    print(f"Wrote growth gate report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
