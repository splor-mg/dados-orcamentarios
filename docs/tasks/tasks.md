# Tasks

As tasks ficam no `pyproject.toml` via [taskipy](https://github.com/taskipy/taskipy).

Com o ambiente virtual ativado, execute `task list`, para listar todas elas.

## Processo ETL

| Task | Executa | O que faz |
| --- | --- | --- |
| [`workflow`](pre_extract/workflow.md) | `python src/update_etl_options.py` | Atualiza as opções de datapackage e ano do `etl.yaml`. |
| [`yaml`](pre_extract/yaml.md) | `python src/build_datapackage.py raw_datapackage.yaml` | Gera o `datapackage.yaml` a partir do `raw_datapackage.yaml`. |
| [`bocache`](pre_extract/bocache.md) | `bo cache update` | Cria o cache do `bocli` (id e caminho dos objetos do BO). |
| `pre_extract` | `task workflow && task yaml && task bocache` | Roda `workflow`, `yaml` e `bocache`, antes do `extract`. |
| [`extract`](extract.md) | `dpetl $ETL_DESCRIPTOR extract --delay 5` | Baixa os dados brutos (`dpetl extract`). |
| [`transform`](transform.md) | `dpetl $ETL_DESCRIPTOR --no-validate transform` | Escreve os dados processados (`dpetl transform`). |
| [`pre_load`](pre_load.md) | `python src/build_datapackage.py datapackage.json` | Atualiza os campos do `datapackage.json`. |
| [`load`](load.md) | `dpetl --validate-before load` | Publica os dados no repositório do datapackage (`dpetl load`). |
| `etl` | `task extract && task transform && task load` | Roda `extract`, `transform` e `load`. |

> **Nota**: o taskipy executa automaticamente as tasks com prefixo `pre_` antes da task principal.
Logo, `task extract` roda `pre_extract` e `task load` roda `pre_load`.

### Variável `ETL_DESCRIPTOR`

As tasks `extract` e `transform` usam `$ETL_DESCRIPTOR` para definir qual pacote terá o processo ETL executado.

```bash
ETL_DESCRIPTOR="-d datapackages/dados_classificadores/datapackage.yaml" task etl
```

Se estiver vazia, o `dpetl` processa todos os `datapackages/*/datapackage.yaml`.

> **Nota**: `task load` não usa essa variável, pois ele precisa do `datapackage.json`, que é gerado pelo `dpetl transform`.

## Desenvolvimento

| Task | O que faz |
| --- | --- |
| `lint` | Verifica boas práticas em Python (`ruff check`). |
| `format` | Formata o código (`ruff format`). |
| `test` | Roda o lint e os testes. |
