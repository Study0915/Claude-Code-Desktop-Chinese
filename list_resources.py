#!/usr/bin/env python3
import os
from pathlib import Path

root = Path("D:\\Claude-Code-zh\\Claude-Code-Desktop-Chinese")
resources_dir = root / "resources"

if resources_dir.exists() and resources_dir.is_dir():
    print(f"Files in {resources_dir}:")
    for f in resources_dir.iterdir():
        print(f"  {f.name}")
else:
    print(f"Resources directory not found at: {resources_dir}")
