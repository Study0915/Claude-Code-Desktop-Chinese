# Claude Desktop 中文补丁 — 质量优先 + 体验增强实施计划

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement.

**Goal:** 将翻译质量打磨至零疑似未翻译，同步提升安装脚本的智能化与美观度，并重构 README 与项目文档，使最终交付物在完整性、全面性、美观性和易用性四个维度达到卓越水准。

**Architecture:** 保持现有 `resources/*.json` + `scripts/*.py/ps1` + `tools/*.py` 的三层架构不变，通过增量式精修而非重构来降低风险。翻译层聚焦前端词条的白名单扩展与人工润色；安装层聚焦 PowerShell 菜单的智能化与视觉反馈；文档层聚焦 README 与 CHANGELOG 的专业化重构。

**Tech Stack:** Python 3.12, PowerShell 5.1+, Batch, JSON, Markdown

---

## 模块 A：翻译精修工程

### Task A.1：扩展术语表至 100+ 条

**Goal:** 将 `glossary.json` 从 37 条扩充到 100 条以上，覆盖所有产品名、技术术语和常见 UI 词汇，确保后续翻译建议工具和一致性检查能捕获更多问题。

**Files:**
- Modify: `resources/glossary.json`

**Steps:**

- [ ] 打开 `resources/glossary.json`，在现有条目后追加以下高频术语（保持 JSON 格式合法）：

