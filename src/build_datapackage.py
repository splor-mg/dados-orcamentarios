import argparse
import os
import re
from frictionless import Package, Schema
from datetime import date
from pathlib import Path

today = date.today()
year_input = os.environ.get('YEAR')
year = int(year_input) if year_input else today.year

MATCH_BY = {'.yaml': 'target',
            '.json': 'name'}


def replace_placeholders(text, previous):
    text = text.replace('{{date}}', today.strftime('%Y-%m-%d'))
    text = re.sub(r'\{\{year(\d+)\}\}', lambda m: str(year + int(m.group(1))), text)
    if previous:
        text = text.replace('/current/', '/previous/')
    return text


def build(source_name, fields_dic):
    extension = Path(source_name).suffix
    match_by = MATCH_BY[extension]
    output_name = f'datapackage{extension}'

    for datapackage in Path('datapackages').glob(f'*/{source_name}'):
        previous_siafi = (year <= today.year - 5) and datapackage.parent.name == 'dados_siafi'
        package = Package(datapackage)
        missing = []

        for resource in package.resources:
            schema = resource.schema.fields

            if previous_siafi:
                schema[:] = [field for field in schema if field.custom.get('previous', True)]

            for index, field in enumerate(schema):
                original_custom = dict(field.custom)

                if match_by == 'target':
                    name = field.custom.get('target')
                else:
                    name = field.name

                if not name:
                    continue

                if name in fields_dic:
                    common_field = fields_dic[name]
                    schema[index] = common_field.to_copy(name=field.name)
                    schema[index].custom.update(original_custom)
                elif name not in missing:
                    missing.append(name)

            for field in schema:
                field.custom.pop('previous', None)

        if missing:
            example = ', '.join(missing[:5])
            if len(missing) > 5:
                example += ', ...'
            print(f'[WARNING] {datapackage}: {len(missing)} field name(s) not found in fields.yaml: {example}')

        output = datapackage.parent / output_name

        if extension == '.yaml':
            package.to_yaml(output)
            text = output.read_text(encoding='utf-8')
            output.write_text(replace_placeholders(text, previous_siafi), encoding='utf-8')
        elif extension == '.json':
            package.to_json(output)


def main():
    parser = argparse.ArgumentParser(description='Build datapackage.yaml/datapackage.json from a given descriptor.')
    parser.add_argument('source', help='Descriptor file name to read, e.g. raw_datapackage.yaml or datapackage.json.')
    args = parser.parse_args()

    fields_schema = Schema('datapackages/fields.yaml')
    fields_dic = {field.name: field for field in fields_schema.fields}

    build(args.source, fields_dic)


if __name__ == '__main__':
    main()
