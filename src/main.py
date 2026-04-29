from frictionless import Package, Schema
from pathlib import Path

common_schema = Schema('datapackages/common.yaml')
names = [field.name for field in common_schema.fields]

datapackages = Path('datapackages').glob('*/datapackage.yaml')

for datapackage in datapackages:
    package = Package(datapackage)
    for resource in package.resources:
        schema = resource.schema.fields
        for index, field in enumerate(schema):
            if field.custom['target'] in names:
                common_field = [
                    common_field for common_field in common_schema.fields
                    if common_field.name == field.custom['target']][0]
                schema[index] = common_field

        resource.custom.pop('dpetl_extract', None)

    package.to_json(datapackage.parent / 'datapackage.json')
