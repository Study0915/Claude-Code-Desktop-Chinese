#!/usr/bin/env python3
"""Validate zh-CN resource files for JSON validity, completeness, and consistency.

Checks:
  - JSON syntax validity
  - No empty values
  - Placeholder consistency between en-US and zh-CN ({name}, {count}, etc.)
  - Common issues: curly quotes used as JSON delimiters
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources"

TARGETS = [
    {
        "name": "desktop",
        "zh": RESOURCES / "desktop-zh-CN.json",
        "en_candidates": [
            Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "en-US.json",
        ],
    },
    {
        "name": "frontend",
        "zh": RESOURCES / "frontend-zh-CN.json",
        "en_candidates": [
            Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "ion-dist" / "i18n" / "en-US.json",
        ],
    },
    {
        "name": "statsig",
        "zh": RESOURCES / "statsig-zh-CN.json",
        "en_candidates": [
            Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "ion-dist" / "i18n" / "statsig" / "en-US.json",
        ],
    },
]

# Match top-level placeholders only (not nested ones inside plural/select forms)
# This extracts variable names like {name}, {count}, {date} but not inner content
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
# Match ICU plural/select patterns to verify structural consistency
ICU_PATTERN_RE = re.compile(r"\{(\w+),\s*(plural|select)\b")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_en_source(candidates: list[Path]) -> Path | None:
    for p in candidates:
        if p.exists():
            return p
    return None


def check_empty_values(data: dict, name: str) -> list[str]:
    issues = []
    for key, value in data.items():
        if isinstance(value, str) and value.strip() == "":
            issues.append(f"  [{name}] Empty value: {key}")
    return issues


def check_placeholders(zh_data: dict, en_data: dict, name: str) -> list[str]:
    issues = []
    for key in zh_data:
        if key not in en_data:
            continue
        zh_val = zh_data[key]
        en_val = en_data[key]
        if not isinstance(zh_val, str) or not isinstance(en_val, str):
            continue
        # Compare top-level placeholder variable names only
        zh_ph = sorted(PLACEHOLDER_RE.findall(zh_val))
        en_ph = sorted(PLACEHOLDER_RE.findall(en_val))
        if zh_ph != en_ph:
            issues.append(f"  [{name}] Placeholder mismatch: {key}")
            issues.append(f"    en: {en_ph}")
            issues.append(f"    zh: {zh_ph}")
        # Check ICU plural/select structural consistency
        zh_icu = sorted(ICU_PATTERN_RE.findall(zh_val))
        en_icu = sorted(ICU_PATTERN_RE.findall(en_val))
        if zh_icu != en_icu:
            issues.append(f"  [{name}] ICU pattern mismatch: {key}")
            issues.append(f"    en: {en_icu}")
            issues.append(f"    zh: {zh_icu}")
    return issues


def check_curly_quotes(path: Path) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        if "“" in line or "”" in line:
            if len(stripped) > 2 and stripped[1] == "“":
                issues.append(f"  [{path.name}] Curly quote as JSON delimiter at line {i}")
            elif "”:" in stripped:
                issues.append(f"  [{path.name}] Curly quote as JSON delimiter at line {i}")
    return issues


def main() -> int:
    all_issues: list[str] = []

    for target in TARGETS:
        name = target["name"]
        zh_path = target["zh"]

        if not zh_path.exists():
            all_issues.append(f"[{name}] MISSING: {zh_path}")
            continue

        try:
            zh_data = load_json(zh_path)
        except json.JSONDecodeError as e:
            all_issues.append(f"[{name}] JSON parse error: {e}")
            continue

        if not isinstance(zh_data, dict):
            all_issues.append(f"[{name}] Expected JSON object, got {type(zh_data).__name__}")
            continue

        print(f"OK {zh_path.name}: {len(zh_data)} keys")

        all_issues.extend(check_empty_values(zh_data, name))
        all_issues.extend(check_curly_quotes(zh_path))

        en_path = find_en_source(target["en_candidates"])
        if en_path:
            try:
                en_data = load_json(en_path)
                ph_issues = check_placeholders(zh_data, en_data, name)
                all_issues.extend(ph_issues)
                if not ph_issues:
                    print(f"  Placeholders: OK (checked against en-US)")
                else:
                    print(f"  Placeholders: {len(ph_issues) // 3} mismatches")
            except Exception as e:
                print(f"  Placeholders: skipped (could not load en-US: {e})")
        else:
            print(f"  Placeholders: skipped (en-US source not found)")

    if all_issues:
        print(f"\n--- Issues ({len(all_issues)} lines) ---")
        for line in all_issues:
            print(line)
        return 1
    else:
        print("\nAll resource files validated. No issues found.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
