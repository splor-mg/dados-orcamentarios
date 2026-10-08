# Extract

A etapa de **extract** baixa os dados brutos para a pasta `data_raw/` de cada datapackage.

Ela é precedida pela `task pre_extract`, que roda [`workflow`](pre_extract/workflow.md), [`yaml`](pre_extract/yaml.md) e [`bocache`](pre_extract/bocache.md).

## task extract

Executa o comando `dpetl $ETL_DESCRIPTOR extract --delay 5`, que roda o `dpetl extract`, com um intervalo de 5 segundos entre as extrações de cada recurso.

- **`mode: cli`**: executa os comandos listados em `arguments`, dentro da propriedade `dpetl_extract` do recurso.

    - Cada comando é um `bo export` do [bo-cli](https://github.com/splor-mg/bo-cli), que baixa uma consulta do BO para `data_raw/`.

```yaml
{% include "classificadores.yaml" %}
```

Para as demais opções (modos `api` e `email`, flags), consulte a [documentação do dpetl](https://splor-mg.github.io/dpetl/extract/).

> **Nota**: cada recurso tem seu schema validado após a sua extração, e caso algum esteja inválido, o processo é interrompido.
