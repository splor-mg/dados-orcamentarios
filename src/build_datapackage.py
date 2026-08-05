import yaml
from datetime import datetime
from frictionless import Package, Schema
from pathlib import Path


year = str(datetime.now().year)

datapackages = Path('datapackages').glob('*/raw_datapackage.yaml')
common_schema = Schema('datapackages/common.yaml')
common_fields = {field.name: field for field in common_schema.fields}

for datapackage in datapackages:
    text = datapackage.read_text(encoding='utf-8').replace('{{year}}', year)
    descriptor = yaml.safe_load(text)
    package = Package(descriptor, basepath=str(datapackage.parent))

    for resource in package.resources:
        schema = resource.schema.fields

        for index, field in enumerate(schema):
            target = field.custom.get('target')

            if target and target in common_fields:
                common_field = common_fields[target]
                schema[index] = common_field.to_copy(name=field.name)
                schema[index].custom['target'] = target

    package.to_yaml(datapackage.parent / 'datapackage.yaml')
