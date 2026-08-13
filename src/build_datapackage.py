import re
from frictionless import Package, Schema
from datetime import date
from pathlib import Path

today = date.today()

def replace_placeholders(text):
    text = text.replace('{{date}}', today.strftime('%Y-%m-%d'))
    text = re.sub(r'\{\{year(\d+)\}\}', lambda m: str(today.year + int(m.group(1))), text)
    return text

datapackages = Path('datapackages').glob('*/raw_datapackage.yaml')
fields_schema = Schema('datapackages/fields.yaml')
fields_dic = {field.name: field for field in fields_schema.fields}

for datapackage in datapackages:
    package = Package(datapackage)

    for resource in package.resources:
        schema = resource.schema.fields

        for index, field in enumerate(schema):
            target = field.custom.get('target')

            if target and target in fields_dic:
                common_field = fields_dic[target]
                schema[index] = common_field.to_copy(name=field.name)
                schema[index].custom['target'] = target

    output = datapackage.parent / 'datapackage.yaml'
    package.to_yaml(output)

    text = output.read_text(encoding='utf-8')
    output.write_text(replace_placeholders(text), encoding='utf-8')
