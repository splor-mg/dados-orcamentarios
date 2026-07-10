import yaml
import pandas as pd

def extract_fields_by_resource(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    results = {}

    for resource in data.get('resources', []):
        resource_name = resource.get('name', '')
        resource_title = resource.get('title', resource_name)
        resource_ppo = resource.get('ppo', '')

        schema = resource.get('schema', {})
        fields = schema.get('fields', [])

        fields_list = []

        for field in fields:
            fields_list.append({
                'Título': field.get('title', ''),
                'SISOR': field.get('name', ''),
                'AID': field.get('target', ''),
                'PPO': field.get('ppo', '')
            })

        df = pd.DataFrame(fields_list)
        results[resource_name] = {
            'title': resource_title,
            'ppo': resource_ppo,
            'dataframe': df
        }

    return results

def generate_combined_markdown(results, output_file='DE-PARA.md'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# Mapeamento de Campos - Datapackage PPO-MG\n\n')
        f.write('## Índice\n\n')

        for idx, (resource_name, info) in enumerate(results.items(), 1):
            resource_title = info['title']
            df = info['dataframe']
            anchor = resource_name.lower().replace('_', '-')
            f.write(f'{idx}. [{resource_title}](#{anchor}) - {len(df)} campos\n')

        f.write('\n---\n\n')

        for resource_name, info in results.items():
            resource_title = info['title']
            resource_ppo = info['ppo']
            df = info['dataframe']

            anchor = resource_name.lower().replace('_', '-')

            f.write(f'## {resource_title}\n\n')
            f.write(f'**Nome da base SISOR:** `{resource_name}`\n\n')
            if resource_ppo:
                f.write(f'**Nome da base PPO:** `{resource_ppo}`\n\n')
            else:
                f.write(f'**Nome da base PPO:** *Não definido*\n\n')

            if not df.empty:
                headers = ['Título', 'SISOR', 'AID', 'PPO']
                f.write('| ' + ' | '.join(headers) + ' |\n')
                f.write('|' + '|'.join(['---' for _ in headers]) + '|\n')

                for _, row in df.iterrows():
                    titulo = str(row['Título']) if pd.notna(row['Título']) else ''
                    sisor = str(row['SISOR']) if pd.notna(row['SISOR']) else ''
                    aid = str(row['AID']) if pd.notna(row['AID']) else ''
                    ppo = str(row['PPO']) if pd.notna(row['PPO']) and row['PPO'] != '' else ''
                    f.write(f'| {titulo} | {sisor} | {aid} | {ppo} |\n')

            f.write(f'\n*Total de campos: {len(df)}*\n\n')
            f.write('---\n\n')

if __name__ == '__main__':
    yaml_file = 'datapackages/dados_ppo/datapackage.yaml'
    results = extract_fields_by_resource(yaml_file)
    generate_combined_markdown(results)
