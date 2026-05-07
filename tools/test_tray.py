#!/usr/bin/env python3
"""Unit tests for tray monitor modules (non-GUI parts)."""
from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import mock

# Add project root to path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_config_manager_load_save() -> None:
    from tray.config_manager import load_config, save_config
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            # Load should return defaults when file doesn't exist
            config = load_config()
            assert config["installed"] is False
            assert config["claude_version"] is None
            # Save and reload
            config["installed"] = True
            config["claude_version"] = "1.5354.0.0"
            assert save_config(config) is True
            reloaded = load_config()
            assert reloaded["installed"] is True
            assert reloaded["claude_version"] == "1.5354.0.0"


def test_config_manager_corrupt_file() -> None:
    from tray.config_manager import load_config
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        fake_config.write_text("not json!", encoding="utf-8")
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            config = load_config()
            assert config["installed"] is False


def test_config_manager_update_install_state() -> None:
    from tray.config_manager import update_install_state, load_config
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            update_install_state("1.5354.0.0", "1.5354.0.1")
            config = load_config()
            assert config["installed"] is True
            assert config["claude_version"] == "1.5354.0.0"
            assert config["patch_version"] == "1.5354.0.1"
            assert config["installed_at"] is not None


def test_win_utils_get_claude_version() -> None:
    from tray.win_utils import get_claude_version
    # Mock a package directory
    with tempfile.TemporaryDirectory() as tmp:
        pkg_dir = Path(tmp) / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app"
        pkg_dir.mkdir(parents=True)
        version = get_claude_version(pkg_dir)
        assert version == "1.5354.0.0"


def test_win_utils_get_claude_version_none() -> None:
    from tray.win_utils import get_claude_version
    assert get_claude_version(None) is None


def test_determine_status_not_installed() -> None:
    from tray.config_manager import load_config
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            # Import and patch at module level
            import tray.app as app_module
            with mock.patch.object(app_module, "load_config", return_value={"installed": False}):
                status = app_module.determine_status()
                assert status == "not_installed"


def test_create_icon_colors() -> None:
    """Verify icon creation doesn't crash for all colors."""
    from tray.app import create_icon
    for color in ("green", "yellow", "red"):
        img = create_icon(color)
        assert img.size == (64, 64)


def main() -> int:
    tests = [
        test_config_manager_load_save,
        test_config_manager_corrupt_file,
        test_config_manager_update_install_state,
        test_win_utils_get_claude_version,
        test_win_utils_get_claude_version_none,
        test_determine_status_not_installed,
        test_create_icon_colors,
    ]
    for test in tests:
        try:
            test()
            print(f"OK {test.__name__}")
        except Exception as e:
            print(f"FAIL {test.__name__}: {e}")
            return 1
    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())