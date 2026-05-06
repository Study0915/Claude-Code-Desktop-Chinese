#!/usr/bin/env python3
"""Check i18n coverage: compare zh-CN against en-US source and detect untranslated entries.

Two modes:
  1. en-US comparison: find keys present in en-US but missing from zh-CN
  2. Self-check: scan zh-CN values for ASCII words that suggest untranslated content
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources"

TARGETS = [
    {
        "name": "desktop",
        "zh": RESOURCES / "desktop-zh-CN.json",
        "en_candidates": [
            Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "en-US.json",
        ],
    },
    {
        "name": "frontend",
        "zh": RESOURCES / "frontend-zh-CN.json",
        "en_candidates": [
            Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "ion-dist" / "i18n" / "en-US.json",
        ],
    },
    {
        "name": "statsig",
        "zh": RESOURCES / "statsig-zh-CN.json",
        "en_candidates": [
            Path(r"C:\Program Files\WindowsApps") / "Claude_1.5354.0.0_x64__pzs8sxrjxfjjc" / "app" / "resources" / "ion-dist" / "i18n" / "statsig" / "en-US.json",
        ],
    },
]

ASCII_WORD_RE = re.compile(r"[A-Za-z]{3,}")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


KNOWN_OK_PATTERNS = [
    re.compile(r"^(USB|AWS|API|SDK|JSON|UTF-8|CI|CLI|MCP|SSH|URL|ID|Caps Lock|SSO|OTEL)$"),
    re.compile(r"^\{.*\}$"),
    re.compile(r"^[\d{}%./: +\-_,()\[\]<>|]+$"),
    re.compile(r"^(Anthropic|Bedrock|Vertex|Foundry|Azure AI|Google Vertex AI|AWS Bedrock)$"),
    re.compile(r"^(Claude|Claude\.ai|Claude API|Claude Code|Claude Code CLI|Claude Enterprise|Claude for Excel|Claude Max|Claude Pro|Claude Team)$"),
    re.compile(r"^(Python|Node\.js|Webhook|GitHub|Gmail|JetBrains|Excel|Artifacts|status\.claude\.com)$"),
    re.compile(r"^(Amazon Bedrock|Claude — zsh|website\.com|Cowork|HIPAA|BAA|RFC|PRD|CTR|DCF)$"),
    re.compile(r"^(Windows \(x64\)|Windows \(arm64\)|Linux \(x64\)|Linux（arm64）|macOS)$"),
    re.compile(r"^(Latin-1 \(ISO-8859-1\)|Ctrl⏎|Enter|Esc|Tab|Shift|⌘)$"),
    re.compile(r"^https?://\S+$"),
    re.compile(r"^[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+$"),
    re.compile(r"^PR #\{.*\}$"),
    re.compile(r"^CI \{.*\}$"),
    re.compile(r"^.{1,3}$"),  # Short strings (1-3 chars) are likely abbreviations
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_en_source(candidates: list[Path]) -> Path | None:
    for p in candidates:
        if p.exists():
            return p
    return None


def is_known_ok(value: str) -> bool:
    return any(p.search(value) for p in KNOWN_OK_PATTERNS)


def classify_value(value: str) -> str | None:
    if not isinstance(value, str):
        return None
    if CJK_RE.search(value):
        return None
    if is_known_ok(value):
        return None
    if ASCII_WORD_RE.search(value):
        return "likely_untranslated"
    return None


def main() -> int:
    report_lines: list[str] = []
    total_missing = 0
    total_suspect = 0

    for target in TARGETS:
        name = target["name"]
        zh_path = target["zh"]

        report_lines.append(f"## {name}")

        if not zh_path.exists():
            report_lines.append("MISSING: file not found")
            report_lines.append("")
            continue

        zh_data = load_json(zh_path)
        report_lines.append(f"zh-CN keys: {len(zh_data)}")

        # Mode 1: en-US comparison
        en_path = find_en_source(target["en_candidates"])
        if en_path:
            en_data = load_json(en_path)
            report_lines.append(f"en-US keys: {len(en_data)}")

            missing_keys = sorted(set(en_data) - set(zh_data))
            obsolete_keys = sorted(set(zh_data) - set(en_data))

            if missing_keys:
                report_lines.append(f"### Missing from zh-CN ({len(missing_keys)})")
                for key in missing_keys:
                    val = en_data[key]
                    if isinstance(val, str):
                        report_lines.append(f"- {key}: {val[:100]}")
                    elif isinstance(val, dict):
                        report_lines.append(f"- {key}: (plural form)")
                total_missing += len(missing_keys)
            else:
                report_lines.append("### Missing from zh-CN: 0 (complete!)")

            if obsolete_keys:
                report_lines.append(f"### Obsolete in zh-CN ({len(obsolete_keys)})")
                for key in obsolete_keys[:20]:
                    report_lines.append(f"- {key}")
                if len(obsolete_keys) > 20:
                    report_lines.append(f"  ... and {len(obsolete_keys) - 20} more")
        else:
            report_lines.append("en-US source: not found (skipping comparison)")

        # Mode 2: Self-check for untranslated values
        issues = []
        for key, value in zh_data.items():
            kind = classify_value(value)
            if kind:
                issues.append((key, value))

        if issues:
            report_lines.append(f"### Suspect untranslated ({len(issues)})")
            for key, value in issues:
                report_lines.append(f"- {key}: {value}")
        else:
            report_lines.append("### Suspect untranslated: 0")
        total_suspect += len(issues)

        report_lines.append("")

    report_lines.append("---")
    report_lines.append(f"**Total missing keys: {total_missing}**")
    report_lines.append(f"**Total suspect untranslated: {total_suspect}**")

    report = "\n".join(report_lines)
    out = ROOT / "I18N-COVERAGE-REPORT.md"
    out.write_text(report, encoding="utf-8")

    print(f"Wrote: {out}")
    print(f"Missing keys (en-US not in zh-CN): {total_missing}")
    print(f"Suspect untranslated values: {total_suspect}")

    return 1 if total_missing > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