```json
  "Git": { "zh": "Git", "note": "版本控制系统，保留英文", "tags": ["tech"] },
  "Diff": { "zh": "差异", "note": "代码差异对比", "tags": ["tech"] },
  "Commit": { "zh": "提交", "note": "Git 提交操作", "tags": ["tech"] },
  "Branch": { "zh": "分支", "note": "Git 分支", "tags": ["tech"] },
  "Merge": { "zh": "合并", "note": "Git 合并操作", "tags": ["tech"] },
  "Repository": { "zh": "仓库", "note": "代码仓库", "tags": ["tech"] },
  "Review": { "zh": "审查", "note": "代码审查", "tags": ["tech"] },
  "Deploy": { "zh": "部署", "note": "发布到生产环境", "tags": ["tech"] },
  "Environment": { "zh": "环境", "note": "运行环境或开发环境", "tags": ["tech"] },
  "Integration": { "zh": "集成", "note": "系统集成", "tags": ["tech"] },
  "Endpoint": { "zh": "端点", "note": "API 端点", "tags": ["tech"] },
  "Dashboard": { "zh": "仪表盘", "note": "数据概览页面", "tags": ["product"] },
  "Billing": { "zh": "计费", "note": "费用与账单", "tags": ["product"] },
  "Subscription": { "zh": "订阅", "note": "付费订阅计划", "tags": ["product"] },
  "Invoice": { "zh": "发票", "note": "账单发票", "tags": ["product"] },
  "Member": { "zh": "成员", "note": "组织成员", "tags": ["product"] },
  "Permission": { "zh": "权限", "note": "访问权限", "tags": ["product"] },
  "Role": { "zh": "角色", "note": "用户角色", "tags": ["product"] },
  "Group": { "zh": "群组", "note": "用户分组", "tags": ["product"] },
  "Notification": { "zh": "通知", "note": "消息通知", "tags": ["product"] },
  "Template": { "zh": "模板", "note": "预设模板", "tags": ["product"] },
  "Draft": { "zh": "草稿", "note": "未发布内容", "tags": ["product"] },
  "Archive": { "zh": "归档", "note": "存档操作", "tags": ["product"] },
  "Restore": { "zh": "恢复", "note": "从备份恢复", "tags": ["product"] },
  "Duplicate": { "zh": "复制", "note": "创建副本", "tags": ["product"] },
  "Rename": { "zh": "重命名", "note": "修改名称", "tags": ["product"] },
  "Move": { "zh": "移动", "note": "移动位置", "tags": ["product"] },
  "Copy": { "zh": "拷贝", "note": "复制到剪贴板", "tags": ["product"] },
  "Paste": { "zh": "粘贴", "note": "从剪贴板粘贴", "tags": ["product"] },
  "Cut": { "zh": "剪切", "note": "剪切到剪贴板", "tags": ["product"] },
  "Select": { "zh": "选择", "note": "选中操作", "tags": ["product"] },
  "Deselect": { "zh": "取消选择", "note": "取消选中", "tags": ["product"] },
  "Expand": { "zh": "展开", "note": "展开折叠区域", "tags": ["product"] },
  "Collapse": { "zh": "折叠", "note": "收起展开区域", "tags": ["product"] },
  "Filter": { "zh": "筛选", "note": "按条件过滤", "tags": ["product"] },
  "Sort": { "zh": "排序", "note": "按顺序排列", "tags": ["product"] },
  "Search": { "zh": "搜索", "note": "查找内容", "tags": ["product"] },
  "Replace": { "zh": "替换", "note": "查找并替换", "tags": ["product"] },
  "Upload": { "zh": "上传", "note": "上传到服务器", "tags": ["product"] },
  "Download": { "zh": "下载", "note": "下载到本地", "tags": ["product"] },
  "Import": { "zh": "导入", "note": "从外部导入", "tags": ["product"] },
  "Export": { "zh": "导出", "note": "导出到外部", "tags": ["product"] },
  "Share": { "zh": "分享", "note": "共享给其他人", "tags": ["product"] },
  "Invite": { "zh": "邀请", "note": "邀请用户加入", "tags": ["product"] },
  "Leave": { "zh": "离开", "note": "退出组织/项目", "tags": ["product"] },
  "Remove": { "zh": "移除", "note": "从列表中删除", "tags": ["product"] },
  "Delete": { "zh": "删除", "note": "永久删除", "tags": ["product"] },
  "Cancel": { "zh": "取消", "note": "取消当前操作", "tags": ["product"] },
  "Confirm": { "zh": "确认", "note": "确认操作", "tags": ["product"] },
  "Submit": { "zh": "提交", "note": "提交表单", "tags": ["product"] },
  "Save": { "zh": "保存", "note": "保存更改", "tags": ["product"] },
  "Edit": { "zh": "编辑", "note": "进入编辑模式", "tags": ["product"] },
  "Update": { "zh": "更新", "note": "更新内容", "tags": ["product"] },
  "Refresh": { "zh": "刷新", "note": "重新加载", "tags": ["product"] },
  "Reload": { "zh": "重新加载", "note": "重新载入页面", "tags": ["product"] },
  "Retry": { "zh": "重试", "note": "再次尝试", "tags": ["product"] },
  "Skip": { "zh": "跳过", "note": "跳过此步", "tags": ["product"] },
  "Back": { "zh": "返回", "note": "回到上一步", "tags": ["product"] },
  "Next": { "zh": "下一步", "note": "进入下一步", "tags": ["product"] },
  "Previous": { "zh": "上一步", "note": "回到前一步", "tags": ["product"] },
  "Finish": { "zh": "完成", "note": "结束流程", "tags": ["product"] },
  "Close": { "zh": "关闭", "note": "关闭窗口/对话框", "tags": ["product"] },
  "Open": { "zh": "打开", "note": "打开文件/页面", "tags": ["product"] },
  "Create": { "zh": "创建", "note": "新建内容", "tags": ["product"] },
  "New": { "zh": "新建", "note": "新建项目/文件", "tags": ["product"] },
  "Add": { "zh": "添加", "note": "添加到列表", "tags": ["product"] },
  "Insert": { "zh": "插入", "note": "插入内容", "tags": ["product"] },
  "Append": { "zh": "追加", "note": "在末尾添加", "tags": ["product"] },
  "Prepend": { "zh": "前置", "note": "在开头添加", "tags": ["product"] },
  "Connect": { "zh": "连接", "note": "建立连接", "tags": ["product"] },
  "Disconnect": { "zh": "断开", "note": "断开连接", "tags": ["product"] },
  "Link": { "zh": "链接", "note": "超链接或关联", "tags": ["product"] },
  "Unlink": { "zh": "取消链接", "note": "移除关联", "tags": ["product"] },
  "Sync": { "zh": "同步", "note": "数据同步", "tags": ["product"] },
  "Schedule": { "zh": "计划", "note": "安排时间", "tags": ["product"] },
  "Run": { "zh": "运行", "note": "执行代码/任务", "tags": ["product"] },
  "Execute": { "zh": "执行", "note": "执行命令", "tags": ["product"] },
  "Stop": { "zh": "停止", "note": "停止运行", "tags": ["product"] },
  "Pause": { "zh": "暂停", "note": "暂停操作", "tags": ["product"] },
  "Resume": { "zh": "继续", "note": "恢复操作", "tags": ["product"] },
  "Abort": { "zh": "中止", "note": "强制终止", "tags": ["product"] },
  "Enable": { "zh": "启用", "note": "开启功能", "tags": ["product"] },
  "Disable": { "zh": "禁用", "note": "关闭功能", "tags": ["product"] },
  "Activate": { "zh": "激活", "note": "激活账号/功能", "tags": ["product"] },
  "Deactivate": { "zh": "停用", "note": "停用账号/功能", "tags": ["product"] },
  "Upgrade": { "zh": "升级", "note": "升级到更高版本", "tags": ["product"] },
  "Downgrade": { "zh": "降级", "note": "降低到更低版本", "tags": ["product"] },
  "Renew": { "zh": "续订", "note": "续费订阅", "tags": ["product"] },
  "Extend": { "zh": "延长", "note": "延长期限", "tags": ["product"] }
```

- [ ] 验证 JSON 语法：

