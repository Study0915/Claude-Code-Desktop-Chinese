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
