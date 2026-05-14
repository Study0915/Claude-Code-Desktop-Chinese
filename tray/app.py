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
import os
from dataclasses import dataclass
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
    update_last_error,
)
from tray.win_utils import (
    find_claude_package,
    get_claude_version,
    get_patch_components,
    show_toast,
    register_startup,
    unregister_startup,
    is_startup_registered,
    is_admin,
    launch_claude,
    open_path,
)

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None
    Image = None
    ImageDraw = None


@dataclass
class SimpleIcon:
    """Small dependency-free icon placeholder for tests and diagnostics."""

    color: str
    size: tuple[int, int]

PATCH_VERSION_FILE = PROJECT_ROOT / "VERSION"


def get_patch_version() -> str:
    """Read the current patch version from VERSION file."""
    if PATCH_VERSION_FILE.exists():
        return PATCH_VERSION_FILE.read_text(encoding="utf-8").strip()
    return "unknown"


def determine_status() -> str:
    """Determine current patch status."""
    config = load_config()
    claude_dir = find_claude_package()
    if claude_dir is None and config.get("app_dir"):
        configured = Path(config["app_dir"])
        if configured.exists():
            claude_dir = configured

    if claude_dir is None:
        return "not_installed"

    current_claude = get_claude_version(claude_dir)
    installed_claude = config.get("claude_version")
    if config.get("installed") and current_claude and installed_claude and current_claude != installed_claude:
        return "outdated"

    components = get_patch_components(claude_dir)
    patch_complete = (
        components["desktop_json"]
        and components["frontend_json"]
        and components["statsig_json"]
        and components["whitelist"]
    )
    if patch_complete:
        return "installed"

    has_any_patch_piece = any(
        components[name]
        for name in ("desktop_json", "frontend_json", "statsig_json", "whitelist", "locale")
    )
    if has_any_patch_piece or config.get("installed"):
        return "partial"

    return "not_installed"


def get_claude_app_dir() -> Path | None:
    """Resolve the best Claude app directory for tray actions."""
    config = load_config()
    app_dir = find_claude_package()
    if app_dir is not None:
        return app_dir
    configured = config.get("app_dir")
    if configured:
        path = Path(configured)
        if path.exists():
            return path
    return None


def create_icon(color: str, size: int = 64):
    """Create a simple status icon.

    Colors: 'green', 'yellow', 'red'
    """
    if Image is None or ImageDraw is None:
        return SimpleIcon(color=color, size=(size, size))
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
        "partial": "yellow",
        "not_installed": "red",
    }
    return create_icon(color_map.get(status, "red"))


def get_status_text() -> str:
    """Get human-readable status text for the menu."""
    config = load_config()
    status = determine_status()
    app_dir = get_claude_app_dir()
    claude_ver = get_claude_version(app_dir)
    patch_ver = get_patch_version()
    components = get_patch_components(app_dir)
    status_label = {
        "installed": "已安装 ✓",
        "outdated": "需要更新 (Claude 已更新)",
        "partial": "安装不完整，请重新安装",
        "not_installed": "未安装",
    }.get(status, status)
    lines = []
    lines.append(f"状态: {status_label}")
    lines.append(f"Claude 版本: {claude_ver or '未检测到'}")
    lines.append(f"补丁版本: {patch_ver}")
    if app_dir:
        lines.append(f"安装路径: {app_dir}")
    if config.get("installed_at"):
        import datetime
        ts = datetime.datetime.fromtimestamp(config["installed_at"])
        lines.append(f"安装时间: {ts.strftime('%Y-%m-%d %H:%M')}")
    lines.append(
        "组件: "
        f"desktop={'✓' if components['desktop_json'] else '×'}, "
        f"frontend={'✓' if components['frontend_json'] else '×'}, "
        f"statsig={'✓' if components['statsig_json'] else '×'}, "
        f"白名单={'✓' if components['whitelist'] else '×'}, "
        f"locale={'✓' if components['locale'] else '×'}"
    )
    if config.get("last_error"):
        lines.append(f"最近错误: {config['last_error']}")
    lines.append(f"开机自启: {'是' if is_startup_registered() else '否'}")
    return "\n".join(lines)


