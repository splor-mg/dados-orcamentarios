import sys
from datetime import date
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path('datapackages/dados_check_siafi/data')
RAW_URL = "https://raw.githubusercontent.com/splor-mg/dados-check-siafi/main/data/{resource}.csv"


def load_previous_version(resource):
    response = requests.get(RAW_URL.format(resource=resource), timeout=60)
    if response.status_code != 200:
        return None
    return pd.read_csv(StringIO(response.text))


def divergent_years(old, new):
    numeric_columns = new.select_dtypes(include="number").columns.drop("ano")
    old_sums = old.groupby("ano")[numeric_columns].sum()
    new_sums = new.groupby("ano")[numeric_columns].sum()
    common_years = old_sums.index.intersection(new_sums.index)
    combined = (new_sums.loc[common_years] - old_sums.loc[common_years]).abs()
    return combined[(combined > 0.01).any(axis=1)].index.tolist()


def main():
    current_year = date.today().year
    years = set()

    for csv_path in sorted(DATA_DIR.glob("*.csv")):
        resource = csv_path.stem
        new = pd.read_csv(csv_path)
        old = load_previous_version(resource)

        if old is None:
            continue

        years.update(divergent_years(old, new))

    years.discard(current_year)

    if years:
        print(f"Anos divergentes: {', '.join(str(year) for year in sorted(years))}", file=sys.stderr)
    else:
        print("Nenhum ano divergente.", file=sys.stderr)

    print(" ".join(str(year) for year in sorted(years)))


if __name__ == "__main__":
    main()