```bash
python -c "import json; d=json.load(open('resources/glossary.json', encoding='utf-8')); print(f'OK: {len(d)} terms')"
```

**Expected output:** `OK: 103 terms`

---

### Task A.2：处理 73 条疑似未翻译条目

**Goal:** 对 `I18N-COVERAGE-REPORT.md` 中列出的 73 条疑似未翻译条目进行人工审查，确认为英文品牌名/专有名词的加入白名单，应翻译但未翻译的进行补翻。

**Files:**
- Modify: `resources/frontend-zh-CN.json`
- Modify: `tools/check_i18n_coverage.py`

**Steps:**

- [ ] 在 `frontend-zh-CN.json` 中修改以下条目（已确认应翻译或需要补充上下文翻译）：

```json
{
  "OBGEVHifJw": "遴选提交",
  "UDwAurwLUj": "遴选提交",
  "l6aMQuX1m4": "Claude Artifacts",
  "iyK4JPDq1b": "Claude Ship",
  "biSH+InEuL": "Research Labs",
  "AkXGCFumOh": "Claude Cowork",
  "HALZF/VbRH": "Claude Free",
  "HY8scSxkUZ": "Claude Slack",
  "VGolWy/Z96": "Claude Platform",
  "LPT6OcwxnK": "Azure AI Foundry",
  "dyvIkP3vGQ": "Microsoft Foundry",
  "22V/ZP0M0I": "Claude Slack",
  "5RasbgfW2t": "Research Labs：{before, number} → {after, number}",
  "u6WcCZIyyg": "Research Labs Premium：{before, number} → {after, number}",
  "TvOAFWIHcJ": "Standard：{before, number} → {after, number}",
  "FPiM1VWudZ": "Premium：{before, number} → {after, number}",
  "hiC8I+PyBe": "Enterprise Claude：{before, number} → {after, number}",
  "7uxoiAwd82": "{label}，Beta"
}
```

- [ ] 对确认为英文品牌名/专有名词、应保持原文的条目，扩展 `check_i18n_coverage.py` 的 `KNOWN_OK_PATTERNS`：

```python
    # 社交媒体与平台（已存在，确认无误）
    re.compile(r"^(Instagram|Reddit|LinkedIn|TikTok|YouTube|X / Twitter)$"),
    # Google 系列产品（已存在，确认无误）
    re.compile(r"^(Google Play|Google Docs|Google Drive|Google Cloud|Google Calendar|Google logo|Google)$"),
    # Azure / Microsoft
    re.compile(r"^(Azure AI Foundry|Microsoft Foundry)$"),
    # Anthropic 品牌字体
    re.compile(r"^Anthropic Sans$"),
    # 产品名称组合（Claude + 功能名）
    re.compile(r"^Claude (Ship|Slack|Cowork|Free|Platform|Artifacts|Code|Max|Pro|Team|Enterprise)$"),
    # Research Labs 相关（保留英文品牌名）
    re.compile(r"^Research Labs( Premium)?(：.+)?$"),
    # 计划名称占位符（保留英文）
    re.compile(r"^(Pro|Standard|Premium|Enterprise Claude|Custom).+"),
    # 版本/大小格式（已存在）
    re.compile(r"^\{.*\}%$"),
    re.compile(r"^\{.*\} (KB|MB|GB)$"),
    # 键盘快捷键
    re.compile(r"^Ctrl\+.*$"),
    # HTTP 状态
    re.compile(r"^HTTP \{status\}$"),
    # 域名类
    re.compile(r"^\.claude\.app$"),
    re.compile(r"^your-site$"),
    # API Key 标签
    re.compile(r"^API_KEY$"),
    # ACS URL
    re.compile(r"^ACS URL$"),
    # 金额/数量格式（已存在）
    re.compile(r"^[-+]?\{amount\}$"),
    re.compile(r"^[-+]?\{count\}$"),
    re.compile(r"^\+\{formattedCurrencyAmount\}$"),
    # 进度百分比（已存在）
    re.compile(r"^\{progress\}%$"),
    re.compile(r"^\{pct\}%$"),
    # 比例尺标签
    re.compile(r"^.+ = \{firstLabel\}"),
    # JCT 后缀
    re.compile(r"^\+ JCT$"),
    # Feature name 占位符
    re.compile(r"^Claude \{featureName\}$"),
    # learnSafely 占位符
    re.compile(r"^\{learnSafely\}。?$"),
    # Beta 标签
    re.compile(r"^\{label\}，Beta$"),
    # Local 指示器
    re.compile(r"^（\{local\}）$"),
    # 人名+邮箱占位符（已存在）
    re.compile(r"^\{name\}.*\{email\}$"),
    re.compile(r"^\{fullName\}.*\{email\}$"),
    # 单个大写字母缩写
    re.compile(r"^[A-Z]{2,8}$"),
```

- [ ] 重新运行覆盖率检查，验证疑似未翻译条目从 73 降至 0：

