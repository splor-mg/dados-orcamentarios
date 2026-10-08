# task workflow

Executa o script `src/update_etl_options.py`, que atualiza as opções de datapackage e ano no **Run workflow** do Actions, para o [workflow](../../workflow.md) `etl.yaml`:

- Os **datapackages** são as pastas de `datapackages/` que têm um `raw_datapackage.yaml`.

- Os **anos** disponíveis são os últimos 5 mais recentes, para que só seja usado o universo atual do SIAFI.

Assim, se o ano virar ou se um novo `datapackages/*/raw_datapackage.yaml` for adicionado, as opções do workflow acompanham.

O workflow faz o commit dessa alteração ao final da execução.
