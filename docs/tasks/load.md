# Load

A etapa de **load** publica os dados processados da pasta `data/` no próprio repositório do datapackage.

Ela é precedida pela task [`pre_load`](pre_load.md).

## task load

Executa o comando `dpetl --validate-before load`, que roda o `dpetl load`, validando o descriptor antes de publicar.

> **Nota**: não deve ser passada a variável `$ETL_PACKAGE`, pois no workflow, essa variável é usada para definir o datapackage.yaml.

O `dpetl load` é responsável por:

- Validar o pacote inteiro antes de publicar (`--validate-before`).

- Remover as propriedades `dpetl_extract`, `dpetl_transform` e `dpetl_load` do `datapackage.json` publicado.

- Publicar os arquivos da pasta `data/` e o `datapackage.json` no repositório.

    - Caso o repositório não exista, ele é criado.

- Excluir os arquivos desatualizados (ex.: se um recurso mudou de nome).

> **Nota**: precisa de autenticação, pelo `GH_TOKEN` ou por `GH_APP_ID` + `GH_APP_PRIVATE_KEY`.

### Opções de publicação:

Em `dpetl_load` (nível do package), pode-se definir:

- **owner**: usuário ou organização, dono do repositório (obrigatório se `repo` for definido).

- **repo**: nome do repositório de destino (se não definido, publica localmente).

- **level**: `user` (usuário; padrão) ou `orgs` (organização).

- **visibility**: `private` (privado; padrão) ou `public` (público).

Exemplo:

```yaml
--8<-- "docs/templates/siafi.yaml:dpetl_load"
```

Para mais detalhes, consulte a [documentação do dpetl](https://splor-mg.github.io/dpetl/load/).
