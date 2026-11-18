import argparse
import os
import re
from frictionless import Package, Schema
from datetime import date
from pathlib import Path

today = date.today()
year_input = os.environ.get('YEAR')
year = int(year_input) if year_input else today.year

# Packages whose fields don't keep the join from fields.yaml
REMOVE_JOIN = ('dados_aux_contratos', 'dados_classificadores', 'dados_ppo', 'dados_siad')


def replace_placeholders(text, previous):
    """Replace {{date}}, {{yearN}} and {{current}} in a text."""
    text = text.replace('{{date}}', today.strftime('%Y-%m-%d'))
    text = re.sub(r'\{\{year(\d+)\}\}', lambda m: str(year + int(m.group(1))), text)
    return text.replace('{{current}}', 'previous' if previous else 'current')


def apply_fields(package, fields, match_by, previous, remove_join):
    """Replace the package fields with the ones in fields.yaml."""
    missing = []

    for resource in package.resources:
        schema = resource.schema.fields

        if previous:
            schema[:] = [field for field in schema if field.custom.get('previous', True)]

        for index, field in enumerate(schema):
            custom = dict(field.custom)

            if match_by == 'target':
                name = custom.get('target', field.name)
            else:
                name = field.name

            if name not in fields:
                if name not in missing:
                    missing.append(name)
                continue

            schema[index] = fields[name].to_copy(name=field.name)
            schema[index].custom.update(custom)

            if 'join' in custom:
                schema[index].custom['join'] = {**fields[name].custom.get('join', {}), **custom['join']}

            if match_by == 'name':
                for prop in ('anonymize', 'join', 'replace', 'compute'):
                    schema[index].custom.pop(prop, None)

        for field in schema:
            field.custom.pop('previous', None)
            if remove_join:
                field.custom.pop('join', None)

    return missing


def build_descriptors(source, output_name, match_by, fields):
    """Build datapackages/*/<output_name> from datapackages/*/<source>."""
    for descriptor in Path('datapackages').glob(f'*/{source}'):
        previous = year <= today.year - 5 and descriptor.parent.name == 'dados_siafi'
        remove_join = descriptor.parent.name in REMOVE_JOIN
        package = Package(descriptor)

        missing = apply_fields(package, fields, match_by, previous, remove_join)
        if missing:
            print(f'[WARNING] {descriptor}: {len(missing)} field name(s) '
                  f'not found in fields.yaml: {", ".join(missing)}')

        output = descriptor.parent / output_name
        if output.suffix == '.yaml':
            package.to_yaml(output)
        else:
            package.to_json(output)

        text = output.read_text(encoding='utf-8')
        output.write_text(replace_placeholders(text, previous), encoding='utf-8')


def pre_extract(fields):
    build_descriptors('raw_datapackage.yaml', 'datapackage.yaml', 'target', fields)


def pre_load(fields):
    build_descriptors('datapackage.json', 'datapackage.json', 'name', fields)


def main():
    parser = argparse.ArgumentParser(description='Prepare the datapackages before extract or load.')
    parser.add_argument('step', choices=['extract', 'load'])
    args = parser.parse_args()

    schema = Schema('datapackages/fields.yaml')
    fields = {field.name: field for field in schema.fields}

    if args.step == 'extract':
        pre_extract(fields)
    else:
        pre_load(fields)


if __name__ == '__main__':
    main()
