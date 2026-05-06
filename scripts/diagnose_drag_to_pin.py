#!/usr/bin/env python3
"""Diagnose why 'Drag to pin' is not being translated."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def find_claude_package() -> Path | None:
    base = Path(r"C:\Program Files\WindowsApps")
    if not base.exists():
        return None
    candidates = sorted(base.glob("Claude_*_x64__*/app/resources/en-US.json"), reverse=True)
    if candidates:
        return candidates[0].parent.parent
    return None


def safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("gbk", errors="replace").decode("gbk"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose 'Drag to pin' translation issue")
    parser.add_argument("--app-dir", type=str, default=None)
    args = parser.parse_args()

    if args.app_dir:
        app_dir = Path(args.app_dir)
    else:
        app_dir = find_claude_package()

    if not app_dir or not app_dir.exists():
        safe_print("Claude app directory not found. Use --app-dir to specify.")
        return 1

    assets_dir = app_dir / "resources" / "ion-dist" / "assets" / "v1"
    if not assets_dir.exists():
        safe_print(f"Assets dir not found: {assets_dir}")
        return 1

    safe_print("=" * 60)
    safe_print("DIAGNOSIS: Why is 'Drag to pin' still in English?")
    safe_print("=" * 60)
    safe_print(f"\nClaude version: {app_dir.name}")
    safe_print(f"Assets dir: {assets_dir}")

    all_js = sorted(assets_dir.glob("*.js"))
    safe_print(f"Total JS files: {len(all_js)}")

    # Test 1: Exact match for current rule
    safe_print("\n" + "-" * 60)
    safe_print("TEST 1: Check if current patch rule matches")
    safe_print("  Rule: children:\"Drag to pin\"")
    safe_print("-" * 60)

    rule = 'children:"Drag to pin"'
    matched = []
    for fpath in all_js:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        if rule in content:
            matched.append(fpath.name)

    if matched:
        safe_print(f"  RESULT: FOUND in {len(matched)} file(s)")
        for name in matched[:5]:
            safe_print(f"    - {name}")
        if len(matched) > 5:
            safe_print(f"    ... and {len(matched) - 5} more")
        safe_print("\n  => Patch rule EXISTS and should work.")
        safe_print("  => If UI still shows English, you need to RE-INSTALL the patch.")
    else:
        safe_print("  RESULT: NOT FOUND")
        safe_print("  => The string may have changed in this Claude version.")

    # Test 2: Search for nearby variants
    safe_print("\n" + "-" * 60)
    safe_print("TEST 2: Search for 'Drag to pin' variants")
    safe_print("-" * 60)

    variants = [
        'Drag to pin',
        'drag to pin',
        'Drag',
    ]

    for variant in variants:
        found_files = []
        for fpath in all_js:
            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            if variant in content:
                found_files.append(fpath.name)

        safe_print(f"  '{variant}' found in {len(found_files)} file(s)")
        if found_files and variant == 'Drag to pin':
            for name in found_files[:3]:
                safe_print(f"    - {name}")

    # Test 3: Look for context around "pin" in sidebar-related files
    safe_print("\n" + "-" * 60)
    safe_print("TEST 3: Check if patch was actually applied")
    safe_print("-" * 60)

    translated = 'children:"拖拽固定"'
    translated_found = 0
    for fpath in all_js:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        if translated in content:
            translated_found += 1

    if translated_found > 0:
        safe_print(f"  Translated string found in {translated_found} file(s)")
        safe_print("  => Patch WAS applied successfully.")
        safe_print("  => Try clearing Claude cache or restart computer.")
    else:
        safe_print("  Translated string NOT found")
        safe_print("  => Patch has NOT been applied to this Claude version.")
        safe_print("  => Close Claude and run claude-zh-cn.bat -> [1] Install")

    safe_print("\n" + "=" * 60)
    safe_print("SUMMARY")
    safe_print("=" * 60)

    if matched and translated_found > 0:
        safe_print("Both English and Chinese strings exist in JS files.")
        safe_print("This is normal - multiple chunks may contain the label.")
        safe_print("If UI still shows English, try:")
        safe_print("  1. Full exit Claude (tray icon too)")
        safe_print("  2. Delete %LOCALAPPDATA%/Claude-zh-CN-official-backup")
        safe_print("  3. Re-run claude-zh-cn.bat -> [1] Install")
        safe_print("  4. Restart Windows (sometimes JS is cached in memory)")
    elif matched and translated_found == 0:
        safe_print("English string found but NO translated string.")
        safe_print("-> Patch needs to be installed. Run claude-zh-cn.bat -> [1]")
    else:
        safe_print("English string NOT found in current Claude version.")
        safe_print("-> This label may have been removed/renamed by Claude update.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
