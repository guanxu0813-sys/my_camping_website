#!/usr/bin/env python3
"""Translate NANGA product intro fields (model, description, highlights) to English."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_PATH = ROOT / "data" / "official" / "nanga" / "products.json"

MODEL_REPLACEMENTS = (
    (r"（数量限定）", "(Limited) "),
    (r"【Re:ACT】", "[Re:ACT] "),
    (r"\(直営店限定\)", "(Direct Store Exclusive) "),
    (r"オーロラテックス\s*レクタンギュラー\s*ダウンバッグ", "Aurora Tex Rectangular Down Bag"),
    (r"オーロラテックス\s*スクエアフット", "Aurora Tex Square Foot"),
    (r"オーロラテックス\s*ライト", "Aurora Tex Light"),
    (r"UDD\s*バッグ", "UDD Bag"),
    (r"ソナエバッグ", "Sonae Bag"),
    (r"キッズ\s*スクエアフット", "Kids Square Foot"),
    (r"マット\s*コンパチブル\s*バッグ", "Mat Compatible Bag"),
    (r"ミニマリスム\s*5ビロー", "Minimarhythm 5 Below"),
    (r"ミニマリスム\s*ゼロ", "Minimarhythm Zero"),
    (r"ミニマリスム\s*ハーフ", "Minimarhythm Half"),
    (r"ラバイマ\s*バッグ\s*ダブル", "Rabaima Bag Double"),
    (r"レベル8\s*", "Level 8 "),
    (r"ライコット", "Raikot"),
)

FILL_TYPE_EN = {
    "羽绒": "Down",
    "化纤棉": "Synthetic",
    "棉 / 化纤": "Cotton / Synthetic",
}


def clear_proxies() -> None:
    for key in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "http_proxy",
        "https_proxy",
        "ALL_PROXY",
        "all_proxy",
    ):
        os.environ.pop(key, None)


def has_japanese(text: str) -> bool:
    return bool(re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text or ""))


def translate_model(name: str, translator: GoogleTranslator) -> str:
    text = name.strip()
    for pattern, repl in MODEL_REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    if has_japanese(text):
        text = translate_with_retry(text, translator)
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, size: int = 1200) -> list[str]:
    text = text.strip()
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            split_at = max(text.rfind("。", start, end), text.rfind(". ", start, end))
            if split_at > start:
                end = split_at + 1
        parts.append(text[start:end].strip())
        start = end
    return [p for p in parts if p]


def translate_with_retry(text: str, translator: GoogleTranslator, retries: int = 5) -> str:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            time.sleep(0.8 + attempt * 0.5)
            return translator.translate(text)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
    if last_exc:
        raise last_exc
    return text


def translate_text(text: str, translator: GoogleTranslator) -> str:
    if not text or not text.strip() or not has_japanese(text):
        return text
    chunks = chunk_text(text)
    translated = [translate_with_retry(chunk, translator) for chunk in chunks]
    return " ".join(translated).strip()


def translate_highlights(items: list[str], translator: GoogleTranslator) -> list[str]:
    return [translate_text(item, translator) for item in items if item]


def is_translated(product: dict) -> bool:
    return not has_japanese(product.get("description") or "")


def main() -> int:
    clear_proxies()
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    translator = GoogleTranslator(source="ja", target="en")

    for idx, product in enumerate(products, start=1):
        if is_translated(product):
            print(f"[{idx}/{len(products)}] skip {product['id']}")
            continue

        original_model = product.get("model") or ""
        if not product.get("modelEn") or product.get("modelEn") == original_model:
            product["modelEn"] = original_model
        product["model"] = translate_model(original_model, translator)
        product["description"] = translate_text(product.get("description") or "", translator)
        product["highlights"] = translate_highlights(product.get("highlights") or [], translator)
        if product.get("imageAlt"):
            product["imageAlt"] = product["model"]

        specs = product.get("specs") or {}
        if specs.get("fillType") in FILL_TYPE_EN:
            specs["fillType"] = FILL_TYPE_EN[specs["fillType"]]
        if specs.get("weightDisplay", "").startswith("约"):
            specs["weightDisplay"] = specs["weightDisplay"].replace("约", "approx.", 1)

        PRODUCTS_PATH.write_text(
            json.dumps(products, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[{idx}/{len(products)}] {original_model} -> {product['model']}")

    print(f"Updated {PRODUCTS_PATH} ({len(products)} products)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
