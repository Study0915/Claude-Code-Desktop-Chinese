import json
import re
from pathlib import Path

ROOT = Path(r"D:\Claude-Code-zh\Claude-Code-Desktop-Chinese")
RESOURCES = ROOT / "resources"

# 加载配置
ASCII_WORD_RE = re.compile(r"[A-Za-z]{3,}")
CJK_RE = re.compile(r"[一-鿿]")

# 加载现有模式
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
    # Social media platforms
    re.compile(r"^(Instagram|Reddit|LinkedIn|TikTok|YouTube|X / Twitter)$"),
    # Cloud/enterprise services
    re.compile(r"^(Google Play|Google Docs|Google Drive|Google Cloud|Google Calendar|Google logo|Google)$"),
    re.compile(r"^(Azure AI Foundry|Microsoft Foundry|Anthropic Sans)$"),
    # Product names
    re.compile(r"^(Claude Slack|Claude Cowork|Claude Free|Claude Platform|Claude Artifacts|Claude Ship|Claude .+)$"),
    re.compile(r"^(Research Labs|Research Labs Premium)$"),
    # Plan names with placeholders
    re.compile(r"^(Pro|Standard|Premium|Enterprise Claude|Custom).+"),
    # Version/size/count format strings
    re.compile(r"^\{.*\}%$"),
    re.compile(r"^\{.*\} (KB|MB|GB)$"),
    # Names with email placeholders
    re.compile(r"^\{name\}.*\{email\}$"),
    re.compile(r"^\{fullName\}.*\{email\}$"),
    # Other format strings with parentheses
    re.compile(r"^（.*\{.*\}.*）$"),
    re.compile(r"^\（.*\）$"),
    # Short labels with symbols
    re.compile(r"^[A-Z][a-z]+ [A-Z][a-z]+$"),
    # HTTP status
    re.compile(r"^HTTP \{status\}$"),
    # Domain-like patterns
    re.compile(r"^\.claude\.app$"),
    re.compile(r"^your-site$"),
    # API key labels
    re.compile(r"^API_KEY$"),
    # ACS URL
    re.compile(r"^ACS URL$"),
    # Mathematical/number formats
    re.compile(r"^.{1}?\{amount\}$"),
    re.compile(r"^\+\{count\}$"),
    re.compile(r"^-\{count\}$"),
    re.compile(r"^\+\{formattedCurrencyAmount\}$"),
    # Progress/percentage
    re.compile(r"^\{progress\}%$"),
    re.compile(r"^\{pct\}%$"),
    # Scale labels
    re.compile(r"^.+ = \{firstLabel\}"),
    # JCT suffix
    re.compile(r"^\+ JCT$"),
    # Feature name placeholder
    re.compile(r"^Claude \{featureName\}$"),
    # Learn safely
    re.compile(r"^\{learnSafely\}"),
    # Label with beta
    re.compile(r"^\{label\}，Beta$"),
    # Local indicator
    re.compile(r"^（\{local\}）$"),
    # 我添加的新模式
    re.compile(r"^Claude (Ship|Slack|Cowork|Free|Platform|Artifacts|Code|Max|Pro|Team|Enterprise)$"),
    re.compile(r"^Research Labs( Premium)?(：.+)?$"),
    re.compile(r"^(Pro|Standard|Premium|Enterprise Claude|Custom).+"),
    re.compile(r"^Ctrl\+.*$"),
    re.compile(r"^Anthropic Sans$"),
    re.compile(r"^(Azure AI Foundry|Microsoft Foundry)$"),
    re.compile(r"^\{label\}，Beta$"),
    re.compile(r"^[A-Z]{2,8}$"),
]

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

# 加载 frontend-zh-CN.json 文件
frontend_file = RESOURCES / "frontend-zh-CN.json"
with open(frontend_file, 'r', encoding='utf-8') as f:
    frontend_data = json.load(f)

# 检查特定的 key
keys_to_check = [
    "22V/ZP0M0I",  # Claude Slack
    "biSH+InEuL",  # Research Labs
    "AkXGCFumOh",  # Claude Cowork
    "HALZF/VbRH",  # Claude Free
    "HY8scSxkUZ",  # Claude Slack
    "VGolWy/Z96",  # Claude Platform
    "LPT6OcwxnK",  # Azure AI Foundry
    "dyvIkP3vGQ",  # Microsoft Foundry
    "5RasbgfW2t",  # Research Labs：{before, number} → {after, number}
    "u6WcCZIyyg",  # Research Labs Premium：{before, number} → {after, number}
    "TvOAFWIHcJ",  # Standard：{before, number} → {after, number}
    "FPiM1VWudZ",  # Premium：{before, number} → {after, number}
    "hiC8I+PyBe",  # Enterprise Claude：{before, number} → {after, number}
    "7uxoiAwd82",  # {label}，Beta
    "l6aMQuX1m4",  # Claude Artifacts
    "iyK4JPDq1b",  # Claude Ship
]

print("测试特定 key 的值:")
for key in keys_to_check:
    if key in frontend_data:
        value = frontend_data[key]
        result = classify_value(value)
        print(f"{key}: '{value}' → {result}")
        print(f"  is_known_ok: {is_known_ok(value)}")
    else:
        print(f"{key}: 未找到")

# 统计总疑似未翻译条目
issues = []
for key, value in frontend_data.items():
    kind = classify_value(value)
    if kind:
        issues.append((key, value))

print(f"\n总疑似未翻译条目数: {len(issues)}")

# 显示一些示例
print("\n前10个疑似未翻译条目:")
for key, value in issues[:10]:
    print(f"- {key}: '{value}'")
