# task yaml

Executa o script `src/build_datapackage.py raw_datapackage.yaml`, que gera o `datapackage.yaml`, a partir do `raw_datapackage.yaml`, para ser usado pelo `dpetl extract` e pelo `dpetl transform`.

## fields.yaml

O script usa o arquivo `datapackages/fields.yaml`, que reúne os metadados dos campos (`type, title, description, constraints, anonymize...`), para completar o schema de todos os datapackages.

O schema de cada recurso só liga o nome da coluna de origem ao nome padronizado, pela propriedade `target`:

```yaml
--8<-- "docs/templates/cnpj_cpf.yaml:schema"
```

O `fields.yaml` traz o restante da definição do campo:

```yaml
--8<-- "docs/templates/cnpj_cpf.yaml:fields"
```

Ao gerar o `datapackage.yaml`, o campo completo é copiado de `fields.yaml` e o nome original da coluna é mantido:

```yaml
--8<-- "docs/templates/cnpj_cpf.yaml:datapackage"
```

Caso o target do schema não tenha um correspondente no name do `fields.yaml`, é gerado um aviso, como:

`[WARNING] datapackages/dados_ppo/raw_datapackage.yaml: 1 field name(s) not found in fields.yaml: classificacao_excluido`

> **Nota**: para manter o `fields.yaml` organizado, a ordenação dos campos por nome pode ser feita com `python src/sort_fields.py`.

## Placeholders

O script também substitui os placeholders (`{{date}},  {{year0}} ...`), usando o ano atual ou a variável de ambiente `YEAR`.

No `raw_datapackage.yaml`, é possível usar:

- `{{date}}`: data de hoje (`AAAA-MM-DD`).

- `{{year0}}, {{year1}}...`: o ano de referência somado ao número (`year0` = o próprio ano, `year1` = ano seguinte...).

## SIAFI

Para lidar especificamente com o universo **histórico do SIAFI**, quando o ano está fora do banco atual, o `/current/` é trocado por `/previous/` no `bo export`.

Além disso, nos schemas, é possível definir um campo com o parâmetro `previous: false`, para removê-lo do descriptor quando o campo não existe no histórico.

No exemplo, o `raw_datapackage.yaml` do `dados_siafi` é processado com `YEAR=2002 task yaml`:

```yaml
--8<-- "docs/templates/siafi.yaml:raw_datapackage"
```

Após a execução, os placeholders `{{year0}}` viraram `2002`, o `/current/` virou `/previous/`, e o campo `vlr_cota_cancelada` foi removido.

```yaml
--8<-- "docs/templates/siafi.yaml:datapackage"
```
