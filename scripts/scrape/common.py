"""Shared utilities for official brand catalog scraping."""

from __future__ import annotations

import html
import json
import re
import ssl
import time
import http.client
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None

ROOT = Path(__file__).resolve().parent.parent.parent
OFFICIAL_DIR = ROOT / "data" / "official"
CONFIG_YAML = Path(__file__).resolve().parent / "config.yaml"

EDITORIAL_KEYS = (
    "status",
    "published",
    "imageLocal",
    "imageAlt",
    "inSummaryTable",
    "inDetailCards",
    "pros",
    "cons",
    "scenarios",
)
VERIFIED_OVERRIDE_KEYS = (
    "model",
    "modelEn",
    "description",
    "specs",
    "highlights",
    "structure",
    "detailStructure",
    "weightKg",
    "weightDisplay",
    "weightRange",
    "capacity",
    "fabric",
    "tarpType",
    "size",
    "bagType",
    "fillType",
    "comfortTemp",
    "seatHeight",
    "foldedSize",
    "subcategory",
)

USER_AGENT = "CampGearCompareScraper/1.0 (+personal compare project; respectful rate limit)"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def ssl_context() -> ssl.SSLContext:
    """macOS/Homebrew Python often lacks default CA bundle; prefer certifi when installed."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class RateLimiter:
    def __init__(self, interval: float) -> None:
        self.interval = max(0.0, interval)
        self._last = 0.0

    def wait(self) -> None:
        if self.interval <= 0:
            return
        now = time.monotonic()
        elapsed = now - self._last
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self._last = time.monotonic()


def load_config() -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML required — pip install PyYAML")
    if not CONFIG_YAML.exists():
        raise RuntimeError(f"Missing {CONFIG_YAML}")
    with CONFIG_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["brands"]


def collection_categories(collection: dict[str, Any]) -> set[str]:
    if collection.get("classifyFurniture"):
        return {"table", "chair"}
    category = collection.get("category")
    return {category} if category else set()


def merge_scraped_product(existing: dict[str, Any] | None, fresh: dict[str, Any]) -> dict[str, Any]:
    """Merge a fresh scrape into an existing record, preserving editorial fields."""
    if not existing:
        return fresh
    merged = dict(fresh)
    for key in EDITORIAL_KEYS:
        if key in existing:
            merged[key] = existing[key]
    if "published" not in existing:
        merged.pop("published", None)
    if existing.get("status") in ("verified", "merged"):
        for key in VERIFIED_OVERRIDE_KEYS:
            val = existing.get(key)
            if val not in (None, "", {}, []):
                merged[key] = val
    return merged


def is_visible_on_site(product: dict[str, Any]) -> bool:
    status = product.get("status")
    if status in ("verified", "merged"):
        return True
    if product.get("published") is True:
        return True
    if status == "draft" and "published" not in product:
        return True
    return False


def fetch_text(
    url: str,
    limiter: RateLimiter | None = None,
    *,
    user_agent: str | None = None,
    timeout: float = 45,
    retries: int = 3,
) -> str:
    last_exc: Exception | None = None
    for attempt in range(max(1, retries)):
        if limiter:
            limiter.wait()
        req = urllib.request.Request(
            url,
            headers={"User-Agent": user_agent or USER_AGENT, "Accept": "*/*"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, http.client.IncompleteRead, TimeoutError, ConnectionResetError) as exc:
            last_exc = exc
            if attempt + 1 < retries:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError("fetch_text failed without exception")


def fetch_json(
    url: str,
    limiter: RateLimiter | None = None,
    *,
    user_agent: str | None = None,
    timeout: float = 45,
    retries: int = 3,
) -> Any:
    return json.loads(
        fetch_text(url, limiter, user_agent=user_agent, timeout=timeout, retries=retries)
    )


def html_to_text(raw_html: str, max_len: int = 1200) -> str:
    if not raw_html:
        return ""
    if BeautifulSoup is not None:
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text("\n", strip=True)
    else:
        text = re.sub(r"<[^>]+>", " ", raw_html)
        text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "item"


def parse_variant_prices(variants: list[dict[str, Any]]) -> tuple[float | None, float | None, float | None, str | None]:
    prices: list[float] = []
    for variant in variants:
        raw = variant.get("price")
        if raw is None:
            continue
        try:
            prices.append(float(raw))
        except (TypeError, ValueError):
            continue
    if not prices:
        return None, None, None, None
    low = min(prices)
    high = max(prices)
    mid = prices[0]
    currency = None
    return mid, low, high, currency


def pick_image(product: dict[str, Any]) -> tuple[str | None, str | None]:
    images = product.get("images") or []
    if images:
        src = images[0].get("src")
        alt = images[0].get("alt") or product.get("title")
        return src, alt
    for variant in product.get("variants") or []:
        featured = variant.get("featured_image")
        if featured and featured.get("src"):
            return featured["src"], featured.get("alt") or product.get("title")
    return None, product.get("title")


def extract_highlights(body_html: str, limit: int = 4) -> list[str]:
    if not body_html or BeautifulSoup is None:
        text = html_to_text(body_html, max_len=600)
        return [text] if text else []
    soup = BeautifulSoup(body_html, "html.parser")
    items: list[str] = []
    for li in soup.find_all("li"):
        line = li.get_text(" ", strip=True)
        if line and len(line) > 8:
            items.append(line[:240])
        if len(items) >= limit:
            break
    if items:
        return items
    text = html_to_text(body_html, max_len=400)
    return [text] if text else []


def infer_specs(product: dict[str, Any]) -> dict[str, Any]:
    specs: dict[str, Any] = {}
    variants = product.get("variants") or []
    grams = [v.get("grams") for v in variants if isinstance(v.get("grams"), (int, float)) and v["grams"] > 0]
    if grams:
        kg = min(grams) / 1000.0
        specs["weightKg"] = round(kg, 2)
        specs["weightDisplay"] = f"约 {specs['weightKg']} kg"

    tags = [t.lower() for t in product.get("tags") or []]
    title = (product.get("title") or "").lower()
    for tag in product.get("tags") or []:
        if "person" in tag.lower():
            specs["capacity"] = tag.replace(" Person", "人").replace("-person", "人")
            break
    if "capacity" not in specs:
        m = re.search(r"(\d+)\s*[-–]?\s*person", title)
        if m:
            specs["capacity"] = m.group(1) + " 人"

    product_type = product.get("product_type") or ""
    if product_type:
        specs["structure"] = product_type

    return specs


def infer_sleeping_bag_specs(product: dict[str, Any]) -> dict[str, Any]:
    """Extract sleeping-bag fields from Shopify title, tags, and body."""
    specs: dict[str, Any] = {}
    title = product.get("title") or ""
    title_lower = title.lower()
    blob = title_lower + " " + html_to_text(product.get("body_html") or "", max_len=400).lower()

    temp_match = re.search(
        r"(\d+)\s*°?\s*f\s*/\s*(-?\d+(?:\.\d+)?)\s*°?\s*c",
        title_lower,
        re.IGNORECASE,
    )
    if temp_match:
        specs["comfortTemp"] = f"{temp_match.group(1)}°F / {temp_match.group(2)}°C"
    else:
        single = re.search(r"(\d+)\s*°?\s*f", title_lower)
        if single:
            specs["comfortTemp"] = f"{single.group(1)}°F"

    if "comfortTemp" not in specs:
        jp_temp = re.search(r"快適使用温度\s*(-?\d+)\s*℃", blob)
        if jp_temp:
            specs["comfortTemp"] = f"{jp_temp.group(1)}°C"
        else:
            zzz_temp = re.search(r"zzz\s*bag\s*(-?\d+)", title_lower)
            if zzz_temp:
                specs["comfortTemp"] = f"{zzz_temp.group(1)}°C"
            else:
                level_temp = re.search(r"レベル8\s*(-?\d+)", title)
                if level_temp:
                    specs["comfortTemp"] = f"{level_temp.group(1)}°C"

    if "down" in blob or "ダウン" in blob:
        if "synthetic" not in title_lower[:40] and "化繊" not in blob[:80]:
            specs["fillType"] = "羽绒"
    elif "synthetic" in blob or "cotton" in blob or "fibre" in blob or "fiber" in blob or "化繊" in blob:
        if "cotton" in blob:
            specs["fillType"] = "棉 / 化纤"
        else:
            specs["fillType"] = "化纤棉"

    if "mummy" in blob or "マミー" in blob:
        specs["bagType"] = "木乃伊"
    elif "envelope" in blob or "rectangular" in blob or "スクエアフット" in blob or "レクタンギュラー" in blob:
        specs["bagType"] = "信封式"
    elif "ofuton" in blob or "system" in blob and "mat" in blob:
        specs["bagType"] = "睡袋系统"
    elif "liner" in blob or "インナー" in blob:
        specs["bagType"] = "内胆"
    elif product.get("product_type") and product["product_type"] not in ("SleepingBag", "Accessory"):
        specs["bagType"] = product["product_type"]

    return specs


def infer_sleeping_pad_specs(product: dict[str, Any]) -> dict[str, Any]:
    """Extract sleeping-pad fields from Shopify title, tags, and body."""
    specs: dict[str, Any] = {}
    title = product.get("title") or ""
    title_lower = title.lower()
    blob = title_lower + " " + html_to_text(product.get("body_html") or "", max_len=600).lower()

    r_match = re.search(r"r[\s\-]?value?\s*[:=]?\s*(\d+(?:\.\d+)?)", blob, re.IGNORECASE)
    if not r_match:
        r_match = re.search(r"\br(\d+(?:\.\d+)?)\b", title_lower)
    if r_match:
        specs["rValue"] = f"R{r_match.group(1)}"

    if "self-inflat" in blob or "self inflat" in blob:
        specs["padType"] = "Self-inflating"
    elif any(k in blob for k in ("closed cell", "foam pad", "foam mat", "z-lite", "ridgerest")):
        specs["padType"] = "Foam pad"
    elif "down mat" in blob or "down pad" in blob:
        specs["padType"] = "Down pad"
    elif "air" in blob or "inflat" in blob:
        specs["padType"] = "Air pad"
    elif product.get("product_type"):
        ptype = product["product_type"].lower()
        if "foam" in ptype:
            specs["padType"] = "Foam pad"
        elif "air" in ptype or "inflat" in ptype:
            specs["padType"] = "Air pad"

    if "double wide" in blob or "double-wide" in blob:
        specs["size"] = "Double wide"
    elif re.search(r"\bwide\b", title_lower) and "double" not in title_lower:
        specs["size"] = "Wide"
    elif re.search(r"\blong\b", title_lower):
        specs["size"] = "Long"
    elif re.search(r"\bshort\b", title_lower):
        specs["size"] = "Short"
    elif "regular" in blob:
        specs["size"] = "Regular"

    dim = re.search(r"(\d{2,3})\s*[×x]\s*(\d{2,3})\s*(?:cm)?", title)
    if dim:
        specs["size"] = f"{dim.group(1)}×{dim.group(2)} cm"

    thick = re.search(r"(\d+(?:\.\d+)?)\s*(?:cm|in(?:ch)?)\s*thick", blob)
    if thick:
        specs["thickness"] = thick.group(0)

    return specs


FURNITURE_EXCLUDE_KEYWORDS = (
    "cot",
    "shelf",
    "shelves",
    "wagon",
    "hook",
    "peg",
    "storage",
    "container",
    "stacking shelf",
    "liner",
    "cushion only",
    "cover only",
    "mat only",
    "insert only",
    "bracket",
    "connector",
    "leg only",
    "frame only",
    "tent pole",
)

TABLE_KEYWORDS = (
    "table",
    "desk",
    "igt",
    "flat top",
    "flattop",
    "my table",
    "folding table",
    "camp table",
    "camping table",
)

CHAIR_KEYWORDS = (
    "chair",
    "stool",
    "sofa",
    "bench",
    "director",
    "recliner",
    "moon chair",
    "beach chair",
    "lounge chair",
    "folding chair",
    "camp chair",
    "camping chair",
    "take!",
    "take chair",
)


def classify_furniture(product: dict[str, Any]) -> str | None:
    """Classify a furniture-collection product as table or chair; None to skip."""
    title = (product.get("title") or "").lower()
    product_type = (product.get("product_type") or "").lower()
    tags = " ".join(product.get("tags") or []).lower()
    blob = f"{title} {product_type} {tags}"

    for bad in FURNITURE_EXCLUDE_KEYWORDS:
        if bad in blob:
            return None

    is_table = any(k in blob for k in TABLE_KEYWORDS)
    is_chair = any(k in blob for k in CHAIR_KEYWORDS)

    if is_table and not is_chair:
        return "table"
    if is_chair and not is_table:
        return "chair"
    if is_table and is_chair:
        if "chair" in title and "table" not in title:
            return "chair"
        if "table" in title and "chair" not in title:
            return "table"
        return None
    return None


def infer_furniture_specs(product: dict[str, Any]) -> dict[str, Any]:
    specs: dict[str, Any] = {}
    title = product.get("title") or ""
    blob = title + " " + html_to_text(product.get("body_html") or "", max_len=800)

    seat = re.search(
        r"seat\s*height[:\s]*(?:about\s*)?(\d+(?:\.\d+)?)\s*(?:in|inch|cm|″)",
        blob,
        re.IGNORECASE,
    )
    if seat:
        specs["seatHeight"] = seat.group(1) + (" cm" if "cm" in seat.group(0).lower() else " in")

    folded = re.search(
        r"fold(?:ed|ing)?\s*size[:\s]*([^\n.;]{8,60})",
        blob,
        re.IGNORECASE,
    )
    if folded:
        specs["foldedSize"] = folded.group(1).strip()

    return specs


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def update_manifest(brand_id: str, count: int, errors: list[str]) -> None:
    manifest_path = OFFICIAL_DIR / "_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else {"version": 1, "batches": []}
    manifest.setdefault("batches", []).append(
        {
            "brandId": brand_id,
            "scrapedAt": now_iso(),
            "productCount": count,
            "errors": errors,
        }
    )
    write_json(manifest_path, manifest)


def matches_filter(product: dict[str, Any], flt: dict[str, Any]) -> bool:
    title = (product.get("title") or "").lower()
    product_type = (product.get("product_type") or "").lower()
    tags = " ".join(product.get("tags") or []).lower()
    blob = f"{title} {product_type} {tags}"

    for bad in flt.get("excludeTitleKeywords") or []:
        if bad.lower() in title:
            return False

    type_ok = any(t.lower() == product_type for t in (flt.get("includeProductTypes") or []))
    keyword_ok = any(k.lower() in blob for k in (flt.get("includeKeywords") or []))
    return type_ok or keyword_ok


def normalize_shopify_product(
    product: dict[str, Any],
    *,
    brand_id: str,
    source_site: str,
    base_url: str,
    category: str,
    subcategory: str | None,
    currency: str,
) -> dict[str, Any]:
    handle = slugify(product.get("handle") or product.get("title") or "product")
    pid = f"{brand_id}-{handle}"
    price, price_min, price_max, _ = parse_variant_prices(product.get("variants") or [])
    image_url, image_alt = pick_image(product)
    description = html_to_text(product.get("body_html") or "", max_len=1500)
    highlights = extract_highlights(product.get("body_html") or "")
    specs = infer_specs(product)
    if category == "sleeping-bag":
        specs.update(infer_sleeping_bag_specs(product))
    if category == "sleeping-pad":
        specs.update(infer_sleeping_pad_specs(product))
    if category in ("table", "chair"):
        specs.update(infer_furniture_specs(product))

    item: dict[str, Any] = {
        "id": pid,
        "brandId": brand_id,
        "category": category,
        "subcategory": subcategory or product.get("product_type") or category,
        "model": product.get("title") or handle,
        "modelEn": product.get("title"),
        "description": description,
        "currency": currency,
        "specs": specs,
        "highlights": highlights,
        "imageUrl": image_url,
        "imageAlt": image_alt,
        "sourceUrl": urllib.parse.urljoin(base_url + "/", f"products/{handle}"),
        "sourceSite": source_site,
        "scrapedAt": now_iso(),
        "status": "draft",
        "published": False,
    }
    if price is not None:
        item["price"] = price
    if price_min is not None:
        item["priceMin"] = price_min
    if price_max is not None:
        item["priceMax"] = price_max
    if category in ("table", "chair"):
        item["inSummaryTable"] = False
    return item


def fetch_shopify_collection_products(
    base_url: str,
    handle: str,
    limiter: RateLimiter,
    limit: int = 250,
    *,
    user_agent: str | None = None,
    warnings: list[str] | None = None,
) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    page = 1
    not_found = False
    while True:
        url = f"{base_url.rstrip('/')}/collections/{handle}/products.json?limit={limit}&page={page}"
        try:
            payload = fetch_json(url, limiter, user_agent=user_agent)
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and page == 1:
                not_found = True
                if warnings is not None:
                    warnings.append(f"collection {handle}: not found (404)")
                break
            raise
        batch = payload.get("products") or []
        if not batch:
            break
        products.extend(batch)
        if len(batch) < limit:
            break
        page += 1
    if not products and not not_found and warnings is not None:
        warnings.append(f"collection {handle}: 0 products returned")
    return products


def fetch_shopify_all_products(
    base_url: str,
    limiter: RateLimiter,
    limit: int = 250,
    *,
    user_agent: str | None = None,
) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"{base_url.rstrip('/')}/products.json?limit={limit}&page={page}"
        payload = fetch_json(url, limiter, user_agent=user_agent, timeout=90, retries=4)
        batch = payload.get("products") or []
        if not batch:
            break
        products.extend(batch)
        if len(batch) < limit:
            break
        page += 1
    return products
