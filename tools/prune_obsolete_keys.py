#!/usr/bin/env python3
"""Remove obsolete keys from zh-CN that no longer exist in en-US."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources"

EN_CANDIDATES = [
    Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "ion-dist" / "i18n" / "en-US.json",
]

ZH_PATH = RESOURCES / "frontend-zh-CN.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_en_source() -> Path | None:
    for p in EN_CANDIDATES:
        if p.exists():
            return p
    return None


def main() -> int:
    en_path = find_en_source()
    if not en_path:
        print("en-US source not found; skipping prune.")
        return 0

    en_data = load_json(en_path)
    zh_data = load_json(ZH_PATH)

    obsolete = sorted(set(zh_data) - set(en_data))
    if not obsolete:
        print("No obsolete keys found.")
        return 0

    print(f"Found {len(obsolete)} obsolete keys. Pruning...")
    for key in obsolete:
        del zh_data[key]

    ZH_PATH.write_text(
        json.dumps(zh_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Removed {len(obsolete)} obsolete keys. Remaining: {len(zh_data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
