import sys
import os

# 切换到正确的目录
os.chdir(r"D:\Claude-Code-zh\Claude-Code-Desktop-Chinese")

# 添加 tools 目录到 Python 路径
sys.path.append(r"D:\Claude-Code-zh\Claude-Code-Desktop-Chinese\tools")

# 运行检查脚本
import subprocess
result = subprocess.run(["python", "tools/check_i18n_coverage.py"], capture_output=True, text=True)

print("标准输出:")
print(result.stdout)
print("\n标准错误:")
print(result.stderr)
