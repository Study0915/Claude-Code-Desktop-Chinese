# Claude Desktop 中文语言包

[English](#english) | 中文

为 Windows 版 Claude Desktop 提供简体中文界面翻译。

> **声明**：本项目为非官方社区翻译补丁，与 Anthropic 公司无关。

## 致谢

本项目基于知乎作者 **云樱梦海** 的原创汉化工作改进而来。

- 原文：[Claude Desktop 中文汉化教程](https://zhuanlan.zhihu.com/p/2032922856410043492)
- 作者已授权本项目开源发布

在原作基础上，本项目进行了以下改进：

- 修正了品牌名称、专业术语等翻译错误
- 润色了生硬的机翻痕迹，提升阅读体验
- 补全了缺失的翻译条目，覆盖率接近 100%
- 提供了一键安装/卸载脚本

## 系统要求

- Windows 10 / 11
- 已安装 [Claude Desktop](https://claude.ai/download)

## 安装方法

1. **关闭 Claude Desktop**（确保系统托盘图标也退出）
2. 下载本项目并解压
3. 右键 `claude-zh-cn.bat` → **以管理员身份运行**
4. 按提示选择 `[1] 安装中文补丁`
5. 等待完成后，重新打开 Claude Desktop 即可看到中文界面

## 卸载方法

右键运行 `claude-zh-cn.bat`，选择 `[2] 卸载中文补丁`，即可恢复英文界面。

## 更新补丁

Claude Desktop 自动更新后界面可能恢复英文，此时重新运行安装脚本即可。

## 目录结构

```
├── claude-zh-cn.bat        # 入口脚本（双击运行）
├── resources/              # 翻译资源文件
│   ├── desktop-zh-CN.json  # 桌面端界面翻译
│   ├── frontend-zh-CN.json # 前端界面翻译
│   └── statsig-zh-CN.json  # 功能描述翻译
├── scripts/                # 安装/卸载脚本
├── tools/                  # 维护工具
├── python/                 # 内置 Python 运行环境
└── docs/                   # 许可证与更新日志
```

## 常见问题

**Q: 提示需要管理员权限？**
A: 请右键 → 以管理员身份运行。

**Q: 提示找不到 Python？**
A: 本项目已内置 Python 环境，无需额外安装。

**Q: Claude 更新后界面变回英文？**
A: 这是正常现象，Claude 更新会覆盖补丁文件。关闭 Claude 后重新运行安装脚本即可。

**Q: 开发者工具菜单为什么是英文？**
A: 这些是 Chromium 原生菜单，不在翻译范围内。

## 许可证

本项目采用 [MIT 许可证](docs/LICENSE.md)。

翻译资源文件的原始版权归 Anthropic 公司所有，本项目仅提供翻译内容。

---

## English

An unofficial Chinese (Simplified) language pack for Claude Desktop on Windows.

Based on the original localization work by **Yunying Menghai** ([Zhihu article](https://zhuanlan.zhihu.com/p/2032922856410043492)), with permission from the original author.

### Installation

1. Close Claude Desktop (including system tray)
2. Right-click `claude-zh-cn.bat` → Run as administrator
3. Select `[1]` to install
4. Restart Claude Desktop

### License

[MIT](docs/LICENSE.md)
