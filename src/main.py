from frictionless import Package, Schema

general_schemas = Schema('datapackages/schemas.yaml')
names = [field.name for field in general_schemas.fields]

package = Package("datapackages/dados_siafi/raw_datapackage.yaml")

for resource in package.resources:
    schema = resource.schema.fields
    for index, field in enumerate(schema):
        if field.custom['target'] in names:
            new_field = [new_field for new_field in general_schemas.fields if new_field.name == field.custom['target']][0]
            schema[index] = new_field

package
package.to_json('datapackages/dados_siafi/datapackage.json')


