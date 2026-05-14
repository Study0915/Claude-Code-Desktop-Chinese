"""Windows-specific utility functions for the tray monitor."""
from __future__ import annotations

import ctypes
import os
import subprocess
from pathlib import Path
from typing import Optional

WINDOWSAPPS_BASE = Path(r"C:\Program Files\WindowsApps")


def is_patch_installed(app_dir: Optional[Path] = None) -> bool:
    """Detect whether the zh-CN patch is actually present in Claude app directory.

    Checks for the existence of zh-CN.json resource files.
    """
    if app_dir is None:
        app_dir = find_claude_package()
    if app_dir is None:
        return False
    res = app_dir / "resources"
    zh_desktop = res / "zh-CN.json"
    zh_frontend = res / "ion-dist" / "i18n" / "zh-CN.json"
    zh_statsig = res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json"
    return zh_desktop.exists() and zh_frontend.exists() and zh_statsig.exists()


def get_patch_components(app_dir: Optional[Path] = None) -> dict[str, bool]:
    """Return detailed patch component status for diagnostics."""
    if app_dir is None:
        app_dir = find_claude_package()
    if app_dir is None:
        return {
            "app_found": False,
            "desktop_json": False,
            "frontend_json": False,
            "statsig_json": False,
            "whitelist": False,
            "locale": False,
        }

    res = app_dir / "resources"
    desktop_json = res / "zh-CN.json"
    frontend_json = res / "ion-dist" / "i18n" / "zh-CN.json"
    statsig_json = res / "ion-dist" / "i18n" / "statsig" / "zh-CN.json"
    assets_dir = res / "ion-dist" / "assets" / "v1"
    whitelist = False
    for path in (assets_dir.glob("index-*.js") if assets_dir.exists() else []):
        try:
            if '"zh-CN"' in path.read_text(encoding="utf-8", errors="ignore"):
                whitelist = True
                break
        except OSError:
            continue

    locale = False
    appdata = os.environ.get("APPDATA")
    config_base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
    config_path = config_base / "Claude-3p" / "config.json"
    if config_path.exists():
        try:
            import json

            locale = json.loads(config_path.read_text(encoding="utf-8")).get("locale") == "zh-CN"
        except (json.JSONDecodeError, OSError):
            locale = False

    return {
        "app_found": True,
        "desktop_json": desktop_json.exists(),
        "frontend_json": frontend_json.exists(),
        "statsig_json": statsig_json.exists(),
        "whitelist": whitelist,
        "locale": locale,
    }


def is_admin() -> bool:
    """Check if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (OSError, AttributeError):
        return False


def find_claude_package() -> Optional[Path]:
    """Auto-detect Claude package under WindowsApps.

    Returns the .../app directory path, or None if not found.
    """
    if not WINDOWSAPPS_BASE.exists():
        return None
    candidates = sorted(
        WINDOWSAPPS_BASE.glob("Claude_*_x64__*/app/resources/en-US.json"),
        reverse=True,
    )
    if candidates:
        return candidates[0].parent.parent  # .../app
    return None


def find_claude_executable(app_dir: Optional[Path] = None) -> Optional[Path]:
    """Find a launchable Claude executable near the app directory."""
    if app_dir is None:
        app_dir = find_claude_package()
    if app_dir is None:
        return None

    candidates = [
        app_dir / "Claude.exe",
        app_dir / "claude.exe",
        app_dir.parent / "Claude.exe",
        app_dir.parent / "claude.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    try:
        found = sorted(app_dir.glob("*.exe"))
    except OSError:
        found = []
    return found[0] if found else None


def open_path(path: Path) -> bool:
    """Open a file or folder in Explorer."""
    try:
        os.startfile(str(path))
        return True
    except OSError as e:
        print(f"Failed to open {path}: {e}")
        return False


def launch_claude(app_dir: Optional[Path] = None) -> bool:
    """Launch Claude Desktop from the detected package."""
    exe = find_claude_executable(app_dir)
    if exe is None:
        return False
    try:
        subprocess.Popen([str(exe)], cwd=str(exe.parent))
        return True
    except OSError as e:
        print(f"Failed to launch Claude: {e}")
        return False


def get_claude_version(app_dir: Optional[Path] = None) -> Optional[str]:
    """Extract Claude version from the package directory name.

    Example: "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" -> "1.5354.0.0"
    """
    if app_dir is None:
        app_dir = find_claude_package()
    if app_dir is None:
        return None
    # The app dir is .../Claude_VERSION_HASH/app, so parent is the package dir
    pkg_dir = app_dir.parent  # .../Claude_VERSION_HASH
    name = pkg_dir.name        # Claude_1.5354.0.0_x64__pzs8sxrjxfjjc
    # Parse version from directory name
    parts = name.split("_")
    if len(parts) >= 2:
        return parts[1]  # "1.5354.0.0"
    return None


def show_toast(title: str, message: str, duration: int = 5) -> bool:
    """Show a Windows toast notification using PowerShell.

    Falls back to print() if toast is not available.
    """
    # Escape single quotes for PowerShell
    safe_title = title.replace("'", "''")
    safe_message = message.replace("'", "''")
    ps_script = f"""
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
    $template = @'
    <toast>
      <visual>
        <binding template="ToastGeneric">
          <text>{safe_title}</text>
          <text>{safe_message}</text>
        </binding>
      </visual>
    </toast>
'@
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($template)
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude zh-CN").Show($toast)
    """
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
        )
        if result.returncode != 0:
            print(f"Toast failed (exit {result.returncode}), falling back to print")
            print(f"  {title}: {message}")
            return False
        return True
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"Toast failed ({e}), falling back to print")
        print(f"  {title}: {message}")
        return False


def register_startup(task_name: str = "ClaudeZhCnTray") -> bool:
    """Register the tray app to start on login via Windows Task Scheduler."""
    script_dir = Path(__file__).resolve().parent.parent
    python_exe = script_dir / "python" / "pythonw.exe"
    tray_script = script_dir / "tray" / "app.py"
    if not python_exe.exists():
        python_exe = script_dir / "python" / "python.exe"
    if not python_exe.exists():
        python_exe = Path("pythonw")
    if not tray_script.exists():
        print(f"Error: tray script not found: {tray_script}")
        return False
    cmd = [
        "schtasks", "/Create", "/TN", task_name,
        "/TR", f'"{python_exe}" "{tray_script}"',
        "/SC", "ONLOGON",
        "/RL", "HIGHEST",
        "/F",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"Failed to register startup: {e}")
        return False


def unregister_startup(task_name: str = "ClaudeZhCnTray") -> bool:
    """Remove the startup task."""
    try:
        result = subprocess.run(
            ["schtasks", "/Delete", "/TN", task_name, "/F"],
            capture_output=True, text=True, timeout=30,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def is_startup_registered(task_name: str = "ClaudeZhCnTray") -> bool:
    """Check if the startup task exists."""
    try:
        result = subprocess.run(
            ["schtasks", "/Query", "/TN", task_name],
            capture_output=True, text=True, timeout=15,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False
