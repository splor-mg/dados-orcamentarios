# Datapackages

Datapackages atuais em `datapackages/`.

| Datapackage | Conteúdo | Publicado em |
| --- | --- | --- |
| [dados_classificadores](classificadores.md) | Tabelas auxiliares de classificadores. | `dados-classificadores` |
| [dados_siafi](siafi.md) | Dados anuais do SIAFI. | `dados-siafi-{{year0}}` |
| [dados_check_siafi](siafi.md#auditoria-do-siafi) | Validador do dados_siafi. | `dados-check-siafi` |
| [dados_aux_contratos](siad.md) | Tabelas auxiliares de contratos do SIAD. | `dados-aux-contratos` |
| [dados_ppo](ppo.md) | Dados do PPO (atualizado manualmente). | `dados-ppo-{{year1}}` |

## Adicionando um datapackage

1. Crie as pastas:

    ```bash
    NAME=datapackage_name
    mkdir -p datapackages/$NAME/{data,data_raw,schemas}
    touch datapackages/$NAME/{data,data_raw}/.gitkeep
    touch datapackages/$NAME/raw_datapackage.yaml
    ```

    > Nota: troque `datapackage_name` pelo nome do novo datapackage

2. Para a construção do `raw_datapackage.yaml`, siga o seguinte esqueleto:

    ```yaml
    name: datapackage_name
    title: Título do datapackage
    owner_org: secretaria-de-estado-de-planejamento-e-gestao-seplag
    dpetl_load:
      owner: splor-mg
      repo: datapackage-name
      level: orgs
      visibility: public

    resources:
      - name: minha_tabela
        type: table
        path: data_raw/minha_tabela.csv
        scheme: file
        format: csv
        mediatype: text/csv
        encoding: utf-8
        schema: schemas/minha_tabela.yaml
        dpetl_extract:
          mode: cli
          arguments:
            - bo export <consulta> -o datapackages/meu_datapackage/data_raw/minha_tabela.csv
      - ...
    ```

3. Se algum campo ainda não existir, inclua-o no `datapackages/fields.yaml`.

Na próxima execução da `task workflow`, o novo datapackage aparece nas opções do ETL.
