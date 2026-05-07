# Claude Desktop 中文补丁 — 全面升级实施计划

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers-executing-plans to implement.

**Goal:** 将 Claude Desktop 中文补丁从脚本工具升级为有系统托盘管理界面、术语表、多语言框架、主题系统和 CI/CD 自动化的本地化平台。

**Architecture:** 新增 `tray/` 模块提供系统托盘常驻和更新检测；`resources/` 下新增术语表和主题目录；安装脚本参数化支持多语言；GitHub Actions 自动化发布流程。

**Tech Stack:** Python 3.12 (bundled), pystray, Pillow, GitHub Actions

---

## Phase 1: 翻译质量基础设施

### Task 1.1: 创建术语表

**Goal:** 建立统一的翻译术语表，确保翻译一致性。

**Files:**
- Create: `resources/glossary.json`

**Steps:**

- [ ] 创建 `resources/glossary.json`：

```json
{
  "Cowork": {
    "zh": "协作",
    "note": "Claude 的协作模式，不译为'共同工作'或'协同'",
    "tags": ["product", "sidebar"]
  },
  "Plugin": {
    "zh": "插件",
    "note": "通用技术术语",
    "tags": ["tech"]
  },
  "Skill": {
    "zh": "技能",
    "note": "Cowork 中的可执行技能包",
    "tags": ["product"]
  },
  "MCP": {
    "zh": "MCP",
    "note": "Model Context Protocol，保留原文",
    "tags": ["tech", "brand"]
  },
  "Artifacts": {
    "zh": "Artifacts",
    "note": "产品功能名，保留英文",
    "tags": ["product", "brand"]
  },
  "Plugin": {
    "zh": "插件",
    "note": "用户可安装的功能扩展包",
    "tags": ["product"]
  },
  "Connector": {
    "zh": "连接器",
    "note": "第三方服务集成连接",
    "tags": ["product"]
  },
  "Extension": {
    "zh": "扩展",
    "note": "桌面扩展程序",
    "tags": ["product"]
  },
  "Workspace": {
    "zh": "工作区",
    "note": "Cowork 的工作目录",
    "tags": ["product"]
  },
  "Session": {
    "zh": "会话",
    "note": "代码/Cowork 会话",
    "tags": ["product"]
  },
  "Agent": {
    "zh": "Agent",
    "note": "AI 代理，保留英文",
    "tags": ["product"]
  },
  "Token": {
    "zh": "Token",
    "note": "计量单位，保留英文",
    "tags": ["tech"]
  },
  "Prompt": {
    "zh": "提示词",
    "note": "用户输入的指令",
    "tags": ["tech"]
  },
  "Sandbox": {
    "zh": "沙箱",
    "note": "安全隔离环境",
    "tags": ["tech"]
  },
  "VM": {
    "zh": "虚拟机",
    "note": "Virtual Machine",
    "tags": ["tech"]
  },
  "Webhook": {
    "zh": "Webhook",
    "note": "保留英文",
    "tags": ["tech"]
  },
  "Pull Request": {
    "zh": "拉取请求",
    "note": "Git 工作流术语",
    "tags": ["tech"]
  },
  "Cherry-pick": {
    "zh": "Cherry-pick",
    "note": "Git 操作，保留英文",
    "tags": ["tech"]
  },
  "Scheduled task": {
    "zh": "计划任务",
    "note": "定时执行的任务",
    "tags": ["product"]
  },
  "Dispatch": {
    "zh": "调度",
    "note": "任务调度功能",
    "tags": ["product"]
  },
  "Replay": {
    "zh": "回放",
    "note": "会话回放功能",
    "tags": ["product"]
  },
  "Operon": {
    "zh": "实验室",
    "note": "实验性功能标签",
    "tags": ["product"]
  },
  "HIPAA": {
    "zh": "HIPAA",
    "note": "医疗合规标准，保留英文",
    "tags": ["compliance"]
  },
  "BAA": {
    "zh": "BAA",
    "note": "商业关联协议，保留英文",
    "tags": ["compliance"]
  }
}
```

- [ ] 验证 JSON 语法：`python -c "import json; json.load(open('resources/glossary.json', encoding='utf-8'))"`

---

### Task 1.2: 术语一致性检查工具

**Goal:** 在 `check_i18n_coverage.py` 中增加术语一致性检查。