def launch_elevated_batch(argument: str) -> bool:
    """Launch the main batch file through UAC for admin-only actions."""
    batch = PROJECT_ROOT / "claude-zh-cn.bat"
    if not batch.exists():
        return False
    safe_batch = str(batch).replace("'", "''")
    safe_argument = argument.replace("'", "''")
    command = f"Start-Process -FilePath '{safe_batch}' -ArgumentList '{safe_argument}' -Verb RunAs"
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            timeout=20,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def run_install() -> None:
    """Run the patch installation scripts."""
    if not is_admin():
        if launch_elevated_batch("/auto"):
            show_toast("Claude 中文补丁", "已请求管理员权限，授权后将自动安装。")
        else:
            message = "安装需要管理员权限，请以管理员身份运行。"
            update_last_error(message)
            show_toast("Claude 中文补丁", message)
        return
    show_toast("Claude 中文补丁", "正在安装补丁...")
    script_dir = PROJECT_ROOT / "scripts"
    python_exe = PROJECT_ROOT / "python" / "python.exe"
    if not python_exe.exists():
        python_exe = Path(sys.executable)
    app_dir = get_claude_app_dir()
    if not app_dir:
        message = "未找到 Claude 安装目录。"
        update_last_error(message)
        show_toast("Claude 中文补丁", message)
        return
    app_dir_str = str(app_dir)
    # Step 1: JSON resources
    try:
        r1 = subprocess.run(
            [str(python_exe), str(script_dir / "patch_windowsapps_json_only.py"), "--app-dir", app_dir_str],
            capture_output=True, text=True, timeout=120,
        )
        # Step 2: JS chunks + font
        r2 = subprocess.run(
            [str(python_exe), str(script_dir / "patch_chunks_zh_cn.py"), "--app-dir", app_dir_str],
            capture_output=True, text=True, timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        message = f"安装失败: {e}"
        update_last_error(message)
        show_toast("Claude 中文补丁", message[:160])
        return
    if r1.returncode == 0 and r2.returncode == 0:
        claude_ver = get_claude_version(app_dir)
        patch_ver = get_patch_version()
        update_install_state(claude_ver or "unknown", patch_ver, app_dir)
        show_toast("Claude 中文补丁", f"安装成功！Claude {claude_ver}")
    else:
        error = r1.stderr or r2.stderr or r1.stdout or r2.stdout or "未知错误"
        update_last_error(error[:500])
        show_toast("Claude 中文补丁", f"安装失败: {error[:100]}")


def run_uninstall() -> None:
    """Run the patch uninstallation."""
    if not is_admin():
        if launch_elevated_batch("/uninstall"):
            show_toast("Claude 中文补丁", "已请求管理员权限，授权后将自动卸载。")
        else:
            message = "卸载需要管理员权限。"
            update_last_error(message)
            show_toast("Claude 中文补丁", message)
        return
    script_dir = PROJECT_ROOT / "scripts"
    python_exe = PROJECT_ROOT / "python" / "python.exe"
    if not python_exe.exists():
        python_exe = Path(sys.executable)
    app_dir = get_claude_app_dir()
    if not app_dir:
        message = "未找到 Claude 安装目录。"
        update_last_error(message)
        show_toast("Claude 中文补丁", message)
        return
    try:
        r = subprocess.run(
            [str(python_exe), str(script_dir / "restore_claude_zh_cn_windowsapps.py"), "--app-dir", str(app_dir)],
            capture_output=True, text=True, timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        message = f"卸载失败: {e}"
        update_last_error(message)
        show_toast("Claude 中文补丁", message[:160])
        return
    if r.returncode == 0:
        config = load_config()
        config["installed"] = False
        config["last_error"] = None
        save_config(config)
        show_toast("Claude 中文补丁", "卸载完成，界面已恢复英文。")
    else:
        error = r.stderr or r.stdout or "未知错误"
        update_last_error(error[:500])
        show_toast("Claude 中文补丁", f"卸载失败: {error[:100]}")


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
    elif status == "partial":
        show_toast("Claude 中文补丁", "补丁安装不完整，请重新安装。")
    else:
        show_toast("Claude 中文补丁", "补丁已是最新。")


def update_icon(icon: pystray.Icon) -> None:
    """Update the tray icon to reflect current status."""
    icon.icon = get_status_icon()
    icon.title = f"Claude 中文补丁 - {determine_status()}"


def run_in_background(target, *args) -> None:
    """Run a tray action in a daemon thread."""
    threading.Thread(target=target, args=args, daemon=True).start()


def show_status() -> None:
    """Display current status as a toast."""
    show_toast("Claude 中文补丁", get_status_text())


def open_claude() -> None:
    """Launch Claude Desktop if an executable can be found."""
    app_dir = get_claude_app_dir()
    if not launch_claude(app_dir):
        show_toast("Claude 中文补丁", "未找到可启动的 Claude 程序。")


def open_install_dir() -> None:
    """Open the detected Claude app directory."""
    app_dir = get_claude_app_dir()
    if app_dir and app_dir.exists():
        open_path(app_dir)
    else:
        show_toast("Claude 中文补丁", "未找到 Claude 安装目录。")


def open_config_dir() -> None:
    """Open the patch config directory."""
    config_dir = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Claude-3p"
    config_dir.mkdir(parents=True, exist_ok=True)
    open_path(config_dir)


class TrayApp:
    """Main tray application class."""

    def __init__(self) -> None:
        self.icon: pystray.Icon | None = None
        self._monitor_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._last_status: str = ""

    def _build_menu(self) -> pystray.Menu:
        """Build the tray context menu."""
        status = determine_status()
        auto_start = is_startup_registered()
        return pystray.Menu(
            pystray.MenuItem("状态详情", lambda icon, item: show_status(), default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "安装 / 更新补丁" if status != "installed" else "重新安装补丁",
                lambda icon, item: run_in_background(run_install),
            ),
            pystray.MenuItem(
                "卸载补丁",
                lambda icon, item: run_in_background(run_uninstall),
                enabled=status != "not_installed",
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "检查更新",
                lambda icon, item: run_in_background(check_for_updates, icon),
            ),
            pystray.MenuItem(
                "打开 Claude",
                lambda icon, item: run_in_background(open_claude),
            ),
            pystray.MenuItem(
                "打开安装目录",
                lambda icon, item: run_in_background(open_install_dir),
            ),
            pystray.MenuItem(
                "打开配置目录",
                lambda icon, item: run_in_background(open_config_dir),
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
            if new_status != self._last_status:
                self._last_status = new_status
                status_text = {
                    "installed": "已安装",
                    "outdated": "需要更新",
                    "partial": "安装不完整",
                    "not_installed": "未安装",
                }.get(new_status, "未知")
                icon.icon = get_status_icon()
                icon.title = f"Claude 中文补丁 - {status_text}"
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
        if pystray is None:
            print("系统托盘界面缺少 pystray / Pillow 依赖。")
            print("当前补丁状态如下：")
            print(get_status_text())
            print("可先使用 claude-zh-cn.bat 安装、卸载和查看状态。")
            sys.exit(1)

        initial_status = determine_status()
        self._last_status = initial_status
        status_text = {
            "installed": "已安装",
            "outdated": "需要更新",
            "partial": "安装不完整",
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
