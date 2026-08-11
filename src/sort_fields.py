import re


with open('datapackages/fields.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

header, fields_content = content.split('\n', 1)

fields = re.findall(r'(?ms)^  - name:.*?(?=^  - name:|\Z)', fields_content)

fields = [field.rstrip() for field in fields]
fields.sort(key=lambda field: field.split('\n', 1)[0])

output = header + '\n\n' + '\n\n'.join(fields) + '\n'

with open('datapackages/fields.yaml', 'w', encoding='utf-8') as f:
    f.write(output)