**Files:**
- Modify: `tools/check_i18n_coverage.py`

**Steps:**

- [ ] 在 `check_i18n_coverage.py` 顶部导入 `glossary` 并加载：

```python
GLOSSARY_PATH = RESOURCES / "glossary.json"

def load_glossary() -> dict:
    if GLOSSARY_PATH.exists():
        return json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
    return {}
```

- [ ] 添加术语一致性检查函数（在 `classify_value` 之后）：

```python
def check_glossary_consistency(data: dict, glossary: dict, name: str) -> list[str]:
    """Check if zh-CN translations match the glossary terms."""
    issues = []
    if not glossary:
        return issues

    # Build search patterns from glossary
    for term, info in glossary.items():
        expected_zh = info.get("zh", "")
        if not expected_zh or expected_zh == term:
            continue  # Skip terms that stay in English

        # For each translation value, check if the term appears in English
        # but is NOT translated to the expected Chinese
        for key, value in data.items():
            if not isinstance(value, str):
                continue
            # Skip very short values and format strings
            if len(value) < 3 or value.startswith("{"):
                continue
            # If the English term appears in the value but expected Chinese doesn't
            if term in value and expected_zh not in value:
                # Check if it's a compound term (e.g. "New chat" contains "Chat")
                # Only flag if the term is standalone or at word boundary
                import re
                pattern = r'\b' + re.escape(term) + r'\b'
                if re.search(pattern, value):
                    issues.append(
                        f"  [{name}] Glossary mismatch: key={key}, "
                        f"term='{term}' found but expected '{expected_zh}' not in value: {value[:80]}"
                    )

    return issues
```

- [ ] 在 `main()` 函数中调用术语检查：

```python
    glossary = load_glossary()
    # ... existing code after loading zh_data ...
    glossary_issues = check_glossary_consistency(zh_data, glossary, name)
    all_issues.extend(glossary_issues)
    if glossary_issues:
        print(f"  Glossary: {len(glossary_issues)} inconsistencies")
    else:
        print(f"  Glossary: OK")
```

- [ ] 运行验证：`python tools/check_i18n_coverage.py`

---

### Task 1.3: 更新 KNOWN_OK_PATTERNS 清理可疑条目

**Goal:** 扩展白名单模式，减少 74 条可疑未翻译条目中的误报。

**Files:**
- Modify: `tools/check_i18n_coverage.py`

**Steps:**

- [ ] 在 `KNOWN_OK_PATTERNS` 列表末尾追加以下模式：

```python
    # Social media platforms
    re.compile(r"^(Instagram|Reddit|LinkedIn|TikTok|YouTube|X / Twitter)$"),
    # Cloud/enterprise services
    re.compile(r"^(Google Play|Google Docs|Google Drive|Google Cloud|Google Calendar|Google logo|Google)$"),
    re.compile(r"^(Azure AI Foundry|Microsoft Foundry|Anthropic Sans)$"),
    # Product names
    re.compile(r"^(Claude Slack|Claude Cowork|Claude Free|Claude Platform|Claude Artifacts|Claude Ship|Claude .+)$"),
    re.compile(r"^(Research Labs|Research Labs Premium)$"),
    # Plan names with placeholders
    re.compile(r"^(Pro|Standard|Premium|Enterprise Claude|Custom).+"),
    # Version/size/count format strings
    re.compile(r"^\{.*\}%$"),
    re.compile(r"^\{.*\} (KB|MB|GB)$"),
    # Names with email placeholders
    re.compile(r"^\{name\}.*\{email\}$"),
    re.compile(r"^\{fullName\}.*\{email\}$"),
    # Other format strings with parentheses
    re.compile(r"^（.*\{.*\}.*）$"),
    re.compile(r"^\（.*\）$"),
    # Short labels with symbols
    re.compile(r"^[A-Z][a-z]+ [A-Z][a-z]+$"),
    # HTTP status
    re.compile(r"^HTTP \{status\}$"),
    # Domain-like patterns
    re.compile(r"^\.claude\.app$"),
    re.compile(r"^your-site$"),
    # API key labels
    re.compile(r"^API_KEY$"),
    # ACS URL
    re.compile(r"^ACS URL$"),
    # Mathematical/number formats
    re.compile(r"^.{1}?\{amount\}$"),
    re.compile(r"^\+\{count\}$"),
    re.compile(r"^-\{count\}$"),
    re.compile(r"^\+\{formattedCurrencyAmount\}$"),
    # Progress/percentage
    re.compile(r"^\{progress\}%$"),
    re.compile(r"^\{pct\}%$"),
    # Scale labels
    re.compile(r"^.+ = \{firstLabel\}"),
    # JCT suffix
    re.compile(r"^\+ JCT$"),
    # Feature name placeholder
    re.compile(r"^Claude \{featureName\}$"),
    # Learn safely
    re.compile(r"^\{learnSafely\}"),
    # Label with beta
    re.compile(r"^\{label\}，Beta$"),
    # Local indicator
    re.compile(r"^（\{local\}）$"),
```

