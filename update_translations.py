import json
import os

# 加载 frontend-zh-CN.json 文件
file_path = r"D:\Claude-Code-zh\Claude-Code-Desktop-Chinese\resources\frontend-zh-CN.json"

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修改指定的 key 值
data['OBGEVHifJw'] = '遴选提交'
data['UDwAurwLUj'] = '遴选提交'

# 保存修改后的文件
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Successfully updated frontend-zh-CN.json")
