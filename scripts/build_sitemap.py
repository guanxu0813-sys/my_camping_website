#!/usr/bin/env python3
"""Generate robots.txt, sitemap.xml, and inject SEO meta / JSON-LD into HTML."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEO_PATH = DATA / "seo.json"
SEO_HEAD_START = "<!-- @seo-head -->"
SEO_HEAD_END = "<!-- @seo-head:end -->"
SEO_CRAWL_START = "<!-- @seo-crawl -->"
SEO_CRAWL_END = "<!-- @seo-crawl:end -->"
ITEM_LIST_LIMIT = 30


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def load_official_products() -> list[dict]:
    sys.path.insert(0, str(ROOT / "scripts" / "scrape"))
    from common import is_visible_on_site  # noqa: E402

    products: list[dict] = []
    official = DATA / "official"
    index_path = official / "index.json"
    if index_path.exists():
        brand_ids = load_json(index_path).get("brandIds", [])
    else:
        brand_ids = [
            p.name
            for p in official.iterdir()
            if p.is_dir() and (p / "products.json").exists()
        ]

    for brand_id in brand_ids:
        path = official / brand_id / "products.json"
        if not path.exists():
            continue
        batch = load_json(path)
        if isinstance(batch, list):
            products.extend(
                p for p in batch if isinstance(p, dict) and is_visible_on_site(p)
            )
    return products


def brand_map(brands: list[dict]) -> dict[str, dict]:
    return {b["id"]: b for b in brands if b.get("id")}


def brand_display_name(brand: dict | None, brand_id: str) -> str:
    if not brand:
        return brand_id
    return brand.get("nameEn") or brand.get("name") or brand_id


def brand_rank(brand: dict | None) -> int:
    if not brand:
        return 9999
    rank = brand.get("rank")
    return int(rank) if isinstance(rank, (int, float)) else 9999


def page_products(page: dict, products: list[dict]) -> list[dict]:
    categories = page.get("categories") or []
    if not categories:
        return []
    return [p for p in products if p.get("category") in categories]


def sorted_products_for_page(page: dict, products: list[dict], brands: dict[str, dict]) -> list[dict]:
    rows = page_products(page, products)

    def sort_key(product: dict) -> tuple:
        brand = brands.get(product.get("brandId", ""))
        return (brand_rank(brand), (product.get("model") or "").lower())

    return sorted(rows, key=sort_key)


def page_lastmod(page: dict, products: list[dict]) -> str:
    html_path = ROOT / page["file"]
    stamps = [html_path.stat().st_mtime] if html_path.exists() else []
    for product in page_products(page, products):
        brand_id = product.get("brandId")
        if not brand_id:
            continue
        catalog_path = DATA / "official" / brand_id / "products.json"
        if catalog_path.exists():
            stamps.append(catalog_path.stat().st_mtime)
    if not stamps:
        return date.today().isoformat()
    return date.fromtimestamp(max(stamps)).isoformat()


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_og_and_twitter(page: dict, site_url: str, seo: dict) -> str:
    title = page["title"]
    description = page["description"]
    url = f"{site_url}{page['path']}"
    image = page.get("ogImage") or seo.get("defaultOgImage") or f"{site_url}/assets/hero-home.jpg"
    lines = [
        f'<meta property="og:type" content="website" />',
        f'<meta property="og:site_name" content="{escape_html(seo.get("siteName", "CampGear Compare"))}" />',
        f'<meta property="og:title" content="{escape_html(title)}" />',
        f'<meta property="og:description" content="{escape_html(description)}" />',
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:image" content="{image}" />',
        f'<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{escape_html(title)}" />',
        f'<meta name="twitter:description" content="{escape_html(description)}" />',
        f'<meta name="twitter:image" content="{image}" />',
    ]
    return "\n  ".join(lines)


def build_home_schema(site_url: str, seo: dict) -> dict:
    site_name = seo.get("siteName", "CampGear Compare")
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{site_url}/#organization",
                "name": site_name,
                "url": f"{site_url}/",
                "logo": f"{site_url}/favicon.svg",
            },
            {
                "@type": "WebSite",
                "@id": f"{site_url}/#website",
                "name": site_name,
                "url": f"{site_url}/",
                "publisher": {"@id": f"{site_url}/#organization"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": f"{site_url}/tent.html?q={{search_term_string}}",
                    },
                    "query-input": "required name=search_term_string",
                },
            },
        ],
    }


def build_category_schema(
    page: dict,
    site_url: str,
    seo: dict,
    products: list[dict],
    brands: dict[str, dict],
) -> dict:
    page_url = f"{site_url}{page['path']}"
    site_name = seo.get("siteName", "CampGear Compare")
    label = page.get("breadcrumb") or page["file"]
    rows = sorted_products_for_page(page, products, brands)
    brand_names: list[str] = []
    seen: set[str] = set()
    for product in rows:
        brand_id = product.get("brandId")
        if not brand_id or brand_id in seen:
            continue
        seen.add(brand_id)
        brand_names.append(brand_display_name(brands.get(brand_id), brand_id))

    item_elements = []
    for index, product in enumerate(rows[:ITEM_LIST_LIMIT], start=1):
        brand_id = product.get("brandId", "")
        name = f"{brand_display_name(brands.get(brand_id), brand_id)} {product.get('model', '')}".strip()
        item_elements.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "url": f"{page_url}#product-{product.get('id', '')}",
            }
        )

    graph: list[dict] = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": f"{site_url}/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": label,
                    "item": page_url,
                },
            ],
        },
        {
            "@type": "CollectionPage",
            "name": page["title"],
            "description": page["description"],
            "url": page_url,
            "isPartOf": {"@id": f"{site_url}/#website"},
            "about": {
                "@type": "Thing",
                "name": label,
                "description": (
                    f"{len(rows)} models compared across "
                    + ", ".join(brand_names[:12])
                    + (" and more" if len(brand_names) > 12 else "")
                ),
            },
        },
    ]
    if item_elements:
        graph.append(
            {
                "@type": "ItemList",
                "name": f"{label} compared on {site_name}",
                "numberOfItems": len(rows),
                "itemListElement": item_elements,
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def build_legal_schema(page: dict, site_url: str, seo: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{site_url}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": page.get("breadcrumb", "Legal"),
                        "item": f"{site_url}{page['path']}",
                    },
                ],
            },
            {
                "@type": "WebPage",
                "name": page["title"],
                "description": page["description"],
                "url": f"{site_url}{page['path']}",
                "isPartOf": {"@id": f"{site_url}/#website"},
            },
        ],
    }


def build_json_ld(
    page: dict,
    site_url: str,
    seo: dict,
    products: list[dict],
    brands: dict[str, dict],
) -> dict:
    schema = page.get("schema", "")
    if schema == "home":
        return build_home_schema(site_url, seo)
    if schema == "category":
        return build_category_schema(page, site_url, seo, products, brands)
    return build_legal_schema(page, site_url, seo)


def build_seo_head_block(
    page: dict,
    site_url: str,
    seo: dict,
    products: list[dict],
    brands: dict[str, dict],
) -> str:
    json_ld = build_json_ld(page, site_url, seo, products, brands)
    return (
        f"{SEO_HEAD_START}\n"
        f"  {build_og_and_twitter(page, site_url, seo)}\n"
        f'  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False, separators=(",", ":"))}</script>\n'
        f"  {SEO_HEAD_END}"
    )


def build_crawl_paragraph(
    page: dict,
    products: list[dict],
    brands: dict[str, dict],
) -> str:
    rows = sorted_products_for_page(page, products, brands)
    if not rows:
        return ""
    label = page.get("breadcrumb") or "Products"
    if label == "Furniture":
        label_plural = "tables and chairs"
    else:
        label_plural = label.lower()
    brand_names: list[str] = []
    seen: set[str] = set()
    for product in rows:
        brand_id = product.get("brandId")
        if not brand_id or brand_id in seen:
            continue
        seen.add(brand_id)
        brand_names.append(brand_display_name(brands.get(brand_id), brand_id))

    sample_models = []
    for product in rows[:8]:
        brand_id = product.get("brandId", "")
        sample_models.append(
            f"{brand_display_name(brands.get(brand_id), brand_id)} {product.get('model', '')}".strip()
        )

    brands_text = ", ".join(brand_names[:14])
    if len(brand_names) > 14:
        brands_text += ", and more"
    samples_text = "; ".join(sample_models)
    return (
        f"Compare {len(rows)} {label_plural} from {brands_text}. "
        f"Sortable specs include weight, capacity, materials, and reference price. "
        f"Featured models: {samples_text}."
    )


def build_crawl_block(
    page: dict,
    products: list[dict],
    brands: dict[str, dict],
) -> str:
    paragraph = build_crawl_paragraph(page, products, brands)
    if not paragraph:
        return ""
    return (
        f"{SEO_CRAWL_START}\n"
        f'  <p class="seo-crawl" id="seo-crawl">{escape_html(paragraph)}</p>\n'
        f"  {SEO_CRAWL_END}"
    )


def inject_html_seo(
    page: dict,
    site_url: str,
    seo: dict,
    products: list[dict],
    brands: dict[str, dict],
) -> bool:
    html_path = ROOT / page["file"]
    if not html_path.exists():
        return False

    text = html_path.read_text(encoding="utf-8")
    head_block = build_seo_head_block(page, site_url, seo, products, brands)
    head_pattern = re.compile(re.escape(SEO_HEAD_START) + r".*?" + re.escape(SEO_HEAD_END), re.DOTALL)
    if head_pattern.search(text):
        text = head_pattern.sub(head_block, text, count=1)
    else:
        text = re.sub(
            r'(<link rel="canonical" href="[^"]+" />\n)',
            r"\1  " + head_block + "\n",
            text,
            count=1,
        )

    if page.get("schema") == "category":
        crawl_block = build_crawl_block(page, products, brands)
        if crawl_block:
            crawl_pattern = re.compile(
                re.escape(SEO_CRAWL_START) + r".*?" + re.escape(SEO_CRAWL_END),
                re.DOTALL,
            )
            if crawl_pattern.search(text):
                text = crawl_pattern.sub(crawl_block, text, count=1)
            else:
                text = re.sub(
                    r'(class="page__lead page__lead--compact">[^<]+</p>\n)',
                    r"\1\n    " + crawl_block + "\n",
                    text,
                    count=1,
                )

    html_path.write_text(text, encoding="utf-8")
    return True


def write_sitemap(site_url: str, pages: list[dict], products: list[dict]) -> None:
    entries = []
    for page in pages:
        loc = f"{site_url}{page['path']}"
        lastmod = page_lastmod(page, products)
        entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{page['changefreq']}</changefreq>\n"
            f"    <priority>{page['priority']}</priority>\n"
            "  </url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def write_robots(site_url: str) -> None:
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /data/\n"
        "\n"
        f"Sitemap: {site_url}/sitemap.xml\n"
    )
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


def main() -> int:
    seo = load_json(SEO_PATH)
    site_url = seo["siteUrl"].rstrip("/")
    pages = seo.get("pages", [])
    brands_list = load_json(DATA / "brands.json")
    brands = brand_map(brands_list if isinstance(brands_list, list) else [])
    products = load_official_products()

    write_sitemap(site_url, pages, products)
    write_robots(site_url)

    updated = 0
    for page in pages:
        if inject_html_seo(page, site_url, seo, products, brands):
            updated += 1

    print(
        f"Wrote sitemap.xml and robots.txt for {site_url}; "
        f"injected SEO blocks into {updated} HTML file(s); "
        f"{len(products)} products indexed for structured data"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
