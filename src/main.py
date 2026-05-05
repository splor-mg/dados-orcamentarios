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
            target = field.custom['target']

            if target in names:
                common_field = [f for f in common_schema.fields if f.name == target][0]

                schema[index] = common_field.to_copy(name=field.name)
                schema[index].custom['target'] = target

        resource.custom.pop('dpetl_extract', None)

    package.to_yaml(datapackage.parent / 'datapackage.yaml')
