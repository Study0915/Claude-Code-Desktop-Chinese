#!/usr/bin/env python3
import json
from pathlib import Path

resources_dir = Path("D:/Claude-Code-zh/Claude-Code-Desktop-Chinese/resources")
frontend_path = resources_dir / "frontend-zh-CN.json"

data = json.loads(frontend_path.read_text(encoding="utf-8"))
print(f"Total keys in frontend-zh-CN.json: {len(data)}")