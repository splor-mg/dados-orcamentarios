<!-- --8<-- [start:site] -->
# Dados Orçamentários

O **dados-orcamentarios** tem como objetivo centralizar o processo de ETL (_Extract_, _Transform_, _Load_) dos pacotes de dados orçamentários da SPLOR-MG.

Para isso, utiliza os padrões espeficiados de [Data Package](https://datapackage.org/), além da ferramenta [frictionless](https://framework.frictionlessdata.io/) e do pacote [DPETL](https://github.com/splor-mg/dpetl).


## Instalação

1. Clone o repositório:

    ```bash
    git clone git@github.com:splor-mg/dados-orcamentarios.git
    cd dados-orcamentarios
    ```

2. Instale as dependências do projeto com Poetry:

    ```bash
    poetry install
    ```

3. Execute manualmente todo o processo de ETL:

    ```bash
    task etl
    ```


## Como funciona

O **dados-orcamentarios** gerencia os metadados dos pacotes de dados da SPLOR-MG na pasta `datapackages/`. Os dados processados não ficam aqui, e sim no repositório de cada pacote.

Cada pacote tem a sua própria pasta, com:

  - `raw_datapackage.yaml`: a lista de todos os seus recursos.

  - `schemas/`: a lista de todos os campos, para cada recurso.

Há ainda o arquivo `datapackages/fields.yaml`, que adiciona descrição e restrições a esses campos e é compartilhado por todos os pacotes.

Dentro dos descritores, há parâmetros como `dpetl_extract`, `dpetl_transform` e `dpetl_load`, que definem como o pacote `DPETL` deve executar os seus comandos.

Para além do `DPETL`, alguns _scripts_ auxiliares, que constam na pasta `src/`, preparam os descritores. A ordem de execução está na task `etl`:

  1. `extract`: gera o `datapackage.yaml` a partir do `raw_datapackage.yaml` e baixa os dados brutos.

  2. `transform`: escreve os dados processados.

  3. `load`: atualiza o `datapackage.json` e publica os dados no repositório do pacote.

O processo roda automaticamente de segunda a sexta, pelo workflow `etl.yaml` do GitHub Actions, e também pode ser disparado manualmente.
<!-- --8<-- [end:site] -->

## Documentação

Consulte a documentação completa, que explica as fases do ETL, os _scripts_ auxiliares e as configurações de cada pacote, em https://splor-mg.github.io/dados-orcamentarios/.
