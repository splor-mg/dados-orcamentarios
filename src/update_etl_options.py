import re
from pathlib import Path

packages = sorted(
    path.parent.name
    for path in Path('datapackages').glob('*/raw_datapackage.yaml')
)

workflow = Path('.github/workflows/etl.yaml')
options = ''.join(f'          - {name}\n' for name in ['todos', *packages])

text = re.sub(
    r'(        options:\n)(?:          - .*\n)+',
    lambda match: match.group(1) + options,
    workflow.read_text(encoding='utf-8'),
)
workflow.write_text(text, encoding='utf-8')
