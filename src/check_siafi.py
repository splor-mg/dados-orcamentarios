import argparse
import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import requests

PACKAGE_DIR = Path('datapackages/dados_check_siafi')
DATA_DIR = PACKAGE_DIR / 'data'
SNAPSHOT_DIR = PACKAGE_DIR / 'data_snapshot'
RAW_URL = "https://raw.githubusercontent.com/splor-mg/dados-check-siafi/main/data/{resource}.csv"


def save_snapshot():
    SNAPSHOT_DIR.mkdir(exist_ok=True)

    for schema_path in sorted((PACKAGE_DIR / 'schemas').glob('*.yaml')):
        resource = schema_path.stem
        response = requests.get(RAW_URL.format(resource=resource), timeout=60)
        if response.status_code == 200:
            (SNAPSHOT_DIR / f'{resource}.csv').write_bytes(response.content)


def divergent_years(old, new):
    columns = new.columns.intersection(old.columns).drop("ano")
    old_sums = old.groupby("ano")[columns].sum()
    new_sums = new.groupby("ano")[columns].sum()
    common_years = old_sums.index.intersection(new_sums.index)
    combined = (new_sums.loc[common_years] - old_sums.loc[common_years]).abs()
    return combined[(combined > 0.01).any(axis=1)].index.tolist()


def main():
    current_year = date.today().year
    years = set()

    for csv_path in sorted(DATA_DIR.glob("*.csv")):
        snapshot_path = SNAPSHOT_DIR / csv_path.name

        if not snapshot_path.exists():
            continue

        new = pd.read_csv(csv_path)
        old = pd.read_csv(snapshot_path)
        years.update(divergent_years(old, new))

    years.discard(current_year)

    if years:
        print(f"Anos divergentes: {', '.join(str(year) for year in sorted(years))}", file=sys.stderr)
    else:
        print("Nenhum ano divergente.", file=sys.stderr)

    print(" ".join(str(year) for year in sorted(years)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finds divergent years.')
    parser.add_argument('--save-snapshot', action='store_true',
                        help='Downloads the published data before the ETL.')
    args = parser.parse_args()

    if os.environ.get('ETL_PACKAGE', '') not in {'', 'dados_check_siafi'}:
        sys.exit()

    try:
        if args.save_snapshot:
            save_snapshot()
        else:
            main()
    except Exception as error:
        print(f"Erro ignorado no check_siafi: {error!r}", file=sys.stderr)