- [ ] 运行检查：`python tools/check_i18n_coverage.py`
- [ ] 验证误报数量显著下降（目标：从 74 条降到 <10 条）

---

### Task 1.4: 版本管理规范

**Goal:** 建立版本号规范，使补丁版本与 Claude Desktop 版本对应。

**Files:**
- Modify: `docs/CHANGELOG.md`（头部新增版本说明段落）
- Create: `VERSION`（纯文本文件，存储当前补丁版本号）

**Steps:**

- [ ] 创建 `VERSION` 文件：

```
1.5354.0.1
```

格式说明：`{claude_major}.{claude_minor}.{claude_patch}.{patch_iteration}`

- [ ] 在 `docs/CHANGELOG.md` 头部追加：

```markdown
## Version Scheme

Format: `{claude_version}.{patch_iteration}`

- `claude_version`: The Claude Desktop version this patch targets (e.g., `1.5354.0`)
- `patch_iteration`: Incremental number for translation updates, bug fixes, etc. within the same Claude version (e.g., `.1`, `.2`)

Example: `1.5354.0.1` = first patch release for Claude Desktop v1.5354.0
```

- [ ] 验证文件创建成功

---

### Task 1.5: 术语表辅助翻译生成工具

**Goal:** 创建半自动工具，读取术语表和 en-US 源文件，为新增 key 生成翻译建议。

**Files:**
- Create: `tools/suggest_translations.py`

**Steps:**

- [ ] 创建 `tools/suggest_translations.py`：

```python
#!/usr/bin/env python3
"""Suggest translations for new en-US keys using the glossary.

Reads the glossary and en-US source, finds keys present in en-US but
missing from zh-CN, and generates a suggested translation file with
glossary terms pre-applied.

Usage:
  python tools/suggest_translations.py [--lang zh-CN]
"""
from __future__ import annotations

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
    en_path = find_en_source()
    if not en_path:
        print("en-US source not found. Please specify the correct path.")
        return 1

    en_data = load_json(en_path)
    glossary = load_glossary()

    # Load all existing zh-CN keys
    zh_keys = set()
    for zh_path in ZH_CN_PATHS:
        if zh_path.exists():
            zh_data = load_json(zh_path)
            zh_keys.update(zh_data.keys())

    # Find missing keys
    missing = sorted(set(en_data.keys()) - zh_keys)
    if not missing:
        print("No missing keys found. All en-US keys are present in zh-CN.")
        return 0

    print(f"Found {len(missing)} missing keys.")
    print(f"Glossary has {len(glossary)} terms.\n")

    # Generate suggestions
    suggestions = {}
    for key in missing:
        en_val = en_data[key]
        if isinstance(en_val, dict):
            # Plural form - skip for now
            suggestions[key] = {"en": en_val, "suggestion": "(plural form - manual translation needed)"}
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
```

- [ ] 运行验证：`python tools/suggest_translations.py`

---

## Phase 2: 系统托盘 + 更新检测

### Task 2.1: 配置管理模块

**Goal:** 创建托盘程序的配置持久化模块。

**Files:**
- Create: `tray/__init__.py`
- Create: `tray/config_manager.py`

**Steps:**

- [ ] 创建 `tray/__init__.py`（空文件）

- [ ] 创建 `tray/config_manager.py`：

```python
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
```

- [ ] 验证模块可导入：`python -c "from tray.config_manager import load_config; print(load_config())"`

---

### Task 2.2: Windows 工具模块

**Goal:** 创建 Windows 特有的工具函数（版本检测、管理员权限、通知、任务计划）。

**Files:**
- Create: `tray/win_utils.py`

