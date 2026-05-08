# 贡献指南

感谢你对 Claude Desktop 中文补丁的关注！

## 翻译贡献

### 如何提交翻译建议

1. **Fork** 本仓库
2. 编辑 `resources/zh-CN/` 下对应的 JSON 文件
3. 提交 Pull Request

### 翻译规范

- 术语请参考 `resources/glossary.json`
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
│   ├── zh-CN/               # 中文翻译
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