#!/usr/bin/env python3
import os
from pathlib import Path

root = Path(r"D:\Claude-Code-zh\Claude-Code-Desktop-Chinese")
print(f"Checking root directory: {root}")
print(f"Exists: {root.exists()}")
print(f"Is dir: {root.is_dir()}")

# Check resources directory
resources_dir = root / "resources"
print(f"\nChecking resources directory: {resources_dir}")
print(f"Exists: {resources_dir.exists()}")
print(f"Is dir: {resources_dir.is_dir()}")

if resources_dir.exists():
    print(f"\nFiles in resources:")
    for f in resources_dir.iterdir():
        print(f"  {f.name}")

# Check tools directory
tools_dir = root / "tools"
print(f"\nChecking tools directory: {tools_dir}")
print(f"Exists: {tools_dir.exists()}")
print(f"Is dir: {tools_dir.is_dir()}")

if tools_dir.exists():
    print(f"\nFiles in tools:")
    for f in tools_dir.iterdir():
        print(f"  {f.name}")
