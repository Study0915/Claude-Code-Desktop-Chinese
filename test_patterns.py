import re

# 测试我添加的模式
patterns = [
    re.compile(r"^Claude (Ship|Slack|Cowork|Free|Platform|Artifacts|Code|Max|Pro|Team|Enterprise)$"),
    re.compile(r"^Research Labs( Premium)?(：.+)?$"),
    re.compile(r"^(Pro|Standard|Premium|Enterprise Claude|Custom).+"),
    re.compile(r"^Ctrl\+.*$"),
    re.compile(r"^Anthropic Sans$"),
    re.compile(r"^(Azure AI Foundry|Microsoft Foundry)$"),
    re.compile(r"^\{label\}，Beta$"),
    re.compile(r"^[A-Z]{2,8}$"),
]

# 测试值
test_values = [
    "Claude Slack",
    "Claude Cowork",
    "Claude Free",
    "Claude Platform",
    "Claude Artifacts",
    "Claude Ship",
    "Research Labs",
    "Research Labs Premium",
    "Research Labs：{before, number} → {after, number}",
    "Standard：{before, number} → {after, number}",
    "Premium：{before, number} → {after, number}",
    "Enterprise Claude：{before, number} → {after, number}",
    "Ctrl+⏎",
    "Anthropic Sans",
    "Azure AI Foundry",
    "Microsoft Foundry",
    "{label}，Beta",
    "ABC",
    "HTTP",
    "API",
]

# 测试每个值
for value in test_values:
    matched = any(p.search(value) for p in patterns)
    print(f"值: '{value}' → 匹配: {matched}")

# 测试一些不应该匹配的值
print("\n测试不应该匹配的值:")
test_values2 = [
    "Cherry-pick",
    "Hello World",
    "这是中文",
    "Claude Something Else",
    "Research Labs Premium Extra",
]

for value in test_values2:
    matched = any(p.search(value) for p in patterns)
    print(f"值: '{value}' → 匹配: {matched}")
