# Changelog

## Version Scheme

Format: `{claude_version}.{patch_iteration}`
- `claude_version`: The Claude Desktop version this patch targets (e.g., `1.5354.0`)
- `patch_iteration`: Incremental number for translation updates, bug fixes, etc. within the same Claude version (e.g., `.1`, `.2`)

Example: `1.5354.0.1` = first patch release for Claude Desktop v1.5354.0

## 2026-05-06

### Added

- 翻译扩充：从 Claude Desktop v1.5354.0.0 的 en-US 源文件中翻译了 1,198 个缺失的前端条目。
- 新增翻译涵盖：连接器管理、Cowork 功能、HIPAA 合规、团队管理、计费、代码会话、AI 提示模板等模块。
- `check_i18n_coverage.py` 新增 en-US 对比功能：自动检测缺失键和过时键。
- `check_i18n_coverage.py` 增强未翻译检测：ASCII 阈值从 4 字符降至 3 字符，新增更多品牌名白名单。
- `validate_resources.py` 新增：空值检查、占位符一致性校验（智能区分变量名和复数形式内容）、中文引号检测。

### Fixed

- 修复 `frontend-zh-CN.json` 中中文引号（U+201C/U+201D）被误用作 JSON 分隔符的语法错误。
- 修复 `desktop-zh-CN.json` 中同样的中文引号 JSON 语法错误。
- 翻译质量润色：统一"回忆"→"记忆"、修复生硬翻译（"嘿那里"→"你好"等）、修复格式问题。

### Coverage

- desktop-zh-CN.json: 361/361 keys (100%)
- frontend-zh-CN.json: 13525/13227 keys (100%+, 含 298 个过时键)
- statsig-zh-CN.json: 46/46 keys (100%)

## 2026-04-26

### Changed

- 项目主线收敛为 JSON-only 官方包 patch，不再碰 Configure Third-Party Inference。
- 主线 patch 脚本 `patch_windowsapps_json_only.py` 现在完整执行：
  - 备份原文件
  - 写入 3 个 zh-CN JSON 资源
  - patch 语言白名单
  - 设置 locale=zh-CN
- `restore_claude_zh_cn_windowsapps.py` 现在同时支持 json-only 和 full-patch 两种备份路径。

### Fixed

- 修复 6 个翻译质量问题（管道符断裂、URL 拼写错误、术语不准确等）。
- 修复根目录 `zh-CN.json` 与 `resources/desktop-zh-CN.json` 的 21 处 macOS/Windows 措辞不一致。

### Removed

- 删除 16 个历史实验脚本（导出副本、chunk patch、3P patch 等）。
- 删除 `Claude_zh-CN_Windows/` 导出的二进制副本（928 个文件）。
- 删除 5 个多余文档。
- 删除根目录重复的 `zh-CN.json` 和 macOS 参考文件 `Localizable.strings`。

### Coverage

- desktop-zh-CN.json: 355/355 keys (100%)
- frontend-zh-CN.json: 12326/12325 keys (100%)
- statsig-zh-CN.json: 46/46 keys (100%)

## Known Issues

- Windows console output may display Chinese text incorrectly under some code pages even when the actual files are valid UTF-8.
- If upstream Claude changes bundle structure or language whitelist layout, the patch script may need updates.
- After official Claude updates, the patch should usually be reinstalled.