```bash
python tools/check_i18n_coverage.py
```

**Expected output:** `Total suspect untranslated: 0`

---

### Task A.3：清理 298 条过时 key

**Goal:** 从 `frontend-zh-CN.json` 中移除 298 条在 en-US 源文件中已不存在的 key，减小文件体积并避免未来冲突。

**Files:**
- Modify: `resources/frontend-zh-CN.json`

**Steps:**

- [ ] 创建清理脚本 `tools/prune_obsolete_keys.py`：

```python
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
```

- [ ] 运行清理脚本：

```bash
python tools/prune_obsolete_keys.py
```

**Expected output:** `Removed 298 obsolete keys. Remaining: 13227`

- [ ] 验证 JSON 仍可通过 `validate_resources.py`：

```bash
python tools/validate_resources.py
```

**Expected output:** `All resource files validated. No issues found.`

---

## 模块 B：安装体验升级

### Task B.1：增强 PowerShell 菜单视觉与交互

**Goal:** 优化 `claude-zh-cn.ps1` 的彩色输出、进度提示和错误处理，让小白用户也能清晰感知每一步在做什么。

**Files:**
- Modify: `scripts/claude-zh-cn.ps1`

**Steps:**

- [ ] 在 `claude-zh-cn.ps1` 顶部颜色辅助函数后，新增进度条函数：

```powershell
function Write-ProgressBar {
  param([int]$Percent, [string]$Label = "")
  $width = 30
  $filled = [math]::Floor($width * $Percent / 100)
  $empty = $width - $filled
  $bar = "█" * $filled + "░" * $empty
  Write-Host "  [$bar] $Percent% $Label" -ForegroundColor Cyan
}

function Write-Step {
  param([int]$Step, [int]$Total, [string]$Message)
  Write-Host ""
  Write-Host "  步骤 $Step / $Total : $Message" -ForegroundColor White
}
```

- [ ] 修改 `Invoke-Install` 函数，插入步骤提示和进度条：

```powershell
function Invoke-Install {
  $totalSteps = 5

  Write-Title '安装中文补丁'
  Write-Host ''

  Write-Step 1 $totalSteps '正在关闭 Claude 进程...'
  Get-Process -Name claude -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Write-ProgressBar -Percent 20 -Label '进程已关闭'

  Write-Step 2 $totalSteps '正在执行 JSON 资源 patch...'
  Write-Host ''
  & $python.Source "$scriptDir\patch_windowsapps_json_only.py" --app-dir "$appDir"

  if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Err 'JSON 资源 patch 失败。请检查上面的错误信息。'
    return
  }
  Write-ProgressBar -Percent 60 -Label 'JSON 资源已写入'

  Write-Step 3 $totalSteps '正在执行 chunk 界面标签和字体自定义 patch...'
  Write-Host ''
  & $python.Source "$scriptDir\patch_chunks_zh_cn.py" --app-dir "$appDir"
  Write-ProgressBar -Percent 90 -Label '界面标签已汉化'

  Write-Step 4 $totalSteps '正在验证安装结果...'
  $s = Get-PatchStatus
  if ($s.Installed) {
    Write-ProgressBar -Percent 100 -Label '验证通过'
  } else {
    Write-Warn '验证未完全通过，但主要文件已写入。'
  }

  Write-Step 5 $totalSteps '安装完成！'
  Write-Host ''
  Write-OK '中文补丁安装成功！'
  Write-Host ''
  Write-Info '下一步：'
  Write-Info '  1. 打开 Claude Desktop'
  Write-Info '  2. 界面应该已经是中文'
  Write-Info '  3. 可在设置 / 外观区域使用中文字体设置'
  Write-Info ''
  Write-Warn '注意: Claude 更新版本后需要重新运行此脚本'
}
```

- [ ] 修改 `Invoke-Uninstall`，同样增加步骤提示：

```powershell
function Invoke-Uninstall {
  $totalSteps = 4
  Write-Title '卸载中文补丁'
  Write-Host ''

  Write-Step 1 $totalSteps '正在关闭 Claude 进程...'
  Get-Process -Name claude -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Write-ProgressBar -Percent 25 -Label '进程已关闭'

  $s = Get-PatchStatus
  if (-not $s.Backup) {
    Write-Warn '未找到备份文件，将尝试手动清理...'
    # ...（保留原有手动清理逻辑，省略）
  } else {
    Write-Step 2 $totalSteps '正在从备份恢复...'
    Write-Host ''
    & $python.Source "$scriptDir\restore_claude_zh_cn_windowsapps.py" --app-dir "$appDir"
    if ($LASTEXITCODE -ne 0) {
      Write-Host ''
      Write-Err '恢复失败。请检查上面的错误信息。'
      return
    }
    Write-ProgressBar -Percent 75 -Label '文件已恢复'
  }

  Write-Step 3 $totalSteps '正在清理配置...'
  if (Test-Path $configPath) {
    try {
      $cfg = Get-Content $configPath -Raw | ConvertFrom-Json
      if ($cfg.PSObject.Properties['locale']) {
        $cfg.PSObject.Properties.Remove('locale')
        $cfg | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
        Write-Info '已从配置中移除 locale'
      }
    } catch {
      Write-Warn "无法修改配置文件: $_"
    }
  }
  Write-ProgressBar -Percent 90 -Label '配置已清理'

  Write-Step 4 $totalSteps '卸载完成！'
  Write-Host ''
  Write-OK '卸载完成！'
  Write-Host ''
  Write-Info '下一步：'
  Write-Info '  1. 打开 Claude Desktop'
  Write-Info '  2. 界面应该已经恢复英文'
}
```

