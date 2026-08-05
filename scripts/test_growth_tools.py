#!/usr/bin/env python3
"""Regression tests for growth, indexing and editorial tooling."""

from __future__ import annotations

import csv
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_guides
import build_sitemap
import discover_guide_candidates
import growth_report
import submit_indexnow


class GrowthToolTests(unittest.TestCase):
    def test_indexnow_maps_public_html(self) -> None:
        base = "https://www.campgearcompare.com"
        self.assertEqual(
            submit_indexnow.html_path_to_url("index.html", base),
            f"{base}/",
        )
        self.assertEqual(
            submit_indexnow.html_path_to_url("guides/index.html", base),
            f"{base}/guides/",
        )
        self.assertIsNone(submit_indexnow.html_path_to_url("404.html", base))
        self.assertIsNone(submit_indexnow.html_path_to_url("data/seo.json", base))

    def test_approved_guide_slugs_and_products_are_unique(self) -> None:
        guides = [
            *build_guides.all_comparison_guides(),
            *build_guides.all_collection_guides(),
        ]
        slugs = [guide["slug"] for guide in guides]
        self.assertEqual(len(slugs), len(set(slugs)))
        known_ids = {
            product["id"] for product in build_sitemap.load_official_products()
        }
        for guide in guides:
            self.assertTrue(guide["takeaways"])
            self.assertTrue(set(guide["product_ids"]).issubset(known_ids))

    def test_candidate_queue_is_review_only_and_excludes_accessories(self) -> None:
        rows = discover_guide_candidates.build_candidates(80)
        self.assertLessEqual(len(rows), 80)
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["review_status"], "candidate")
            self.assertNotRegex(
                row["family"].lower(),
                r"footprint|groundsheet|inner tent|stuff sack|pole kit",
            )

    def test_low_value_accessories_are_not_indexable(self) -> None:
        product = {
            "model": "Alto TR2 Inner Tent Stuff Sack",
            "inSummaryTable": True,
        }
        self.assertTrue(build_sitemap.is_low_value_accessory(product))
        self.assertIsNotNone(
            build_guides.ACCESSORY_PATTERN.search("Ground Control Tent Pegs")
        )

    def test_tent_with_included_footprint_is_not_an_accessory(self) -> None:
        product = {
            "model": "Aurora Backpacking Tent & Footprint",
            "category": "tent",
        }
        self.assertFalse(build_sitemap.is_low_value_accessory(product))

    def test_search_priority_guides_have_reviewed_answers(self) -> None:
        priority_slugs = {
            "naturehike-snowbird-sp700-vs-sp550",
            "naturehike-giling-pro-1-vs-mongar-pro-1",
        }
        guides = {
            guide["slug"]: guide for guide in build_guides.all_comparison_guides()
        }
        for slug in priority_slugs:
            guide = guides[slug]
            self.assertTrue(guide["verdict"])
            self.assertRegex(guide["reviewed_on"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertTrue(guide["limitations"])

        snowbird = guides["naturehike-snowbird-sp700-vs-sp550"]
        self.assertNotIn("1.5 kg", " ".join(snowbird["takeaways"]))

    def test_day_five_copper_spur_guide_is_reviewed_and_connected(self) -> None:
        slug = "big-agnes-copper-spur-ul1-vs-ul2"
        guide = next(
            guide
            for guide in build_guides.all_collection_guides()
            if guide["slug"] == slug
        )
        expected_ids = {
            "big-agnes-copper-spur-ul-one",
            "big-agnes-copper-spur-ul1-bikepack",
            "big-agnes-copper-spur-ul-two",
            "big-agnes-copper-spur-ul2-bikepack",
            "big-agnes-copper-spur-ul-two-xl",
            "big-agnes-copper-spur-ul-three",
            "big-agnes-copper-spur-ul3-bikepack",
            "big-agnes-copper-spur-ul-three-xl",
        }
        self.assertEqual(set(guide["product_ids"]), expected_ids)
        self.assertEqual(guide["brand_id"], "big-agnes")
        self.assertTrue(guide["verdict"])
        self.assertTrue(guide["limitations"])
        self.assertRegex(guide["reviewed_on"], r"^\d{4}-\d{2}-\d{2}$")

        guide_path = f"/guides/{slug}.html"
        for product_id in expected_ids:
            product_links = build_guides.guide_links_by_product()[product_id]
            self.assertIn(guide_path, {path for path, _ in product_links})
        brand_links = build_guides.guide_links_by_brand()["big-agnes"]
        self.assertIn(guide_path, {path for path, _ in brand_links})

    def test_growth_report_prefers_explicit_comparison_periods(self) -> None:
        latest = {
            "gsc_impressions": "1037",
            "comparison_gsc_impressions": "453",
            "comparison_total_visits": "",
        }
        previous = {"gsc_impressions": "879", "total_visits": "4"}
        self.assertEqual(
            growth_report.comparison_number(
                latest, previous, "gsc_impressions"
            ),
            453,
        )
        self.assertIsNone(
            growth_report.comparison_number(latest, previous, "total_visits")
        )

    def test_day_seven_tiger_wall_guide_is_reviewed_and_cross_linked(self) -> None:
        guides = {
            guide["slug"]: guide
            for guide in build_guides.all_collection_guides()
        }
        tiger_slug = "big-agnes-tiger-wall-models-compared"
        copper_slug = "big-agnes-copper-spur-ul1-vs-ul2"
        tiger = guides[tiger_slug]
        copper = guides[copper_slug]
        expected_ids = {
            "big-agnes-tiger-wall-platinum-two-tent",
            "big-agnes-tiger-wall-platinum-three-tent",
            "big-agnes-tiger-wall-ul-one",
            "big-agnes-tiger-wall-ul1-bikepack",
            "big-agnes-tiger-wall-ul-two",
            "big-agnes-tiger-wall-ul2-bikepack",
            "big-agnes-tiger-wall-ul-three",
            "big-agnes-tiger-wall-ul3-bikepack",
        }
        self.assertEqual(set(tiger["product_ids"]), expected_ids)
        self.assertTrue(tiger["verdict"])
        self.assertTrue(tiger["limitations"])
        self.assertEqual(tiger["brand_id"], "big-agnes")
        self.assertIn(
            copper_slug,
            {item["slug"] for item in tiger["related_guides"]},
        )
        self.assertIn(
            tiger_slug,
            {item["slug"] for item in copper["related_guides"]},
        )

        tiger_path = f"/guides/{tiger_slug}.html"
        for product_id in expected_ids:
            product_links = build_guides.guide_links_by_product()[product_id]
            self.assertIn(tiger_path, {path for path, _ in product_links})

    def test_day_eight_down_hugger_guide_preserves_temperature_tiers(self) -> None:
        slug = "montbell-down-hugger-650-models-compared"
        guide = next(
            guide
            for guide in build_guides.all_collection_guides()
            if guide["slug"] == slug
        )
        expected_ids = {
            "montbell-down-hugger-650-2-sunflower",
            "montbell-down-hugger-650-2-long-sunflower",
            "montbell-down-hugger-650-3-balsam",
            "montbell-down-hugger-650-3-long-balsam",
            "montbell-down-hugger-650-5-blue-ridge",
            "montbell-down-hugger-650-5-long-blue-ridge",
        }
        self.assertEqual(set(guide["product_ids"]), expected_ids)
        self.assertEqual(guide["brand_id"], "montbell")
        self.assertTrue(guide["preserve_product_order"])
        self.assertTrue(guide["verdict"])
        self.assertIn("ISO", guide["limitations"])
        self.assertEqual(
            [column["key"] for column in guide["columns"]],
            ["size", "comfortTemp", "lowerLimitTemp", "weight", "price"],
        )

        product_map = {
            product["id"]: product for product in build_sitemap.load_official_products()
        }
        guide_path = f"/guides/{slug}.html"
        for product_id in expected_ids:
            product = product_map[product_id]
            self.assertEqual(product["status"], "verified")
            self.assertIn(product["specs"]["size"], {"Regular", "Long"})
            self.assertTrue(product["specs"]["comfortTemp"])
            self.assertTrue(product["specs"]["lowerLimitTemp"])
            self.assertEqual(build_sitemap.format_capacity_display(product), "")
            product_links = build_guides.guide_links_by_product()[product_id]
            self.assertIn(guide_path, {path for path, _ in product_links})

    def test_day_ten_seo_overrides_cover_ten_gsc_pages(self) -> None:
        overrides = build_sitemap.load_seo_overrides()
        entries = [
            *(overrides.get("pages") or {}).values(),
            *(overrides.get("products") or {}).values(),
            *(overrides.get("brands") or {}).values(),
        ]
        self.assertEqual(len(entries), 10)
        self.assertEqual(overrides["_meta"]["updated"], "2026-08-05")
        self.assertEqual(overrides["_meta"]["reviewAfter"], "2026-09-02")
        for entry in entries:
            self.assertGreaterEqual(len(entry["title"]), 30)
            self.assertLessEqual(len(entry["title"]), 60)
            self.assertGreaterEqual(len(entry["description"]), 120)
            self.assertLessEqual(len(entry["description"]), 160)

        pages = [{"path": "/tent.html", "title": "Old", "description": "Old"}]
        build_sitemap.apply_page_seo_overrides(pages, overrides)
        self.assertEqual(
            pages[0]["title"],
            overrides["pages"]["/tent.html"]["title"],
        )

    def test_day_eleven_report_preserves_currency_boundaries(self) -> None:
        report_path = ROOT / "data" / "reports" / "camping-gear-weight-price-2026.csv"
        with report_path.open(encoding="utf-8", newline="") as report_file:
            rows = list(csv.DictReader(report_file))
        self.assertEqual(len(rows), 543)
        self.assertEqual(
            Counter(row["currency"] for row in rows),
            Counter({"USD": 497, "GBP": 28, "JPY": 18}),
        )
        self.assertTrue(all(row["data_reviewed"] == "2026-08-05" for row in rows))

        report_html = (
            ROOT / "guides" / "camping-gear-weight-price-report-2026.html"
        ).read_text(encoding="utf-8")
        self.assertIn("Median USD Price", report_html)
        self.assertIn("Other currencies remain in the", report_html)


if __name__ == "__main__":
    unittest.main()
