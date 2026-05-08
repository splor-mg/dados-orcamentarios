import argparse

from datapackage_raw import apply_common_fields
from datapackage import apply_data_transformations
from validate import validate_datapackage


def extract_validate_command():
    apply_common_fields()
    validate_datapackage()


def transform_validate_command():
    apply_data_transformations()
    validate_datapackage()


def main():
    parser = argparse.ArgumentParser(description='Pipeline de dados')
    parser.add_argument('command', choices=['extract_validate', 'transform_validate'],
                        help='`extract_validate` to validate data_raw, `transform_validate` to validate data')

    args = parser.parse_args()

    try:
        if args.command == 'extract_validate':
            extract_validate_command()

        elif args.command == 'transform_validate':
            transform_validate_command()

    except RuntimeError as e:
        print(f'Erro: {e}')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