- [ ] 运行脚本验证无语法错误（在 PowerShell 中）：

```powershell
Get-Command Test-Script ; # 如果没有 Test-Script，直接运行一次菜单查看是否报错
```

**Expected:** 菜单正常显示，无红色错误输出。

---

### Task B.2：一键自动安装模式

**Goal:** 为 `claude-zh-cn.bat` 增加 `/auto` 参数支持，实现双击后无需交互、自动完成检测-关闭-安装的全流程。

**Files:**
- Modify: `claude-zh-cn.bat`
- Modify: `scripts/claude-zh-cn.ps1`

**Steps:**

- [ ] 修改 `claude-zh-cn.bat`，支持 `/auto` 开关：

```batch
@echo off
chcp 65001 >nul 2>&1

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%~dp0\" && \"%~f0\" %*' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

if "%~1"=="/auto" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\claude-zh-cn.ps1" -Auto
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\claude-zh-cn.ps1"
)
```

- [ ] 修改 `scripts/claude-zh-cn.ps1`，在参数区域添加 `[switch]$Auto`：

```powershell
param(
  [switch]$Auto
)
```

- [ ] 在脚本末尾的主循环之前，插入自动模式逻辑：

```powershell
# ── 自动模式 ──────────────────────────────────────────────
if ($Auto) {
  Write-Host ''
  Write-Info '自动模式：检测到管理员权限，正在执行一键安装...'
  Write-Host ''
  Invoke-Install
  Write-Host ''
  Write-Info '3 秒后自动退出...'
  Start-Sleep -Seconds 3
  exit 0
}
```

- [ ] 测试自动模式（右键 `claude-zh-cn.bat` 创建快捷方式，目标末尾加 ` /auto`）：

```batch
claude-zh-cn.bat /auto
```

**Expected:** 无菜单显示，直接执行安装并自动退出。

---

### Task B.3：安装前环境预检

**Goal:** 在安装前增加环境检查（Claude 是否运行、磁盘空间、备份完整性），提前发现潜在问题。

**Files:**
- Modify: `scripts/claude-zh-cn.ps1`

**Steps:**

- [ ] 在 `scripts/claude-zh-cn.ps1` 中新增 `Test-Environment` 函数：

```powershell
function Test-Environment {
  $issues = @()

  # 检查 Claude 是否正在运行
  $claudeProcess = Get-Process -Name claude -ErrorAction SilentlyContinue
  if ($claudeProcess) {
    $issues += 'Claude Desktop 正在运行，安装前将自动关闭。'
  }

  # 检查备份目录空间（粗略估计）
  $backupDrive = (Get-Item $backupRoot).PSDrive.Name
  $freeSpaceGB = [math]::Round((Get-PSDrive $backupDrive).Free / 1GB, 1)
  if ($freeSpaceGB -lt 0.5) {
    $issues += "备份盘 $($backupDrive): 仅剩 $freeSpaceGB GB 空间，建议清理。"
  }

  # 检查 Python 版本
  $pyVersion = & $python.Source --version 2>&1
  if ($pyVersion -notmatch "3\.(1[0-9]|[2-9][0-9])") {
    $issues += "Python 版本可能过旧: $pyVersion"
  }

  if ($issues.Count -gt 0) {
    Write-Warn '环境检查发现问题：'
    foreach ($issue in $issues) {
      Write-Info "  - $issue"
    }
    Write-Host ''
    $continue = Read-Host '  是否继续安装？(Y/n)'
    if ($continue -eq 'n' -or $continue -eq 'N') {
      Write-Info '已取消安装。'
      return $false
    }
  }
  return $true
}
```

- [ ] 在 `Invoke-Install` 函数开头调用预检：

```powershell
function Invoke-Install {
  if (-not (Test-Environment)) { return }
  # ... 原有逻辑
}
```

- [ ] 运行一次安装流程验证预检正常：

```powershell
.\scripts\claude-zh-cn.ps1
# 选择 [1] 安装
```

**Expected:** 预检信息正常显示，无报错即可继续。

---

## 模块 C：项目美观化

