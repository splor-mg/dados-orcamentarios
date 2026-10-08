# task pre_load

Executa o script `src/build_datapackage.py datapackage.json`, que sobrescreve o `datapackage.json` gerado pelo `dpetl transform`

Ela é precedida pela [`task transform`](transform.md) e sempre roda antes da [`task load`](load.md).

Esse script é necessário quando um recurso usa o modo cli do transform, pois o `datapackage.json` gerado reinfere os metadados.

Portanto, o script deve usar novamente o `datapackages/fields.yaml` para completar os metadados dos campos.

> **Nota**: a ligação é feita pelo `name` do campo (e não mais pelo `target`).

??? note "Por que o dpetl reinfere os metadados?"
    O dpetl transform escreve um novo datapackage.json, porque a mudança feita pelo cli é imprevisível para o dpetl (e o datapackage.yaml estará desatualizado).

    Por exemplo, caso o cli executado adicione uma nova coluna, o datapackage.yaml não tem como ter esta coluna prevista no seu schema, então o dpetl infere novamente os recursos, para adicionar o novo campo.
