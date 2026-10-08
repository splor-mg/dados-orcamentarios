# Transform

A etapa de **transform** processa os dados brutos da pasta `data_raw/` e escreve os dados transformados na pasta `data/` de cada datapackage.

Ela é precedida pela [`task extract`](extract.md).

## task transform

Executa o comando `dpetl $ETL_DESCRIPTOR --no-validate transform`, que roda o `dpetl transform`, mas sem fazer a validação do descriptor.

O `dpetl transform` é responsável por:

- Converter cada recurso para uma tabela e gravar em `data/`.

- Renomear os campos que têm `target`.

- Anonimizar os campos que têm `anonymize`.

- Gerar o `datapackage.json`.

??? note "Por que --no-validate?"
    Quando um recurso usa o modo cli do transform, o datapackage.json gerado reinfere os metadados, uma vez que a mudança feita pelo cli é imprevisível para o dpetl, e o .yaml estará desatualizado.

    Com isso, os parâmetros validadores (`constraints`) são adicionados ao .json depois, na task [pre_load](pre_load.md).

    Então, o transform não deve validar o descriptor. A validação acontece no load, com `--validate-before`.

### Opções de saída

Em `dpetl_transform`, pode-se definir:

  - **path**: (padrão `data`)

  - **format**: (padrão `csv.gz`, um csv compactado com gzip)

  - **encoding**: (padrão `utf-8`)

  - **delimiter**: (padrão `,`).

### Anonimização

No `fields.yaml`, a propriedade `anonymize` define como o campo é anonimizado.

No exemplo, o CPF (11 dígitos) é cifrado com `aes_siv`, e o CNPJ, que não passa pelo `filter`, fica como está:

```yaml
--8<-- "docs/templates/cnpj_cpf.yaml:fields"
```

Este método usa a chave da variável de ambiente `ANONYMIZE_SECRET_KEY`, que pode ser gerada com:

```bash
dpetl transform keygen
```

Há outras opções de anonimização, com máscara ou `sha256`. Veja a [documentação do dpetl](https://splor-mg.github.io/dpetl/transform/).
