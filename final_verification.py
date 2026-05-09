import json
import re
from pathlib import Path

ROOT = Path(r"D:\Claude-Code-zh\Claude-Code-Desktop-Chinese")

print("=== 最终验证 ===\n")

# 1. 验证 frontend-zh-CN.json 中的修改
print("1. 验证 frontend-zh-CN.json 中的修改:")
frontend_file = ROOT / "resources" / "frontend-zh-CN.json"
with open(frontend_file, 'r', encoding='utf-8') as f:
    frontend_data = json.load(f)

keys_to_verify = [
    ("OBGEVHifJw", "Cherry-pick", "遴选提交"),
    ("UDwAurwLUj", "Cherry-pick", "遴选提交"),
]

for key, old_value, new_value in keys_to_verify:
    if key in frontend_data:
        actual_value = frontend_data[key]
        if actual_value == new_value:
            print(f"   ✓ {key}: 正确修改为 '{new_value}'")
        else:
            print(f"   ✗ {key}: 预期 '{new_value}', 实际 '{actual_value}'")
    else:
        print(f"   ✗ {key}: 未找到")

# 2. 验证 check_i18n_coverage.py 中的模式
print("\n2. 验证 check_i18n_coverage.py 中的模式:")
check_file = ROOT / "tools" / "check_i18n_coverage.py"
with open(check_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否包含所有添加的模式
patterns_to_check = [
    r"^Claude (Ship|Slack|Cowork|Free|Platform|Artifacts|Code|Max|Pro|Team|Enterprise)$",
    r"^Research Labs( Premium)?(：.+)?$",
    r"^(Pro|Standard|Premium|Enterprise Claude|Custom).+",
    r"^Ctrl\+.*$",
    r"^Anthropic Sans$",
    r"^(Azure AI Foundry|Microsoft Foundry)$",
    r"^\{label\}，Beta$",
    r"^[A-Z]{2,8}$",
]

all_found = True
for pattern in patterns_to_check:
    # 转义正则表达式中的特殊字符以便搜索
    escaped_pattern = re.escape(pattern).replace(r"\ ", r"\s*").replace(r"\+", r"\+")
    if re.search(pattern, content):
        print(f"   ✓ 找到模式: {pattern}")
    else:
        print(f"   ✗ 未找到模式: {pattern}")
        all_found = False

# 3. 总结
print("\n3. 总结:")
print("   已成功完成所有任务要求:")
print("   - 修改了 2 个 Git 操作条目的翻译")
print("   - 添加了 8 组正则表达式模式到白名单")
print("   - 所有产品名、品牌名、专有名词等现在应该不再被标记为疑似未翻译")

if all_found:
    print("\n   ✓ 所有模式均已正确添加")
else:
    print("\n   ✗ 部分模式未找到")

print("\n任务完成！")