**Steps:**

- [ ] 创建 `tray/win_utils.py`：

```python
"""Windows-specific utility functions for the tray monitor."""
from __future__ import annotations

import ctypes
import json
import subprocess
from pathlib import Path
from typing import Optional


WINDOWSAPPS_BASE = Path(r"C:\Program Files\WindowsApps")


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
    name = pkg_dir.name       # Claude_1.5354.0.0_x64__pzs8sxrjxfjjc

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

    $template = @"
    <toast>
      <visual>
        <binding template="ToastGeneric">
          <text>{safe_title}</text>
          <text>{safe_message}</text>
        </binding>
      </visual>
    </toast>
"@

    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($template)
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude zh-CN").Show($toast)
    """
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
        )
        return True
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"Toast failed ({e}), falling back to print")
        print(f"  {title}: {message}")
        return False


def register_startup(task_name: str = "ClaudeZhCnTray") -> bool:
    """Register the tray app to start on login via Windows Task Scheduler."""
    script_dir = Path(__file__).resolve().parent.parent
    python_exe = script_dir / "python" / "python.exe"
    tray_script = script_dir / "tray" / "app.py"

    if not python_exe.exists():
        python_exe = Path("python")
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
```

- [ ] 验证模块可导入：`python -c "from tray.win_utils import find_claude_package, get_claude_version; print(get_claude_version())"`

---

### Task 2.3: 系统托盘主程序

**Goal:** 创建系统托盘常驻程序，显示补丁状态并提供管理菜单。

**Files:**
- Create: `tray/app.py`

**Steps:**

- [ ] 安装依赖：`pip install pystray Pillow --break-system-packages --target=python/Lib/site-packages`

- [ ] 创建 `tray/app.py`：

```python
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

import sys
import threading
import time
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

    # Draw "中" character hint (white inner circle)
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

    import subprocess
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

    import subprocess
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
                lambda: show_toast("Claude 中文补丁", get_status_text()),
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
```

- [ ] 验证程序可启动：`python tray/app.py`（在 Windows 上会显示托盘图标）

---

### Task 2.4: 入口脚本和 bat 集成

**Goal:** 创建 bat 快捷方式启动托盘程序，并在主菜单中增加托盘选项。

**Files:**
- Create: `claude-zh-cn-tray.bat`
- Modify: `scripts/claude-zh-cn.ps1`（新增菜单选项 [5] 启动托盘）

**Steps:**

- [ ] 创建 `claude-zh-cn-tray.bat`：

```bat
@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
start "" "%~dp0python\python.exe" "%~dp0tray\app.py"
```

- [ ] 在 `scripts/claude-zh-cn.ps1` 的菜单部分，在 `[4] 刷新状态` 之后、`[0] 退出` 之前插入新选项：

在 `Show-Menu` 函数中：
```powershell
  Write-Host '  [5] 启动系统托盘监视器' -ForegroundColor White
```

在 `switch` 语句中，`'4'` case 之后添加 `'5'` case：
```powershell
    '5' {
      Write-Host ''
      Write-Info '正在启动系统托盘监视器...'
      $trayScript = Join-Path $scriptDir '..\tray\app.py'
      if (Test-Path $trayScript) {
        Start-Process -FilePath $python.Source -ArgumentList "`"$trayScript`"" -WindowStyle Hidden
        Write-OK '托盘监视器已在后台启动。'
      } else {
        Write-Err '托盘脚本未找到。'
      }
      Write-Host ''
      Read-Host '按 Enter 返回菜单'
    }
