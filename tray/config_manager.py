"""Configuration manager for Claude zh-CN tray monitor.

Stores patch state (installed version, Claude version, timestamps)
in %APPDATA%\\Claude-3p\\zh-cn-patch.json.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / "AppData" / "Roaming" / "Claude-3p"
PATCH_CONFIG_PATH = CONFIG_DIR / "zh-cn-patch.json"


def _default_config() -> dict[str, Any]:
    return {
        "installed": False,
        "claude_version": None,
        "patch_version": None,
        "installed_at": None,
        "last_check": None,
        "language": "zh-CN",
        "auto_start": False,
        "check_interval_minutes": 60,
    }


def load_config() -> dict[str, Any]:
    """Load patch config, returning defaults if file is missing."""
    if not PATCH_CONFIG_PATH.exists():
        return _default_config()
    try:
        data = json.loads(PATCH_CONFIG_PATH.read_text(encoding="utf-8"))
        merged = _default_config()
        merged.update(data)
        return merged
    except (json.JSONDecodeError, OSError):
        return _default_config()


def save_config(config: dict[str, Any]) -> bool:
    """Save patch config to disk."""
    try:
        PATCH_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        PATCH_CONFIG_PATH.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return True
    except OSError as e:
        print(f"Warning: cannot save config: {e}")
        return False


def update_install_state(claude_version: str, patch_version: str) -> None:
    """Record a successful installation."""
    config = load_config()
    config["installed"] = True
    config["claude_version"] = claude_version
    config["patch_version"] = patch_version
    config["installed_at"] = time.time()
    save_config(config)


def update_check_time() -> None:
    """Record that a version check was performed."""
    config = load_config()
    config["last_check"] = time.time()
    save_config(config)