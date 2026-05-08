from frictionless import Package
from pathlib import Path


def apply_data_transformations():

    datapackages = Path('datapackages').glob('*/datapackage.yaml')

    for datapackage in datapackages:
        package = Package(datapackage)

        for resource in package.resources:
            schema = resource.schema.fields
            resource.path = f'data/{resource.name}.csv.gz'
            resource.scheme = 'file'
            resource.compression = 'gz'

            for index, field in enumerate(schema):
                target = field.custom.get('target')

                if target:
                    schema[index] = field.to_copy(name=target)

            for field in schema:
                field.custom.pop('target', None)

            resource.extrapaths = None

        package.to_yaml(datapackage.parent / 'datapackage.yaml')