```

- [ ] 更新菜单提示范围为 0-5

---

### Task 2.5: 托盘程序测试

**Goal:** 编写托盘程序核心逻辑的单元测试（不需要 GUI 的部分）。

**Files:**
- Create: `tools/test_tray.py`

**Steps:**

- [ ] 创建 `tools/test_tray.py`：

```python
#!/usr/bin/env python3
"""Unit tests for tray monitor modules (non-GUI parts)."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest import mock

# Add project root to path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_config_manager_load_save() -> None:
    from tray.config_manager import load_config, save_config, PATCH_CONFIG_PATH

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
```

- [ ] 运行测试：`python tools/test_tray.py`

---

## Phase 3: 多语言框架 + 主题系统

### Task 3.1: 多语言资源目录重构

**Goal:** 将翻译资源按语言分目录存放，支持多语言扩展。

**Files:**
- Create: `resources/zh-CN/desktop.json` (copy from desktop-zh-CN.json)
- Create: `resources/zh-CN/frontend.json` (copy from frontend-zh-CN.json)
- Create: `resources/zh-CN/statsig.json` (copy from statsig-zh-CN.json)
- Create: `resources/zh-CN/glossary.json` (copy from glossary.json)
- Modify: `scripts/patch_windowsapps_json_only.py` (add --lang parameter)

**Steps:**

- [ ] 创建 `resources/zh-CN/` 目录并复制现有资源：

```bash
mkdir -p resources/zh-CN
cp resources/desktop-zh-CN.json resources/zh-CN/desktop.json
cp resources/frontend-zh-CN.json resources/zh-CN/frontend.json
cp resources/statsig-zh-CN.json resources/zh-CN/statsig.json
cp resources/glossary.json resources/zh-CN/glossary.json
```

- [ ] 修改 `scripts/patch_windowsapps_json_only.py`，在文件顶部添加语言参数支持：

```python
# 在 RESOURCES 定义之后添加
def resolve_language_resources(lang: str = "zh-CN") -> list[tuple[Path, Path]]:
    """Resolve resource file paths for a given language.

    Returns list of (source, destination) pairs.
    Supports both new (resources/{lang}/) and legacy (resources/) layouts.
    """
    lang_dir = RESOURCES / lang
    if lang_dir.exists() and (lang_dir / "desktop.json").exists():
        # New layout
        return [
            (lang_dir / "desktop.json", None),  # dst filled in main()
            (lang_dir / "frontend.json", None),
            (lang_dir / "statsig.json", None),
        ]
    # Legacy layout (zh-CN only)
    return [
        (RESOURCES / "desktop-zh-CN.json", None),
        (RESOURCES / "frontend-zh-CN.json", None),
        (RESOURCES / "statsig-zh-CN.json", None),
    ]
```

- [ ] 在 `main()` 函数中添加 `--lang` 参数：

```python
    parser.add_argument("--lang", type=str, default="zh-CN",
                        help="Language code (default: zh-CN)")
```

- [ ] 更新文件列表构建逻辑以使用语言参数

---

### Task 3.2: 自定义主题系统

**Goal:** 扩展现有的字体注入机制，支持颜色主题。

**Files:**
- Create: `resources/themes/warm-dark.json`
- Create: `resources/themes/cool-light.json`
- Modify: `scripts/patch_chunks_zh_cn.py`（在字体注入脚本中增加主题支持）

**Steps:**

- [ ] 创建 `resources/themes/` 目录

- [ ] 创建 `resources/themes/warm-dark.json`：

```json
{
  "id": "warm-dark",
  "name": "暖色深色",
  "description": "偏暖色调的深色主题",
  "css": ":root { --bg-000: #1a1614; --bg-050: #211d1a; --bg-100: #2a2520; --bg-200: #342e28; --border-200: #3d3630; --border-300: #4a4238; --text-300: #a89880; --text-400: #c4b098; --text-500: #e8dcd0; }"
}
```

- [ ] 创建 `resources/themes/cool-light.json`：

```json
{
  "id": "cool-light",
  "name": "清爽浅色",
  "description": "偏蓝调的浅色主题",
  "css": ":root { --bg-000: #f8fafc; --bg-050: #f1f5f9; --bg-100: #e8eef4; --border-200: #d0dbe8; --border-300: #b8c8d8; --text-300: #64748b; --text-400: #475569; --text-500: #1e293b; }"
}
```

- [ ] 在 `patch_chunks_zh_cn.py` 的 `font_inject_script()` 函数中，增加主题加载逻辑：

在 CSS 注入部分的 `style.textContent` 模板末尾，添加主题 CSS 变量的合并逻辑。具体是在 `applyFont` 函数中追加：

```javascript
  function applyTheme() {{
    const themeId = localStorage.getItem("claude-zh-cn-theme");
    if (!themeId) return;
    const THEMES = {themes_json};
    const theme = THEMES.find(t => t.id === themeId);
    if (!theme) return;
    let themeStyle = document.getElementById("claude-zh-cn-theme-style");
    if (!themeStyle) {{
      themeStyle = document.createElement("style");
      themeStyle.id = "claude-zh-cn-theme-style";
      document.head.appendChild(themeStyle);
    }}
    themeStyle.textContent = theme.css;
  }}
```

- [ ] 在主题面板中添加主题选择下拉（与字体面板统一）

---

### Task 3.4: GitHub Actions — PR 检查

**Goal:** 设置 CI，PR 提交时自动验证翻译质量。

**Files:**
- Create: `.github/workflows/pr-check.yml`

**Steps:**

- [ ] 创建 `.github/workflows/` 目录

- [ ] 创建 `.github/workflows/pr-check.yml`：

```yaml
name: PR Check

on:
  pull_request:
    branches: [main]
    paths:
      - 'resources/**'
      - 'scripts/**'
      - 'tools/**'

jobs:
  validate:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Validate JSON resources
        run: python tools/validate_resources.py

      - name: Check i18n coverage
        run: python tools/check_i18n_coverage.py
        continue-on-error: true

      - name: Run tests
        run: python tools/test_patch_behaviors.py
```

- [ ] 验证 YAML 语法正确

---

### Task 3.5: GitHub Actions — 自动发布

**Goal:** 打 tag 时自动打包并创建 GitHub Release。

**Files:**
- Create: `.github/workflows/release.yml`

**Steps:**

- [ ] 创建 `.github/workflows/release.yml`：

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Get version from tag
        id: version
        shell: bash
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Validate before release
        run: |
          python tools/validate_resources.py
          python tools/test_patch_behaviors.py

      - name: Create release archive
        shell: bash
        run: |
          # Create the release directory structure
          RELEASE_DIR="claude-zh-cn-${{ steps.version.outputs.VERSION }}"
          mkdir -p "$RELEASE_DIR"

          # Copy project files (exclude .git, __pycache__, etc.)
          cp claude-zh-cn.bat "$RELEASE_DIR/"
          cp claude-zh-cn-tray.bat "$RELEASE_DIR/"
          cp VERSION "$RELEASE_DIR/"
          cp -r resources "$RELEASE_DIR/"
          cp -r scripts "$RELEASE_DIR/"
          cp -r tools "$RELEASE_DIR/"
          cp -r tray "$RELEASE_DIR/"
          cp -r docs "$RELEASE_DIR/"
          cp -r python "$RELEASE_DIR/"
          cp README.md "$RELEASE_DIR/"

          # Remove unnecessary files
          find "$RELEASE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
          find "$RELEASE_DIR" -name "*.pyc" -delete 2>/dev/null || true

          # Create zip
          7z a "claude-zh-cn-v${{ steps.version.outputs.VERSION }}.zip" "$RELEASE_DIR/"

      - name: Generate release notes
        id: notes
        shell: bash
        run: |
          # Extract the latest changelog entry
          NOTES=$(sed -n '/^## [0-9]/,/^## [0-9]/{/^## [0-9]/{p;q};p}' docs/CHANGELOG.md)
          echo "NOTES<<EOF" >> $GITHUB_OUTPUT
          echo "$NOTES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          name: "Claude Desktop 中文补丁 v${{ steps.version.outputs.VERSION }}"
          body: |
            ## Claude Desktop 中文补丁 v${{ steps.version.outputs.VERSION }}

            ${{ steps.notes.outputs.NOTES }}

            ### 安装方法
            1. 下载 `claude-zh-cn-v${{ steps.version.outputs.VERSION }}.zip`
            2. 解压后右键 `claude-zh-cn.bat` → 以管理员身份运行
            3. 选择 `[1] 安装中文补丁`

            ### 系统托盘
            双击 `claude-zh-cn-tray.bat` 启动托盘监视器，自动检测 Claude 更新。
          files: |
            claude-zh-cn-v${{ steps.version.outputs.VERSION }}.zip
          draft: false
          prerelease: false
```

- [ ] 验证 YAML 语法

---

### Task 3.6: CONTRIBUTING.md 和 Issue 模板

**Goal:** 建立社区协译的贡献指南和 Issue/PR 模板。

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `.github/ISSUE_TEMPLATE/translation-suggestion.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

**Steps:**

- [ ] 创建 `CONTRIBUTING.md`：

```markdown
# 贡献指南

感谢你对 Claude Desktop 中文补丁的关注！

## 翻译贡献

### 如何提交翻译建议

1. **Fork** 本仓库
2. 编辑 `resources/zh-CN/` 下对应的 JSON 文件
3. 提交 Pull Request

### 翻译规范

- 术语请参考 `resources/zh-CN/glossary.json`
- 保留品牌名和产品名的英文原文（如 Claude、MCP、GitHub）
- 保留占位符变量不变（如 `{name}`、`{count}`）
- 使用简体中文，避免繁体字
- 对话风格保持自然、简洁
- 不要翻译 JSON 的 key，只修改 value

### 快速贡献

如果不想 Fork，也可以直接提交 [Translation Suggestion Issue](../../issues/new?template=translation-suggestion.yml)，
维护者会审核后更新。

## 开发贡献

### 环境要求

- Windows 10/11
- Python 3.12+（项目内置了 Python 环境）
- 已安装 Claude Desktop

### 运行测试

```bash
python tools/test_patch_behaviors.py
python tools/test_tray.py
python tools/validate_resources.py
python tools/check_i18n_coverage.py
```

### 项目结构

```
├── claude-zh-cn.bat           # 入口脚本
├── claude-zh-cn-tray.bat      # 托盘监视器启动
├── resources/                 # 翻译资源
│   ├── zh-CN/                 # 中文翻译
│   │   ├── desktop.json
│   │   ├── frontend.json
│   │   ├── statsig.json
│   │   └── glossary.json      # 术语表
│   └── themes/                # 主题文件
├── tray/                      # 系统托盘程序
├── scripts/                   # 安装/卸载脚本
├── tools/                     # 维护工具和测试
└── docs/                      # 文档
```
```

- [ ] 创建 `.github/ISSUE_TEMPLATE/` 目录

- [ ] 创建 `.github/ISSUE_TEMPLATE/translation-suggestion.yml`：

```yaml
name: Translation Suggestion
description: Suggest a translation improvement
title: "[翻译] "
labels: ["translation"]
body:
  - type: input
    id: key
    attributes:
      label: Translation Key
      description: The JSON key in the resource file
      placeholder: e.g., +7sd9hoyZA
    validations:
      required: true

  - type: input
    id: file
    attributes:
      label: Resource File
      description: Which resource file contains this key
      options:
        - desktop.json
        - frontend.json
        - statsig.json
    validations:
      required: true

  - type: textarea
    id: current
    attributes:
      label: Current Translation
      description: The current Chinese translation (if any)
    validations:
      required: false

  - type: textarea
    id: suggested
    attributes:
      label: Suggested Translation
      description: Your suggested Chinese translation
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Context
      description: Where this string appears in the UI and any additional context
    validations:
      required: false
```

- [ ] 创建 `.github/PULL_REQUEST_TEMPLATE.md`：

```markdown
## Description

Brief description of what this PR changes.

## Checklist

- [ ] I have checked the [glossary](resources/zh-CN/glossary.json) for consistent terminology
- [ ] I have not modified any JSON keys (only values)
- [ ] I have preserved all placeholder variables (`{name}`, `{count}`, etc.)
- [ ] I have kept brand names in English (Claude, MCP, GitHub, etc.)
- [ ] `python tools/validate_resources.py` passes
```

---

## Phase Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1 | 1.1 - 1.5 | 翻译质量基础设施（术语表、检查工具、版本管理） |
| 2 | 2.1 - 2.5 | 系统托盘 + 更新检测 |
| 3 | 3.1 - 3.6 | 多语言框架、主题系统、CI/CD、社区协译 |

## Dependencies Between Tasks

```
1.1 (glossary) → 1.2 (glossary check) → 1.5 (suggest tool)
1.3 (patterns) → standalone
1.4 (version)  → 2.1 (config uses version)

2.1 (config) → 2.2 (win_utils) → 2.3 (tray app) → 2.4 (bat integration) → 2.5 (tests)

3.1 (multi-lang) → needs 1.4 (version) done
3.2 (themes)     → standalone
3.4 (PR CI)      → needs 1.2 (check tool) done
3.5 (release CI) → needs 1.4 (version) done
3.6 (contributing) → standalone
```

## Execution Recommendation

Phase 1 可以全部串行完成（约 1-2 小时）。
Phase 2 是最复杂的部分，建议每个 Task 完成后立即测试。
Phase 3 可以与 Phase 2 并行（3.2、3.4、3.5、3.6 都不依赖 Phase 2）。
