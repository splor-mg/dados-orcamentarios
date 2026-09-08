import argparse
import re
from frictionless import Package, Schema
from datetime import date
from pathlib import Path

today = date.today()

MATCH_BY = {'.yaml': 'target',
            '.json': 'name'}


def replace_placeholders(text):
    text = text.replace('{{date}}', today.strftime('%Y-%m-%d'))
    text = re.sub(r'\{\{year(\d+)\}\}', lambda m: str(today.year + int(m.group(1))), text)
    return text


def build(source_name, fields_dic):
    extension = Path(source_name).suffix
    match_by = MATCH_BY[extension]
    output_name = f'datapackage{extension}'

    for datapackage in Path('datapackages').glob(f'*/{source_name}'):
        package = Package(datapackage)
        missing = []

        for resource in package.resources:
            schema = resource.schema.fields

            for index, field in enumerate(schema):
                if match_by == 'target':
                    name = field.custom.get('target')
                else:
                    name = field.name

                if not name:
                    continue

                if name in fields_dic:
                    common_field = fields_dic[name]
                    schema[index] = common_field.to_copy(name=field.name)

                    if match_by == 'target':
                        schema[index].custom['target'] = name

                elif name not in missing:
                    missing.append(name)

        if missing:
            example = ', '.join(missing[:5])
            if len(missing) > 5:
                example += ', ...'
            print(f'[WARNING] {datapackage}: {len(missing)} field name(s) not found in fields.yaml: {example}')

        output = datapackage.parent / output_name

        if extension == '.yaml':
            package.to_yaml(output)
        elif extension == '.json':
            package.to_json(output)

        text = output.read_text(encoding='utf-8')
        output.write_text(replace_placeholders(text), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Build datapackage.yaml/datapackage.json from a given descriptor.')
    parser.add_argument('source', help='Descriptor file name to read, e.g. raw_datapackage.yaml or datapackage.json.')
    args = parser.parse_args()

    fields_schema = Schema('datapackages/fields.yaml')
    fields_dic = {field.name: field for field in fields_schema.fields}

    build(args.source, fields_dic)


if __name__ == '__main__':
    main()
