# CampGear Compare

**CampGear Compare** — [campgearcompare.com](https://www.campgearcompare.com)

Side-by-side camping gear spec comparisons from official brand data. Sort tents, tarps, sleeping bags, and camp furniture by weight, capacity, materials, and reference price.

## Live site

https://www.campgearcompare.com

## Categories

| Page | URL |
|------|-----|
| Home | https://www.campgearcompare.com/ |
| Tents | https://www.campgearcompare.com/tent.html |
| Tarps | https://www.campgearcompare.com/tarp.html |
| Sleeping bags | https://www.campgearcompare.com/sleeping-bag.html |
| Furniture | https://www.campgearcompare.com/furniture.html |

## Development

Static site (HTML, CSS, vanilla JS). No build step required for local preview:

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

After editing official product JSON:

```bash
python3 scripts/build_catalog.py
python3 scripts/build_sitemap.py
python3 scripts/validate_official.py --quality-report data/reports/product-quality-audit.csv
python3 scripts/discover_guide_candidates.py
python3 scripts/growth_report.py --month 1
python3 scripts/test_growth_tools.py
```

`build_sitemap.py` also regenerates static SEO pages under `products/` and
`brands/`, injects no-JS fallback tables into category pages, and writes the
data-backed pages under `guides/`, the `sitemap.xml` index, and separate core,
brand, and product sitemaps. Guide topics discovered by
`discover_guide_candidates.py` are review-only; only editorial records marked
`approved` in `data/guide-approvals.json` are published.

## SEO & indexing

- Sitemap: https://www.campgearcompare.com/sitemap.xml
- RSS: https://www.campgearcompare.com/feed.xml
- Google Search Console setup: [docs/gsc-setup-campgearcompare.md](docs/gsc-setup-campgearcompare.md)
- Search submission policy and IndexNow: [docs/gsc-indexing-api-setup.md](docs/gsc-indexing-api-setup.md)
- Six-month operating cadence: [docs/growth-operations.md](docs/growth-operations.md)
- Baidu setup: [docs/baidu-setup-campgearcompare.md](docs/baidu-setup-campgearcompare.md)
- Brand search monitoring: [docs/brand-search-monitoring.md](docs/brand-search-monitoring.md)

## Data

Product data lives in `data/official/{brandId}/products.json`. See [data/README.md](data/README.md).

## License

ISC
