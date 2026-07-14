import re

with open('datapackages/common.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

fields_raw = re.split(r'\n(?=  - name:)', content.strip())

fields_with_names = []
for field in fields_raw:
    name_match = re.search(r'  - name: (.+?)\n', field)
    if name_match:
        fields_with_names.append((name_match.group(1), field))

fields_with_names.sort(key=lambda x: x[0])

header = 'fields:'
body = '\n'.join([field for _, field in fields_with_names])

output = header + '\n' + body + '\n'

with open('datapackages/common.yaml', 'w', encoding='utf-8') as f:
    f.write(output)
