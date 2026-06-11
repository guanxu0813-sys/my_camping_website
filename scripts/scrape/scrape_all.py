#!/usr/bin/env python3
"""Run scrape_brand.py for every brand in config.yaml."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_config  # noqa: E402

SCRAPE_SCRIPT = Path(__file__).resolve().parent / "scrape_brand.py"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Batch-scrape all configured brands",
        epilog=(
            "If scraping fails with SSL or proxy errors, try:\n"
            "  env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy "
            "python3 scripts/scrape/scrape_all.py"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "brands",
        nargs="*",
        help="Brand keys to scrape (default: all brands in config.yaml)",
    )
    parser.add_argument(
        "--continue",
        dest="continue_on_error",
        action="store_true",
        help="Keep scraping remaining brands after a failure",
    )
    args = parser.parse_args()

    all_brands = load_config()
    keys = args.brands if args.brands else sorted(all_brands.keys())
    failed: list[str] = []

    for key in keys:
        if key not in all_brands:
            print(f"Unknown brand {key!r}", file=sys.stderr)
            failed.append(key)
            continue
        print(f"\n========== {key} ==========", flush=True)
        result = subprocess.run([sys.executable, str(SCRAPE_SCRIPT), key], check=False)
        if result.returncode != 0:
            failed.append(key)
            if not args.continue_on_error:
                return result.returncode

    if failed:
        print(f"\nFailed brands: {', '.join(failed)}", file=sys.stderr)
        return 1
    print(f"\nDone. Scraped {len(keys) - len(failed)} brand(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
