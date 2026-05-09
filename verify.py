import json

try:
    with open('resources/glossary.json', encoding='utf-8') as f:
        data = json.load(f)
    print(f'OK: {len(data)} terms')

    # 验证所有要求的术语都存在
    required_terms = [
        # Git/技术术语
        "Git", "Diff", "Commit", "Branch", "Merge", "Repository", "Review", "Deploy", "Environment", "Integration", "Endpoint",
        # 产品功能词
        "Dashboard", "Billing", "Subscription", "Invoice", "Member", "Permission", "Role", "Group", "Notification", "Template", "Draft", "Archive", "Restore", "Duplicate", "Rename", "Move",
        # 通用UI操作词
        "Copy", "Paste", "Cut", "Select", "Deselect", "Expand", "Collapse", "Filter", "Sort", "Search", "Replace", "Upload", "Download", "Import", "Export", "Share", "Invite", "Leave", "Remove", "Delete", "Cancel", "Confirm", "Submit", "Save", "Edit", "Update", "Refresh", "Reload", "Retry", "Skip", "Back", "Next", "Previous", "Finish", "Close", "Open", "Create", "New", "Add", "Insert", "Append", "Prepend", "Connect", "Disconnect", "Link", "Unlink", "Sync", "Schedule", "Run", "Execute", "Stop", "Pause", "Resume", "Abort", "Enable", "Disable", "Activate", "Deactivate", "Upgrade", "Downgrade", "Renew", "Extend"
    ]

    missing = [term for term in required_terms if term not in data]
    if missing:
        print(f'缺失术语: {missing}')
    else:
        print('所有要求的术语都已存在')

except Exception as e:
    print(f'错误: {e}')