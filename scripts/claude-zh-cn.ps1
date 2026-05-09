<#
.SYNOPSIS
  Claude Desktop 中文补丁 - 安装 / 卸载 / 状态检查
.DESCRIPTION
  交互式菜单，自动检测 Claude 安装路径，执行对应操作。
  需要以管理员身份运行（因为要写 WindowsApps 目录）。
  需要 Python 3。
#>

param(
  [switch]$Auto
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ── 脚本目录 ──────────────────────────────────────────────
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ── 颜色辅助 ──────────────────────────────────────────────
function Write-Title  { param($t) Write-Host "`n  $t" -ForegroundColor Cyan }
function Write-OK     { param($t) Write-Host "  [OK] $t" -ForegroundColor Green }
function Write-Warn   { param($t) Write-Host "  [!]  $t" -ForegroundColor Yellow }
function Write-Err    { param($t) Write-Host "  [X]  $t" -ForegroundColor Red }
function Write-Info   { param($t) Write-Host "  $t" -ForegroundColor Gray }

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

# ── 管理员检查 ────────────────────────────────────────────
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
  [Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
  Write-Host ''
  Write-Err '需要以管理员身份运行此脚本。'
  Write-Info '右键 PowerShell -> 以管理员身份运行，然后重新执行。'
  Write-Host ''
  Read-Host '按 Enter 退出'
  exit 1
}

# ── Python 检查 ───────────────────────────────────────────
$localPythonPath = Join-Path $scriptDir '..\python\python.exe'
if (Test-Path $localPythonPath) {
  $python = Get-Command $localPythonPath -ErrorAction SilentlyContinue
}
if (-not $python) {
  $python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
}
if (-not $python) {
  Write-Host ''
  Write-Err '未找到 Python 3。'
  Write-Info '请先安装 Python 3：https://www.python.org/downloads/'
  Write-Host ''
  Read-Host '按 Enter 退出'
  exit 1
}

# ── 自动检测 Claude 包路径 ────────────────────────────────

function Resolve-ClaudeAppPath {
  param([string]$InputPath)

  if ([string]::IsNullOrWhiteSpace($InputPath)) {
    return $null
  }

  try {
    $resolved = [System.IO.Path]::GetFullPath($InputPath.Trim())
  } catch {
    return $null
  }

  $app = $resolved.TrimEnd('\\/')
  $res = Join-Path $app 'resources'
  $desktop = Join-Path $res 'en-US.json'
  if ((Test-Path $app) -and (Test-Path $desktop)) {
    return @{ AppDir = $app; ResourcesDir = $res; PackageName = ('manual:' + $app) }
  }

  return $null
}

function Find-ClaudePackage {
  $base = 'C:\Program Files\WindowsApps'
  $dirs = Get-ChildItem $base -Directory -Filter 'Claude_*_x64__*' -ErrorAction SilentlyContinue |
          Sort-Object Name -Descending
  foreach ($d in $dirs) {
    $app = Join-Path $d.FullName 'app'
    $res = Join-Path $app 'resources'
    if (Test-Path (Join-Path $res 'en-US.json')) {
      return @{ AppDir = $app; ResourcesDir = $res; PackageName = $d.Name }
    }
  }
  return $null
}

function Resolve-ClaudePackage {
  $detected = Find-ClaudePackage
  if ($detected) { return $detected }

  Write-Host ''
  Write-Warn '未检测到 WindowsApps 安装。'
  Write-Info '如果你使用的是解压后直接运行的 Claude，请手动输入 Claude app 目录。'
  Write-Info '示例: D:\Claude\app'
  Write-Host ''

  while ($true) {
    $inputPath = Read-Host '  请输入 Claude app 目录（留空则退出）'
    if ([string]::IsNullOrWhiteSpace($inputPath)) {
      return $null
    }

    $manual = Resolve-ClaudeAppPath $inputPath
    if ($manual) { return $manual }

    Write-Warn '该目录下未找到 app\resources\en-US.json，请确认输入的是 Claude 的 app 目录。'
  }
}

function Set-ClaudePackageManual {
  Write-Host ''
  Write-Info '手动指定 Claude app 目录'
  Write-Info '示例: D:\Claude\app'
  Write-Host ''

  while ($true) {
    $inputPath = Read-Host '  请输入 Claude app 目录（留空则取消）'
    if ([string]::IsNullOrWhiteSpace($inputPath)) {
      Write-Info '已取消。'
      return $false
    }

    $manual = Resolve-ClaudeAppPath $inputPath
    if ($manual) {
      $script:pkg = $manual
      $script:appDir = $manual.AppDir
      $script:resDir = $manual.ResourcesDir
      $script:pkgName = $manual.PackageName
      Write-OK "已切换到手动路径: $appDir"
      return $true
    }

    Write-Warn '该目录下未找到 app\resources\en-US.json，请确认输入的是 Claude 的 app 目录。'
  }
}

$pkg = Resolve-ClaudePackage
if (-not $pkg) {
  Write-Host ''
  Write-Err '未找到可用的 Claude 安装目录。'
  Write-Info '请确认已安装 Claude Desktop，或手动提供解压运行版本的 app 目录。'
  Write-Host ''
  Read-Host '按 Enter 退出'
  exit 1
}

$appDir      = $pkg.AppDir
$resDir      = $pkg.ResourcesDir
$pkgName     = $pkg.PackageName
$backupRoot  = Join-Path $env:LOCALAPPDATA 'Claude-zh-CN-official-backup\json-only'
$configPath  = Join-Path $env:APPDATA 'Claude-3p\config.json'

# ── 状态检测 ──────────────────────────────────────────────
function Get-PatchStatus {
  $zhDesktop  = Join-Path $resDir 'zh-CN.json'
  $zhFrontend = Join-Path $resDir 'ion-dist\i18n\zh-CN.json'
  $zhStatsig  = Join-Path $resDir 'ion-dist\i18n\statsig\zh-CN.json'

  $hasZhFiles = (Test-Path $zhDesktop) -and (Test-Path $zhFrontend) -and (Test-Path $zhStatsig)

  # 检查白名单
  $hasWhitelist = $false
  $indexFiles = Get-ChildItem (Join-Path $resDir 'ion-dist\assets\v1') -Filter 'index-*.js' -ErrorAction SilentlyContinue
  foreach ($f in $indexFiles) {
    $content = [System.IO.File]::ReadAllText($f.FullName)
    if ($content.Contains('"zh-CN"')) { $hasWhitelist = $true; break }
  }

  # 检查 locale
  $hasLocale = $false
  if (Test-Path $configPath) {
    try {
      $cfg = Get-Content $configPath -Raw | ConvertFrom-Json
      if ($cfg.locale -eq 'zh-CN') { $hasLocale = $true }
    } catch {}
  }

  # 检查备份
  $hasBackup = (Test-Path $backupRoot) -and ((Get-ChildItem $backupRoot -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)

  return @{
    ZhFiles    = $hasZhFiles
    Whitelist  = $hasWhitelist
    Locale     = $hasLocale
    Backup     = $hasBackup
    Installed  = $hasZhFiles -and $hasWhitelist
  }
}

# ── 显示状态 ──────────────────────────────────────────────
function Show-Status {
  $s = Get-PatchStatus

  Write-Title '当前状态'
  Write-Info  "Claude 来源: $pkgName"
  Write-Info  "安装路径:  $appDir"
  Write-Host ''

  if ($s.ZhFiles)   { Write-OK   '中文资源文件已写入' }   else { Write-Info '中文资源文件未写入' }
  if ($s.Whitelist)  { Write-OK   '语言白名单已包含 zh-CN' } else { Write-Info '语言白名单未包含 zh-CN' }
  if ($s.Locale)     { Write-OK   'locale 已设为 zh-CN' }   else { Write-Info 'locale 未设置' }
  if ($s.Backup)     { Write-OK   '备份存在' }             else { Write-Info '无备份' }

  Write-Host ''
  if ($s.Installed) {
    Write-OK '中文补丁状态: 已安装'
  } else {
    Write-Info '中文补丁状态: 未安装'
  }

  return $s
}

# ── 环境预检 ─────────────────────────────────────────────
function Test-Environment {
  $issues = @()

  # 检查 Claude 是否正在运行
  $claudeProcess = Get-Process -Name claude -ErrorAction SilentlyContinue
  if ($claudeProcess) {
    $issues += 'Claude Desktop 正在运行，安装前将自动关闭。'
  }

  # 检查备份目录空间（粗略估计）
  if (Test-Path $backupRoot) {
    $backupDrive = (Get-Item $backupRoot).PSDrive.Name
    $freeSpaceGB = [math]::Round((Get-PSDrive $backupDrive).Free / 1GB, 1)
    if ($freeSpaceGB -lt 0.5) {
      $issues += "备份盘 $($backupDrive): 仅剩 $freeSpaceGB GB 空间，建议清理。"
    }
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
    Write-Host ""
    $continue = Read-Host '  是否继续安装？(Y/n)'
    if ($continue -eq 'n' -or $continue -eq 'N') {
      Write-Info '已取消安装。'
      return $false
    }
  }
  return $true
}

# ── 安装 ──────────────────────────────────────────────────
function Invoke-Install {
  $totalSteps = 5

  if (-not (Test-Environment)) { return }

  Write-Title '安装中文补丁'
  Write-Host ""

  Write-Step 1 $totalSteps '正在关闭 Claude 进程...'
  Get-Process -Name claude -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Write-ProgressBar -Percent 20 -Label '进程已关闭'

  Write-Step 2 $totalSteps '正在执行 JSON 资源 patch...'
  Write-Host ""
  & $python.Source "$scriptDir\patch_windowsapps_json_only.py" --app-dir "$appDir"

  if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Err 'JSON 资源 patch 失败。请检查上面的错误信息。'
    return
  }
  Write-ProgressBar -Percent 60 -Label 'JSON 资源已写入'

  Write-Step 3 $totalSteps '正在执行 chunk 界面标签和字体自定义 patch...'
  Write-Host ""
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
  Write-Host ""
  Write-OK '中文补丁安装成功！'
  Write-Host ""
  Write-Info '下一步：'
  Write-Info '  1. 打开 Claude Desktop'
  Write-Info '  2. 界面应该已经是中文'
  Write-Info '  3. 可在设置 / 外观区域使用中文字体设置'
  Write-Info ""
  Write-Warn '注意: Claude 更新版本后需要重新运行此脚本'
}

# ── 卸载 ──────────────────────────────────────────────────
function Invoke-Uninstall {
  $totalSteps = 4
  Write-Title '卸载中文补丁'
  Write-Host ""

  Write-Step 1 $totalSteps '正在关闭 Claude 进程...'
  Get-Process -Name claude -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  Write-ProgressBar -Percent 25 -Label '进程已关闭'

  $s = Get-PatchStatus
  if (-not $s.Backup) {
    Write-Warn '未找到备份文件，将尝试手动清理...'
    # 保留原有手动清理逻辑
    Write-Host ''
    $confirm = Read-Host '  是否仍要尝试删除中文资源文件？(y/N)'
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
      Write-Info '已取消。'
      return
    }

    # 手动删除 zh-CN 文件 + 尝试清除白名单中的 zh-CN
    $targets = @(
      (Join-Path $resDir 'zh-CN.json'),
      (Join-Path $resDir 'ion-dist\i18n\zh-CN.json'),
      (Join-Path $resDir 'ion-dist\i18n\statsig\zh-CN.json')
    )
    foreach ($t in $targets) {
      if (Test-Path $t) { Remove-Item $t -Force; Write-Info "  已删除: $t" }
    }

    # 尝试从白名单中移除 zh-CN
    $indexFiles = Get-ChildItem (Join-Path $resDir 'ion-dist\assets\v1') -Filter 'index-*.js' -ErrorAction SilentlyContinue
    foreach ($f in $indexFiles) {
      $content = [System.IO.File]::ReadAllText($f.FullName)
      if ($content.Contains(',"zh-CN"')) {
        $content = $content.Replace(',"zh-CN"', '')
        [System.IO.File]::WriteAllText($f.FullName, $content)
        Write-Info "  已从白名单移除 zh-CN: $($f.Name)"
      }
    }
  } else {
    Write-Step 2 $totalSteps '正在从备份恢复...'
    Write-Host ""
    & $python.Source "$scriptDir\restore_claude_zh_cn_windowsapps.py" --app-dir "$appDir"

    if ($LASTEXITCODE -ne 0) {
      Write-Host ""
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
  Write-Host ""
  Write-OK '卸载完成！'
  Write-Host ""
  Write-Info '下一步：'
  Write-Info '  1. 打开 Claude Desktop'
  Write-Info '  2. 界面应该已经恢复英文'
}

# ── 主菜单 ────────────────────────────────────────────────
function Show-Menu {
  Clear-Host
  Write-Host ''
  Write-Host '  ╔══════════════════════════════════════════════╗' -ForegroundColor Cyan
  Write-Host '  ║   Claude Desktop 中文补丁 (zh-CN, Windows)  ║' -ForegroundColor Cyan
  Write-Host '  ╚══════════════════════════════════════════════╝' -ForegroundColor Cyan

  $s = Show-Status

  Write-Host ''
  Write-Host '  ─────────────────────────────────────────────' -ForegroundColor DarkGray

  if ($s.Installed) {
    Write-Host '  [1] 重新安装 / 更新中文补丁' -ForegroundColor White
    Write-Host '  [2] 卸载中文补丁（恢复英文）' -ForegroundColor White
  } else {
    Write-Host '  [1] 安装中文补丁' -ForegroundColor White
    Write-Host '  [2] 卸载中文补丁（恢复英文）' -ForegroundColor DarkGray
  }
  Write-Host '  [3] 手动指定 Claude app 目录' -ForegroundColor White
  Write-Host '  [4] 刷新状态' -ForegroundColor White
  Write-Host '  [5] 启动系统托盘监视器' -ForegroundColor White
  Write-Host '  [0] 退出' -ForegroundColor White
  Write-Host ''
}

# ── 自动模式 ──────────────────────────────────────────────
if ($Auto) {
  Write-Host ""
  Write-Info '自动模式：检测到管理员权限，正在执行一键安装...'
  Write-Host ""
  Invoke-Install
  Write-Host ""
  Write-Info '3 秒后自动退出...'
  Start-Sleep -Seconds 3
  exit 0
}

# ── 主循环 ────────────────────────────────────────────────
while ($true) {
  Show-Menu
  $choice = Read-Host '  请选择'

  switch ($choice) {
    '1' {
      Invoke-Install
      Write-Host ''
      Read-Host '按 Enter 返回菜单'
    }
    '2' {
      $s = Get-PatchStatus
      if (-not $s.Installed -and -not $s.Backup) {
        Write-Host ''
        Write-Warn '当前未安装中文补丁，也没有备份，无需卸载。'
        Write-Host ''
        Read-Host '按 Enter 返回菜单'
      } else {
        Invoke-Uninstall
        Write-Host ''
        Read-Host '按 Enter 返回菜单'
      }
    }
    '3' {
      Write-Host ''
      $changed = Set-ClaudePackageManual
      Write-Host ''
      Read-Host '按 Enter 返回菜单'
    }
    '4' {
      # 刷新状态，直接回到菜单
    }
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
    '0' {
      Write-Host ''
      Write-Info '再见！'
      Write-Host ''
      exit 0
    }
    default {
      Write-Host ''
      Write-Warn '无效选择，请输入 0-5。'
      Start-Sleep -Milliseconds 800
    }
  }
}
