#!/usr/bin/env python3
"""Claude Desktop zh-CN Patch — System Tray Monitor.

Shows patch status in the system tray with a right-click menu for:
- Viewing current status
- Installing/updating the patch
- Uninstalling the patch
- Checking for updates
- Enabling/disabling auto-start
- Exiting

Status icon colors:
  Green  = Patch installed, version matches
  Yellow = Patch outdated (Claude has been updated)
  Red    = Patch not installed
"""
from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path

# Ensure tray/parent is in path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tray.config_manager import (
    load_config,
    save_config,
    update_install_state,
    update_check_time,
)
from tray.win_utils import (
    find_claude_package,
    get_claude_version,
    show_toast,
    register_startup,
    unregister_startup,
    is_startup_registered,
    is_admin,
)

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: pystray and Pillow are required.")
    print("Install with: pip install pystray Pillow")
    sys.exit(1)

PATCH_VERSION_FILE = PROJECT_ROOT / "VERSION"


def get_patch_version() -> str:
    """Read the current patch version from VERSION file."""
    if PATCH_VERSION_FILE.exists():
        return PATCH_VERSION_FILE.read_text(encoding="utf-8").strip()
    return "unknown"


def determine_status() -> str:
    """Determine current patch status: 'installed', 'outdated', or 'not_installed'."""
    config = load_config()
    if not config.get("installed"):
        return "not_installed"
    claude_dir = find_claude_package()
    current_claude = get_claude_version(claude_dir)
    installed_claude = config.get("claude_version")
    if current_claude and installed_claude and current_claude != installed_claude:
        return "outdated"
    return "installed"


