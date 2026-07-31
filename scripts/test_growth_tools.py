#!/usr/bin/env python3
"""Regression tests for growth, indexing and editorial tooling."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_guides
import build_sitemap
import discover_guide_candidates
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


if __name__ == "__main__":
    unittest.main()
