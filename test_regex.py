#!/usr/bin/env python3
import re

# Test patterns
patterns = {
    "product_names": re.compile(r'^Claude (Ship|Slack|Cowork|Free|Platform|Artifacts|Code|Max|Pro|Team|Enterprise)$'),
    "research_labs": re.compile(r'^Research Labs( Premium)?(：.+)?$'),
    "short_abbrev": re.compile(r'^[A-Z]{2,8}$'),
    "ctrl_shortcut": re.compile(r'^Ctrl\+.*$'),
}

# Test cases
test_cases = {
    "product_names": [
        ("Claude Ship", True),
        ("Claude Slack", True),
        ("Claude Cowork", True),
        ("Claude Free", True),
        ("Claude Platform", True),
        ("Claude Artifacts", True),
        ("Claude Code", True),
        ("Claude Max", True),
        ("Claude Pro", True),
        ("Claude Team", True),
        ("Claude Enterprise", True),
        ("Claude  Code", False),  # extra space
        ("ClaudeShip", False),  # no space
        ("Claude Unknown", False),
    ],
    "research_labs": [
        ("Research Labs", True),
        ("Research Labs Premium", True),
        ("Research Labs：测试", True),  # Chinese colon
        ("Research Labs: test", False),  # English colon
        ("Research Labs测试", False),  # no space
        ("Other Labs", False),
    ],
    "short_abbrev": [
        ("OK", True),
        ("API", True),
        ("HTTP", True),
        ("A", False),  # too short
        ("ABCDEFGHI", False),  # too long (9 chars)
        ("123", False),  # not uppercase letters
        ("OKOK", True),  # 4 chars
    ],
    "ctrl_shortcut": [
        ("Ctrl+Z", True),
        ("Ctrl+Shift+S", True),
        ("Ctrl+Alt+Delete", True),
        ("Ctrl + Z", False),  # extra space
        ("CTRL+Z", False),  # uppercase CTRL
        ("Cmd+Z", False),  # wrong modifier
    ],
}

# Run tests
print("=== Testing Regex Patterns ===")
for pattern_name, tests in test_cases.items():
    print(f"\n# {pattern_name}")
    pattern = patterns[pattern_name]
    for test_str, expected in tests:
        result = pattern.search(test_str)
        status = "PASS" if (result is not None) == expected else "FAIL"
        print(f"  {status}: '{test_str}' -> {'matched' if result else 'not matched'} (expected: {'matched' if expected else 'not matched'})")

# Test actual translation examples
print("\n=== Testing Actual Translation Examples ===")
example_translations = [
    "遴选提交",
    "Research Labs",
    "Research Labs Premium",
    "Research Labs：高级版",
    "Ctrl+⏎",
    "OK",
    "API",
    "Claude Code",
    "Claude Enterprise",
]

for text in example_translations:
    matched = []
    for name, pattern in patterns.items():
        if pattern.search(text):
            matched.append(name)
    print(f"'{text}' -> matched: {', '.join(matched) if matched else 'none'}")
