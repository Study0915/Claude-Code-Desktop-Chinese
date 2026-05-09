#!/usr/bin/env python3
"""Test the fixed validate_resources.py script"""
import json
from pathlib import Path
import sys

# Add the tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from validate_resources import check_glossary_consistency, load_glossary

# Test data
test_glossary = {
    "Pull Request": {
        "zh": "拉取请求",
        "note": "Git 工作流术语"
    },
    "Claude Code": {
        "zh": "Claude Code",
        "note": "产品名，保留英文"
    },
    "Commit": {
        "zh": "提交",
        "note": "Git 提交操作"
    }
}

test_data = {
    "pr.title": "Create a new Pull Request",
    "pr.description": "This is a test Pull Request",
    "claude.code.intro": "Welcome to Claude Code",
    "commit.message": "Update documentation",
    "wrong.commit": "Update documentation with commit",  # Should not match - missing expected translation
    "placeholder.test": "{count} Commits",  # Should be skipped
    "short.test": "Co",  # Should be skipped (length < 3)
}

print("Testing check_glossary_consistency...")
issues = check_glossary_consistency(test_data, test_glossary, "test")

print(f"\nFound issues: {len(issues)}")
for issue in issues:
    print(f"- {issue}")

# Expected issues:
# - [test] Glossary mismatch: key=wrong.commit, term='Commit' found but expected '提交' not in value
# - [test] Glossary mismatch: key=wrong.commit, term='Pull Request' found but expected '拉取请求' not in value

print("\nTest completed!")