def create_icon(color: str, size: int = 64) -> Image.Image:
    """Create a simple status icon.

    Colors: 'green', 'yellow', 'red'
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    color_map = {
        "green": (76, 175, 80, 230),
        "yellow": (255, 193, 7, 230),
        "red": (244, 67, 54, 230),
    }
    fill = color_map.get(color, color_map["red"])
    # Draw a filled circle
    margin = 4
    draw.ellipse([margin, margin, size - margin, size - margin], fill=fill)
    # Draw inner white circle
    inner_margin = 18
    draw.ellipse(
        [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
        fill=(255, 255, 255, 200),
    )
    return img


def get_status_icon() -> Image.Image:
    """Get the appropriate icon for current status."""
    status = determine_status()
    color_map = {
        "installed": "green",
        "outdated": "yellow",
        "not_installed": "red",
    }
    return create_icon(color_map.get(status, "red"))


def get_status_text() -> str:
    """Get human-readable status text for the menu."""
    config = load_config()
    status = determine_status()
    claude_ver = get_claude_version()
    patch_ver = get_patch_version()
    lines = []
    if status == "installed":
        lines.append("状态: 已安装 ✓")
    elif status == "outdated":
        lines.append("状态: 需要更新 (Claude 已更新)")
    else:
        lines.append("状态: 未安装")
    lines.append(f"Claude 版本: {claude_ver or '未检测到'}")
    lines.append(f"补丁版本: {patch_ver}")
    if config.get("installed_at"):
        import datetime
        ts = datetime.datetime.fromtimestamp(config["installed_at"])
        lines.append(f"安装时间: {ts.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"开机自启: {'是' if is_startup_registered() else '否'}")
    return "\n".join(lines)


def run_install() -> None:
    """Run the patch installation scripts."""
    if not is_admin():
        show_toast("Claude 中文补丁", "安装需要管理员权限，请以管理员身份运行。")
        return
    show_toast("Claude 中文补丁", "正在安装补丁...")
    script_dir = PROJECT_ROOT / "scripts"
    python_exe = PROJECT_ROOT / "python" / "python.exe"
    if not python_exe.exists():
        python_exe = Path(sys.executable)
    app_dir = find_claude_package()
    if not app_dir:
        show_toast("Claude 中文补丁", "未找到 Claude 安装目录。")
        return
    app_dir_str = str(app_dir)
    # Step 1: JSON resources
    r1 = subprocess.run(
        [str(python_exe), str(script_dir / "patch_windowsapps_json_only.py"), "--app-dir", app_dir_str],
        capture_output=True, text=True, timeout=120,
    )
    # Step 2: JS chunks + font
    r2 = subprocess.run(
        [str(python_exe), str(script_dir / "patch_chunks_zh_cn.py"), "--app-dir", app_dir_str],
        capture_output=True, text=True, timeout=120,
    )
    if r1.returncode == 0 and r2.returncode == 0:
        claude_ver = get_claude_version(app_dir)
        patch_ver = get_patch_version()
        update_install_state(claude_ver or "unknown", patch_ver)
        show_toast("Claude 中文补丁", f"安装成功！Claude {claude_ver}")
    else:
        error = r1.stderr or r2.stderr or "未知错误"
        show_toast("Claude 中文补丁", f"安装失败: {error[:100]}")


def run_uninstall() -> None:
    """Run the patch uninstallation."""
    if not is_admin():
        show_toast("Claude 中文补丁", "卸载需要管理员权限。")
        return
    script_dir = PROJECT_ROOT / "scripts"
    python_exe = PROJECT_ROOT / "python" / "python.exe"
    if not python_exe.exists():
        python_exe = Path(sys.executable)
    app_dir = find_claude_package()
    if not app_dir:
        show_toast("Claude 中文补丁", "未找到 Claude 安装目录。")
        return
    r = subprocess.run(
        [str(python_exe), str(script_dir / "restore_claude_zh_cn_windowsapps.py"), "--app-dir", str(app_dir)],
        capture_output=True, text=True, timeout=120,
    )
    if r.returncode == 0:
        config = load_config()
        config["installed"] = False
        save_config(config)
        show_toast("Claude 中文补丁", "卸载完成，界面已恢复英文。")
    else:
        show_toast("Claude 中文补丁", f"卸载失败: {r.stderr[:100]}")


def check_for_updates(icon: pystray.Icon) -> None:
    """Check if Claude has been updated since last patch install."""
    update_check_time()
    status = determine_status()
    if status == "outdated":
        config = load_config()
        old_ver = config.get("claude_version", "?")
        new_ver = get_claude_version()
        show_toast(
            "Claude 中文补丁",
            f"Claude 已从 {old_ver} 更新到 {new_ver}，请重新安装补丁。",
        )
    elif status == "not_installed":
        show_toast("Claude 中文补丁", "补丁尚未安装。")
    else:
        show_toast("Claude 中文补丁", "补丁已是最新。")


def update_icon(icon: pystray.Icon) -> None:
    """Update the tray icon to reflect current status."""
    icon.icon = get_status_icon()
    icon.title = f"Claude 中文补丁 - {determine_status()}"


class TrayApp:
    """Main tray application class."""

    def __init__(self) -> None:
        self.icon: pystray.Icon | None = None
        self._monitor_thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def _build_menu(self) -> pystray.Menu:
        """Build the tray context menu."""
        status = determine_status()
        auto_start = is_startup_registered()
        return pystray.Menu(
            pystray.MenuItem(
                "状态详情",
                lambda icon, item: show_toast("Claude 中文补丁", get_status_text()),
                default=True,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "安装 / 更新补丁" if status != "installed" else "重新安装补丁",
                lambda icon, item: threading.Thread(target=run_install, daemon=True).start(),
            ),
            pystray.MenuItem(
                "卸载补丁",
                lambda icon, item: threading.Thread(target=run_uninstall, daemon=True).start(),
                enabled=status != "not_installed",
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "检查更新",
                lambda icon, item: threading.Thread(
                    target=check_for_updates, args=(icon,), daemon=True
                ).start(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                f"开机自启: {'开' if auto_start else '关'}",
                self._toggle_auto_start,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self._quit),
        )

    def _toggle_auto_start(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Toggle auto-start on login."""
        if is_startup_registered():
            if unregister_startup():
                show_toast("Claude 中文补丁", "已关闭开机自启。")
        else:
            if register_startup():
                show_toast("Claude 中文补丁", "已开启开机自启。")
        # Rebuild menu to reflect change
        icon.menu = self._build_menu()

    def _quit(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Stop the monitor and exit."""
        self._stop_event.set()
        icon.stop()

    def _monitor_loop(self, icon: pystray.Icon) -> None:
        """Background thread: periodically check for updates."""
        config = load_config()
        interval = config.get("check_interval_minutes", 60) * 60
        while not self._stop_event.wait(timeout=interval):
            new_status = determine_status()
            old_status = icon.title.split(" - ")[-1] if " - " in icon.title else ""
            if new_status != old_status:
                icon.icon = get_status_icon()
                icon.title = f"Claude 中文补丁 - {new_status}"
                icon.menu = self._build_menu()
                if new_status == "outdated":
                    config_data = load_config()
                    old_ver = config_data.get("claude_version", "?")
                    new_ver = get_claude_version()
                    show_toast(
                        "Claude 中文补丁",
                        f"Claude 已更新 ({old_ver} → {new_ver})，请重新安装补丁。",
                    )

    def run(self) -> None:
        """Start the tray application."""
        initial_status = determine_status()
        status_text = {
            "installed": "已安装",
            "outdated": "需要更新",
            "not_installed": "未安装",
        }.get(initial_status, "未知")
        self.icon = pystray.Icon(
            name="claude-zh-cn",
            icon=get_status_icon(),
            title=f"Claude 中文补丁 - {status_text}",
            menu=self._build_menu(),
        )
        # Start background monitor
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(self.icon,),
            daemon=True,
        )
        self._monitor_thread.start()
        # Run the tray event loop (blocks)
        self.icon.run()


def main() -> None:
    """Entry point."""
    app = TrayApp()
    app.run()


if __name__ == "__main__":
    main()