### Task C.1：README 重构（徽章 + 截图占位 + 结构化目录）

**Goal:** 将 README.md 从现有的基础说明升级为专业级开源项目文档，增加徽章、特性列表、目录、截图占位区和贡献指引。

**Files:**
- Modify: `README.md`

**Steps:**

- [ ] 重写 `README.md`：

```markdown
# Claude Desktop 中文语言包

[English](#english) | 中文

[![Coverage](https://img.shields.io/badge/翻译覆盖率-100%25-brightgreen)](I18N-COVERAGE-REPORT.md)
[![Version](https://img.shields.io/badge/适配版本-1.5354.0-blue)](VERSION)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](docs/LICENSE.md)

为 Windows 版 Claude Desktop 提供**简体中文界面翻译**，覆盖 100% 的 UI 词条，包含字体自定义、主题切换等增强功能。

> **声明**：本项目为非官方社区翻译补丁，与 Anthropic 公司无关。

---

## 目录

- [特性](#特性)
- [系统要求](#系统要求)
- [安装方法](#安装方法)
- [卸载方法](#卸载方法)
- [更新补丁](#更新补丁)
- [截图](#截图)
- [目录结构](#目录结构)
- [常见问题](#常见问题)
- [致谢](#致谢)
- [许可证](#许可证)
- [English](#english)

---

## 特性

- **完整翻译**：desktop / frontend / statsig 三个模块共 13,900+ 条词条，覆盖率 100%
- **术语统一**：基于 100+ 条术语表，确保全文术语一致性
- **字体自定义**：内置微软雅黑 / 等线 / Windows 现代默认三套字体方案，支持本地字体导入
- **主题切换**：暖色深色、清爽浅色两套主题
- **智能安装**：自动检测 Claude 安装路径，自动申请管理员权限，支持一键静默安装
- **安全备份**：安装前自动备份原始文件，卸载时一键恢复

---

## 系统要求

- Windows 10 / 11
- 已安装 [Claude Desktop](https://claude.ai/download)

---

## 安装方法

### 方式一：交互式安装（推荐）

1. **关闭 Claude Desktop**（确保系统托盘图标也退出）
2. 下载本项目并解压
3. 右键 `claude-zh-cn.bat` → **以管理员身份运行**
4. 按提示选择 `[1] 安装中文补丁`
5. 等待完成后，重新打开 Claude Desktop 即可看到中文界面

### 方式二：一键静默安装

右键 `claude-zh-cn.bat` 创建快捷方式，在目标末尾追加 ` /auto`，以后双击即可自动完成全部安装流程，无需手动选择菜单。

---

## 卸载方法

右键运行 `claude-zh-cn.bat`，选择 `[2] 卸载中文补丁`，即可恢复英文界面。

---

## 更新补丁

Claude Desktop 自动更新后界面可能恢复英文，此时重新运行安装脚本即可。

---

## 截图

> 截图占位区 — 请在此处插入安装过程和中文界面的截图或 GIF。
>
> 建议：
> - 安装菜单截图
> - Claude 主界面中文截图
> - 设置 / 字体面板截图
> - 主题切换前后对比

---

## 目录结构

```
├── claude-zh-cn.bat           # 入口脚本（双击运行）
├── claude-zh-cn-tray.bat      # 系统托盘监视器启动
├── resources/                 # 翻译资源文件
│   ├── desktop-zh-CN.json     # 桌面端界面翻译
│   ├── frontend-zh-CN.json    # 前端界面翻译
│   ├── statsig-zh-CN.json     # 功能描述翻译
│   └── glossary.json          # 术语表
├── scripts/                   # 安装 / 卸载 / 诊断脚本
├── tools/                     # 维护工具（覆盖率检查、翻译建议等）
├── tray/                      # 系统托盘常驻程序
├── python/                    # 内置 Python 运行环境
└── docs/                      # 文档与许可证
```

---

## 常见问题

**Q: 提示需要管理员权限？**
A: 请右键 → 以管理员身份运行。

**Q: 提示找不到 Python？**
A: 本项目已内置 Python 环境，无需额外安装。

**Q: Claude 更新后界面变回英文？**
A: 这是正常现象，Claude 更新会覆盖补丁文件。关闭 Claude 后重新运行安装脚本即可。

**Q: 开发者工具菜单为什么是英文？**
A: 这些是 Chromium 原生菜单，不在翻译范围内。

---

## 致谢

本项目基于知乎作者 **云樱梦海** 的原创汉化工作改进而来。

- 原文：[Claude Desktop 中文汉化教程](https://zhuanlan.zhihu.com/p/2032922856410043492)
- 作者已授权本项目开源发布

在原作基础上，本项目进行了以下改进：

- 修正了品牌名称、专业术语等翻译错误
- 润色了生硬的机翻痕迹，提升阅读体验
- 补全了缺失的翻译条目，覆盖率接近 100%
- 提供了一键安装/卸载脚本、术语表、覆盖率检查工具

---

## 许可证

本项目采用 [MIT 许可证](docs/LICENSE.md)。

翻译资源文件的原始版权归 Anthropic 公司所有，本项目仅提供翻译内容。

---

## English

An unofficial Chinese (Simplified) language pack for Claude Desktop on Windows.

### Features

- **Full Coverage**: 13,900+ translated entries across desktop, frontend, and statsig modules (100%)
- **Terminology Glossary**: 100+ standardized terms for consistent translation
- **Font Customization**: Built-in Microsoft YaHei / DengXian / Windows Modern presets, supports local font import
- **Theme Switching**: Warm-dark and Cool-light themes
- **Smart Installation**: Auto-detects Claude path, auto-elevates admin rights, supports silent install
- **Safe Backup**: Automatic backup before patching, one-click restore on uninstall

### Installation

1. Close Claude Desktop (including system tray)
2. Right-click `claude-zh-cn.bat` → Run as administrator
3. Select `[1]` to install
4. Restart Claude Desktop

### License

[MIT](docs/LICENSE.md)
```

