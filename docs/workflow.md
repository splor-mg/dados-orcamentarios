# Workflow

O ETL roda no GitHub Actions, pelo workflow `.github/workflows/etl.yaml`.

## Quando roda

- **Agendado**: de segunda a sexta, às 10h UTC (`cron: "0 10 * * 1-5"`).

- **Manual** (`workflow_dispatch`), pelo botão **Run workflow** do [Actions](https://github.com/splor-mg/dados-orcamentarios/actions/workflows/etl.yaml), com duas opções:

    - `package`: qual datapackage executar (ou todos).

    - `year` (opcional): ano de exercício.

As opções desse formulário são mantidas pela [`task workflow`](tasks/pre_extract/workflow.md).

## O que faz

1. Gera o token do **GitHub App**, com acesso aos repositórios `dados-orcamentarios` e `bo-cli`.

2. Faz o checkout, instala Python, Poetry e as dependências.

3. Roda o ETL: **`task etl`**.

    - Se um `package` foi escolhido, define `ETL_DESCRIPTOR="-d datapackages/<package>/datapackage.yaml"`. Caso contrário, processa
    todos.

    - Se um `year` foi escolhido, os placeholders dos descriptors usam esse ano. Caso contrário, usa o ano atual.

4. Faz o commit das opções do workflow atualizadas pela task `workflow` (`chore: update etl package options`), se houver mudança.

5. Se algo falhar, abre um **issue** com a label `bug` e com o link do log da execução (texto em `.github/etl_failure.md`).

## Variáveis e secrets

Configuradas em **Settings → Secrets and variables → Actions** do repositório.

| Nome | Tipo | Usada para |
| --- | --- | --- |
| `BO_USER`, `BO_PASSWORD` | secret | acesso ao BusinessObjects (`bocli`) |
| `BO_AUTH`, `BO_BASE_URL`, `BO_VERIFY_SSL` | variável | conexão com o BusinessObjects (`bocli`) |
| `BOCLI_MAX_REQUESTS_PER_MINUTE`, `BOCLI_REQUEST_DELAY`, `BOCLI_NETWORK_RETRIES` | variável | limite de requisições, intervalo e tentativas do `bocli` |
| `ANONYMIZE_SECRET_KEY` | secret | chave da anonimização `aes_siv` ([Transform](tasks/transform.md#anonimizacao)) |
| `GH_APP_ID`, `GH_APP_PRIVATE_KEY` | secret | GitHub App: token do workflow e autenticação do `dpetl load` |

Para rodar localmente, defina as mesmas variáveis em um arquivo `.env`.

## Documentação

O site é gerado com `task build` e publicado no GitHub Pages pelo workflow `.github/workflows/docs.yaml`, a cada push na `main` ou manualmente.

Se o build falhar, o workflow abre uma issue com o label `bug`.

```bash
task serve   # testa o site localmente
task build   # gera o site em site/
```
