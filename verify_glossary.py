import json
with open('D:/Claude-Code-zh/Claude-Code-Desktop-Chinese/resources/glossary.json', encoding='utf-8') as f:
    data = json.load(f)

print('Total terms:', len(data))

missing_fields = []
for term, info in data.items():
    fields = []
    if 'zh' not in info:
        fields.append('zh')
    if 'note' not in info:
        fields.append('note')
    if 'tags' not in info:
        fields.append('tags')
    if fields:
        missing_fields.append((term, fields))

if missing_fields:
    print('Terms with missing fields:')
    for term, fields in missing_fields:
        print(f'- {term}: missing {fields}')
else:
    print('All terms have required fields')

plugin_entries = [term for term in data.keys() if term.lower() == 'plugin']
print(f'Plugin entries: {len(plugin_entries)}')