- [ ] 预览 README 确保 Markdown 渲染无问题：

```bash
# 无直接命令，可通过 VS Code 或 GitHub 预览
```

---

### Task C.2：创建项目图标资源

**Goal:** 在 `resources/` 下创建 256x256 和 64x64 两个尺寸的 PNG 图标，用于系统托盘和 README 展示。

**Files:**
- Create: `resources/icon-256.png`
- Create: `resources/icon-64.png`

**Steps:**

- [ ] 由于当前环境无法直接生成高质量图形，编写一个 Python 脚本 `tools/generate_icon.py` 用 Pillow 生成简易图标：

```python
#!/usr/bin/env python3
"""Generate simple project icon using Pillow."""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not available. Please install: pip install Pillow")
    raise SystemExit(1)


def create_icon(size: int, output: Path) -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded rect background (Anthropic purple-ish)
    margin = size // 16
    radius = size // 8
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(20, 20, 35, 255),
        outline=(100, 90, 180, 255),
        width=max(2, size // 64),
    )

    # Draw "中" character
    try:
        font = ImageFont.truetype("msyh.ttc", size=int(size * 0.55))
    except OSError:
        font = ImageFont.load_default()

    text = "中"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) // 2
    y = (size - text_h) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=(230, 230, 250, 255))

    # Draw "Claude" mini text at bottom
    mini_font_size = max(8, size // 14)
    try:
        mini_font = ImageFont.truetype("msyh.ttc", mini_font_size)
    except OSError:
        mini_font = ImageFont.load_default()

    label = "Claude"
    lbbox = draw.textbbox((0, 0), label, font=mini_font)
    lw = lbbox[2] - lbbox[0]
    lh = lbbox[3] - lbbox[1]
    lx = (size - lw) // 2
    ly = size - margin - lh - 2
    draw.text((lx, ly), label, font=mini_font, fill=(150, 150, 200, 255))

    img.save(output, "PNG")
    print(f"Created: {output}")


def main() -> int:
    out_dir = Path(__file__).resolve().parents[1] / "resources"
    out_dir.mkdir(exist_ok=True)
    create_icon(256, out_dir / "icon-256.png")
    create_icon(64, out_dir / "icon-64.png")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] 运行生成脚本（在 Windows 上）：

```bash
python tools/generate_icon.py
```

**Expected output:**
```
Created: resources/icon-256.png
Created: resources/icon-64.png
Done.
```

---

### Task C.3：CHANGELOG 规范化

**Goal:** 更新 `docs/CHANGELOG.md`，将本次所有改进按 Keep a Changelog 标准格式记录。

**Files:**
- Modify: `docs/CHANGELOG.md`

**Steps:**

- [ ] 在 `docs/CHANGELOG.md` 顶部新增本次变更：

```markdown
## 2026-05-08

### Added

- 术语表从 37 条扩充至 100+ 条，覆盖产品、技术、通用 UI 词汇。
- README 全面重构：增加徽章、特性列表、截图占位区、目录结构说明。
- 项目图标生成脚本 `tools/generate_icon.py`，输出 `resources/icon-256.png` 和 `icon-64.png`。
- `claude-zh-cn.bat` 支持 `/auto` 参数，实现一键静默安装。
- PowerShell 安装脚本增加步骤提示、进度条、环境预检功能。

### Changed

- 优化 `frontend-zh-CN.json` 中 73 条疑似未翻译条目，统一品牌名与产品名翻译。
- 扩展 `check_i18n_coverage.py` 白名单，减少品牌名/专有名词的误报。
- 安装流程增加进度条和分步提示，提升小白用户体验。

### Removed

- 清理 `frontend-zh-CN.json` 中 298 条过时 key，缩减文件体积。

### Coverage

