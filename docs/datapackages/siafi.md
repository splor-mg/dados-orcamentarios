# dados_siafi

Os dados vêm do banco atual do SIAFI, filtrados pelo ano (`-p "Ano de Exercício={{year0}}"`). O ano é o atual, ou o da variável `YEAR` (veja [Auditoria do SIAFI](#auditoria-do-siafi)).

# Auditoria do SIAFI

O SIAFI muda retroativamente: valores de anos anteriores podem ser corrigidos depois que o ano acabou. Este fluxo detecta esses anos e republica os dados deles.

## Banco atual e histórico

O "banco atual" do SIAFI é uma janela deslizante de **5 anos** (hoje 2022 a 2026). A cada virada de ano ela se desloca (em 2027 passa a ser 2023 a 2027), e o ano mais antigo sai do atual e vai para o **histórico**.

Cada ano tem seu repositório (`dados-siafi-2026`, `dados-siafi-2025`...), com o datapackage `dados_siafi` do ano correspondente.

## SIAFI histórico

Para um ano fora do banco atual (`ano <= ano de hoje - 5`), a [task `yaml`](../tasks/pre_extract/yaml.md):

- troca `/current/` por `/previous/` nos comandos `bo export`;
- remove os campos marcados com `previous: false` nos schemas, que não existem no histórico.

## `dados_check_siafi`

É um datapackage de validação: tem as consultas (`alteracoes_orcamentarias`, `cota`, `credito`, `execucao`, `execucao_alem_credito`, `receita`, `restos_pagar` e `restos_pagar_folha`) sem filtro de ano (cobrem todo o banco atual), e é publicado em `dados-check-siafi`, com `data/*.csv` e `datapackage.json`.

## Como o workflow usa

Depois do `task etl`, quando o workflow roda todos os packages (ou só o `dados_check_siafi`), ele executa `src/check_siafi.py`:

1. Para cada CSV de `datapackages/dados_check_siafi/data/`, baixa a versão publicada em `dados-check-siafi` (`raw.githubusercontent.com`). Se não existe, o recurso é ignorado.
2. Soma as colunas numéricas por `ano`, nas duas versões, e compara. Um ano é **divergente** se alguma soma difere em mais de 0,01.
3. Descarta o ano atual (que já é atualizado pelo ETL normal) e imprime os anos divergentes.

Para cada ano divergente, o workflow roda de novo o `task etl` só para o `dados_siafi`, com `YEAR=<ano>`, o que atualiza o `dados-siafi-<ano>`.

```bash
# trecho do etl.yaml
divergent_years=$(python3 src/check_siafi.py)
for year in $divergent_years; do
  export ETL_DESCRIPTOR="-d datapackages/dados_siafi/datapackage.yaml"
  export YEAR="$year"
  task etl
done
```
