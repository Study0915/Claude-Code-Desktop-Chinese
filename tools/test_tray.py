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
            update_install_state("1.5354.0.0", "1.5354.0.1", "C:/Claude/app")
            config = load_config()
            assert config["installed"] is True
            assert config["app_dir"] == "C:/Claude/app"
            assert config["claude_version"] == "1.5354.0.0"
            assert config["patch_version"] == "1.5354.0.1"
            assert config["installed_at"] is not None
            assert config["last_error"] is None


def test_config_manager_update_last_error() -> None:
    from tray.config_manager import update_last_error, load_config
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            update_last_error("failed")
            assert load_config()["last_error"] == "failed"


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


def test_win_utils_is_patch_installed() -> None:
    from tray.win_utils import is_patch_installed
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = Path(tmp) / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app"
        res = app_dir / "resources"
        # Not installed: files missing
        assert is_patch_installed(app_dir) is False
        # Create zh-CN files
        (res / "zh-CN.json").parent.mkdir(parents=True)
        (res / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "zh-CN.json").write_text("{}", encoding="utf-8")
        assert is_patch_installed(app_dir) is False
        (res / "ion-dist" / "i18n" / "statsig").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json").write_text("{}", encoding="utf-8")
        assert is_patch_installed(app_dir) is True


def test_win_utils_get_patch_components() -> None:
    from tray.win_utils import get_patch_components
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = Path(tmp) / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app"
        res = app_dir / "resources"
        assets = res / "ion-dist" / "assets" / "v1"
        (res / "zh-CN.json").parent.mkdir(parents=True)
        (res / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n" / "zh-CN.json").parent.mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n" / "statsig").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json").write_text("{}", encoding="utf-8")
        assets.mkdir(parents=True)
        (assets / "index-test.js").write_text('const locales=["en-US","zh-CN"];', encoding="utf-8")
        components = get_patch_components(app_dir)
        assert components["app_found"] is True
        assert components["desktop_json"] is True
        assert components["frontend_json"] is True
        assert components["statsig_json"] is True
        assert components["whitelist"] is True


def test_determine_status_installed_from_files() -> None:
    """If config says not installed but zh-CN files exist, detect as installed."""
    import tray.app as app_module
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        app_dir = Path(tmp) / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app"
        res = app_dir / "resources"
        (res / "zh-CN.json").parent.mkdir(parents=True)
        (res / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n" / "statsig").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json").write_text("{}", encoding="utf-8")
        assets = res / "ion-dist" / "assets" / "v1"
        assets.mkdir(parents=True)
        (assets / "index-test.js").write_text('const locales=["en-US","zh-CN"];', encoding="utf-8")
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            with mock.patch.object(app_module, "find_claude_package", return_value=app_dir):
                status = app_module.determine_status()
                assert status == "installed"


def test_determine_status_uses_configured_app_dir() -> None:
    import tray.app as app_module
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = Path(tmp) / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app"
        res = app_dir / "resources"
        (res / "zh-CN.json").parent.mkdir(parents=True)
        (res / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n" / "statsig").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json").write_text("{}", encoding="utf-8")
        assets = res / "ion-dist" / "assets" / "v1"
        assets.mkdir(parents=True)
        (assets / "index-test.js").write_text('const locales=["en-US","zh-CN"];', encoding="utf-8")
        config = {
            "installed": True,
            "app_dir": str(app_dir),
            "claude_version": "1.5354.0.0",
        }
        with mock.patch.object(app_module, "load_config", return_value=config):
            with mock.patch.object(app_module, "find_claude_package", return_value=None):
                assert app_module.determine_status() == "installed"


def test_determine_status_partial_when_whitelist_missing() -> None:
    import tray.app as app_module
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        app_dir = Path(tmp) / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app"
        res = app_dir / "resources"
        (res / "zh-CN.json").parent.mkdir(parents=True)
        (res / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "zh-CN.json").write_text("{}", encoding="utf-8")
        (res / "ion-dist" / "i18n" / "statsig").mkdir(parents=True)
        (res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json").write_text("{}", encoding="utf-8")
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            with mock.patch.object(app_module, "find_claude_package", return_value=app_dir):
                assert app_module.determine_status() == "partial"


def test_determine_status_outdated() -> None:
    import tray.app as app_module
    with tempfile.TemporaryDirectory() as tmp:
        fake_config = Path(tmp) / "zh-cn-patch.json"
        fake_config.write_text(
            '{"installed": true, "claude_version": "1.5354.0.0"}',
            encoding="utf-8",
        )
        # Current Claude is 1.5355.0.0
        app_dir = Path(tmp) / "Claude_1.5355.0.0_x64__pzs8sxrjxfjjc" / "app"
        app_dir.mkdir(parents=True)
        with mock.patch("tray.config_manager.PATCH_CONFIG_PATH", fake_config):
            with mock.patch.object(app_module, "find_claude_package", return_value=app_dir):
                status = app_module.determine_status()
                assert status == "outdated"


def test_create_icon_colors() -> None:
    """Verify icon creation doesn't crash for all colors."""
    from tray.app import create_icon
    for color in ("green", "yellow", "red"):
        img = create_icon(color)
        assert img.size == (64, 64)


def test_app_imports_without_tray_dependencies() -> None:
    import tray.app as app_module
    assert app_module.pystray is None or hasattr(app_module.pystray, "Icon")
    icon = app_module.create_icon("green")
    assert getattr(icon, "size") == (64, 64)


def main() -> int:
    tests = [
        test_config_manager_load_save,
        test_config_manager_corrupt_file,
        test_config_manager_update_install_state,
        test_config_manager_update_last_error,
        test_win_utils_get_claude_version,
        test_win_utils_get_claude_version_none,
        test_win_utils_is_patch_installed,
        test_win_utils_get_patch_components,
        test_determine_status_not_installed,
        test_determine_status_installed_from_files,
        test_determine_status_uses_configured_app_dir,
        test_determine_status_partial_when_whitelist_missing,
        test_determine_status_outdated,
        test_create_icon_colors,
        test_app_imports_without_tray_dependencies,
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
