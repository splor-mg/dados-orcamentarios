import re
from datetime import date
from pathlib import Path

packages = sorted(path.parent.name for path in Path('datapackages').glob('*/raw_datapackage.yaml'))
package_options = ''.join(f'          - {name}\n' for name in ['todos', *packages])

current_year = date.today().year
years = range(current_year, current_year - 5, -1)
year_options = ''.join(f'          - "{year}"\n' for year in years)

workflow = Path('.github/workflows/etl.yaml')
text = workflow.read_text(encoding='utf-8')

text = re.sub(
    r'(      package:\n(?:.*\n)*?        options:\n)(?:          - .*\n)+',
    lambda match: match.group(1) + package_options,
    text,
)

text = re.sub(
    r'(      year:\n(?:.*\n)*?        options:\n)(?:          - .*\n)+',
    lambda match: match.group(1) + year_options,
    text,
)

workflow.write_text(text, encoding='utf-8')
