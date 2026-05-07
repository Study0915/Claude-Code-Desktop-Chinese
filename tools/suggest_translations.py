#!/usr/bin/env python3
"""Suggest translations for new en-US keys using the glossary.

Reads the glossary and en-US source, finds keys present in en-US but
missing from zh-CN, and generates a suggested translation file with
glossary terms pre-applied.

Usage:
  python tools/suggest_translations.py [--lang zh-CN]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources"
GLOSSARY_PATH = RESOURCES / "glossary.json"

EN_US_CANDIDATES = [
    Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "en-US.json",
    Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "ion-dist" / "i18n" / "en-US.json",
]

ZH_CN_PATHS = [
    RESOURCES / "desktop-zh-CN.json",
    RESOURCES / "frontend-zh-CN.json",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_en_source() -> Path | None:
    for p in EN_US_CANDIDATES:
        if p.exists():
            return p
    return None


def load_glossary() -> dict:
    if GLOSSARY_PATH.exists():
        return json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
    return {}


def apply_glossary(text: str, glossary: dict) -> str:
    """Apply glossary substitutions to an English string."""
    result = text
    for term, info in glossary.items():
        zh = info.get("zh", "")
        if not zh or zh == term:
            continue
        # Only substitute whole words
        pattern = r'\b' + re.escape(term) + r'\b'
        result = re.sub(pattern, zh, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest translations for new en-US keys")
    parser.add_argument("--lang", type=str, default="zh-CN",
                        help="Target language code (default: zh-CN)")
    args = parser.parse_args()

    en_path = find_en_source()
    if not en_path:
        print("en-US source not found. Please specify the correct path.")
        print(f"Expected one of: {EN_US_CANDIDATES}")
        return 1

    en_data = load_json(en_path)
    glossary = load_glossary()

    # Load all existing zh-CN keys
    zh_keys: set[str] = set()
    for zh_path in ZH_CN_PATHS:
        if zh_path.exists():
            zh_data = load_json(zh_path)
            zh_keys.update(zh_data.keys())

    # Find missing keys
    missing = sorted(set(en_data.keys()) - zh_keys)

    if not missing:
        print("No missing keys found. All en-US keys are present in zh-CN.")
        return 0

    print(f"Found {len(missing)} missing keys in {args.lang}.")
    print(f"Glossary has {len(glossary)} terms.\n")

    # Generate suggestions
    suggestions: dict = {}
    for key in missing:
        en_val = en_data[key]
        if isinstance(en_val, dict):
            # Plural form - skip for now
            suggestions[key] = {
                "en": en_val,
                "suggestion": "(plural form - manual translation needed)"
            }
            continue

        suggested = apply_glossary(en_val, glossary)
        auto_translated = suggested != en_val
        suggestions[key] = {
            "en": en_val,
            "suggestion": suggested,
            "auto_translated": auto_translated,
        }

    # Write suggestions file
    out_path = RESOURCES / "translation-suggestions.json"
    out_path.write_text(
        json.dumps(suggestions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    auto_count = sum(1 for v in suggestions.values() if v.get("auto_translated"))
    manual_count = len(suggestions) - auto_count

    print(f"Wrote suggestions to: {out_path}")
    print(f"  Auto-translated (glossary applied): {auto_count}")
    print(f"  Manual translation needed: {manual_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())