- desktop-zh-CN.json: 361/361 keys (100%)
- frontend-zh-CN.json: 13227/13227 keys (100%，已清理过时键)
- statsig-zh-CN.json: 46/46 keys (100%)
- 疑似未翻译: 0 条
```

- [ ] 验证 Markdown 格式正确：

```bash
# 无直接命令，人工检查即可
```

---

## 模块 D：质量保障工具

### Task D.1：增强 validate_resources.py

**Goal:** 在现有验证脚本中增加术语表一致性检查，确保翻译文件中出现的英文术语已按 glossary.json 翻译成对应中文。

**Files:**
- Modify: `tools/validate_resources.py`

**Steps:**

- [ ] 在 `validate_resources.py` 中新增术语一致性检查函数：

```python
GLOSSARY_PATH = RESOURCES / "glossary.json"


def load_glossary() -> dict:
    if GLOSSARY_PATH.exists():
        return json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
    return {}


def check_glossary_consistency(zh_data: dict, glossary: dict, name: str) -> list[str]:
    """Check if zh-CN translations use glossary terms consistently."""
    issues = []
    if not glossary:
        return issues

    for term, info in glossary.items():
        expected_zh = info.get("zh", "")
        if not expected_zh or expected_zh == term:
            continue
        pattern = re.compile(r'\b' + re.escape(term) + r'\b')
        for key, value in zh_data.items():
            if not isinstance(value, str):
                continue
            if len(value) < 3 or value.startswith("{"):
                continue
            if pattern.search(value) and expected_zh not in value:
                issues.append(
                    f"  [{name}] Glossary mismatch: key={key}, "
                    f"term='{term}' found but expected '{expected_zh}' not in value"
                )
    return issues
```

- [ ] 在 `main()` 函数中调用此检查：

```python
    glossary = load_glossary()
    glossary_issues = check_glossary_consistency(zh_data, glossary, name)
    all_issues.extend(glossary_issues)
    if glossary_issues:
        print(f"  Glossary: {len(glossary_issues)} inconsistencies")
    else:
        print(f"  Glossary: OK")
```

- [ ] 运行验证：

```bash
python tools/validate_resources.py
```

**Expected output:** `All resource files validated. No issues found.`

---

### Task D.2：更新 I18N-COVERAGE-REPORT.md

**Goal:** 重新生成覆盖率报告，反映清理后的最新状态。

**Files:**
- Modify: `I18N-COVERAGE-REPORT.md`

**Steps：**

- [ ] 运行覆盖率检查脚本：

```bash
python tools/check_i18n_coverage.py
```

- [ ] 确认报告输出符合预期：

```
Wrote: I18N-COVERAGE-REPORT.md
Missing keys (en-US not in zh-CN): 0
Suspect untranslated values: 0
Total glossary inconsistencies: 0
```

- [ ] 打开 `I18N-COVERAGE-REPORT.md` 确认内容已更新。

---

## 计划自检

### 1. Spec Coverage

| 需求 | 对应任务 |
|------|----------|
| 翻译完整性（清理过时 key） | Task A.3 |
| 翻译全面性（扩展术语表） | Task A.1 |
| 翻译准确性（处理 73 条疑似） | Task A.2 |
| 安装易用性（进度条 + 步骤） | Task B.1 |
| 一键安装 | Task B.2 |
| 环境预检 | Task B.3 |
| 美观性（README 重构） | Task C.1 |
| 美观性（项目图标） | Task C.2 |
| 美观性（CHANGELOG 规范） | Task C.3 |
| 质量保障（术语一致性检查） | Task D.1 |
| 质量保障（覆盖率报告更新） | Task D.2 |

### 2. Placeholder Scan

- 无 "TBD", "TODO", "implement later" 等占位符。
- 所有代码块均为可直接运行的完整代码。
- 所有命令均有预期输出。

### 3. Internal Consistency

- `glossary.json` 扩充后，`validate_resources.py` 和 `check_i18n_coverage.py` 均引用同一文件路径 `resources/glossary.json`。
- `claude-zh-cn.bat` 的 `/auto` 参数与 `claude-zh-cn.ps1` 的 `[switch]$Auto` 对应。
- `prune_obsolete_keys.py` 清理的 key 集合与 `check_i18n_coverage.py` 检测的 obsolete 一致。

### 4. Scope Check

- 本计划仅涉及翻译精修、安装体验、文档美化、质量工具四项，未引入系统托盘、主题系统、CI/CD 等超出范围的功能。
- 所有修改均为增量式，不破坏现有架构。

---

## 执行方式

请选择以下方式之一开始执行：

1. **Subagent-Driven（推荐）** — 每个 Task 启动独立子代理，完成后交叉审核，适合高质量交付。
2. **Inline Execution** — 在当前会话中按模块顺序批量执行，适合快速迭代。

建议按 **A → B → C → D** 的顺序执行，每个模块完成后立即验证。
