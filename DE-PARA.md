# Mapeamento de Campos - Datapackage PPO-MG

## Índice

1. [Orçamento da Despesa Fiscal / Itens de Despesa](#base-orcam-despesa-item-fiscal) - 21 campos
2. [Detalhamento Plurianual Fiscal](#base-qdd-plurianual) - 23 campos
3. [Detalhamento Plurianual Investimento](#base-qdd-plurianual-invest) - 21 campos
4. [Orçamento da Despesa de Investimento](#base-orcam-despesa-investimento) - 21 campos
5. [Detalhamento de Obras](#base-detalhamento-obras) - 24 campos
6. [QDD Fiscal](#base-qdd-fiscal) - 27 campos
7. [QDD Investimento](#base-qdd-investimento) - 23 campos
8. [Orçamento da Receita Fiscal](#base-orcam-receita-fiscal) - 24 campos
9. [Orçamento da Receita Investimento](#base-orcam-receita-investimento) - 14 campos
10. [Registro de Obras no SIAD](#base-obras-siad) - 10 campos
11. [Categoria de Pessoal](#base-categoria-pessoal) - 5 campos
12. [Repasse de Recursos](#base-repasse-recursos) - 9 campos
13. [Limite de Cota](#base-limite-cota) - 15 campos
14. [Base Intraorçamentária de Detalhamento](#base-intra-orcamentaria-detalhamento) - 4 campos
15. [Base Intraorçamentária de Repasse](#base-intra-orcamentaria-repasse) - 9 campos
16. [Relação das Unidades Orçamentárias e suas Versões](#base-unidades-orcamentaria-versoes) - 4 campos

---

## Orçamento da Despesa Fiscal / Itens de Despesa

**Nome da base SISOR:** `base_orcam_despesa_item_fiscal`

**Nome da base PPO:** `exemplo`

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Órgão - Código | Código do Órgão | orgao_cod |  |
| Órgão - Nome e Sigla | Órgão | orgao_nome_sigla |  |
| Unidade Orçamentária - Código | Código da UO | uo_cod |  |
| Unidade Orçamentária - Nome e Sigla | Unidade Orçamentária | uo_nome_sigla |  |
| Função - Código | Função | funcao_cod |  |
| Subfunção - Código | Subfunção | subfuncao_cod |  |
| Programa - Código | Programa | programa_cod |  |
| Identificador - Código | Identificador | identificador_cod |  |
| Projeto Atividade - Código | Projeto_Atividade | projeto_atividade_cod |  |
| Ação - Código | Ação | acao_cod |  |
| Subprojeto - Código | Subprojeto | subprojeto_cod |  |
| Categoria Econômica Despesa - Código | Categoria | categoria_cod |  |
| Grupo Despesa - Código | Grupo_Despesa | grupo_cod |  |
| Modalidade Aplicação - Código | Modalidade | modalidade_cod |  |
| Elemento Despesa - Código | Elemento_Despesa | elemento_cod |  |
| Item Despesa - Código | Item_Despesa | item_cod |  |
| Fonte Recurso - Código | Fonte | fonte_cod |  |
| Procedência - Código | IPU | ipu_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Ação - Descrição | Descrição | acao_desc |  |
| Valor (R$) | Valor (R$) | vlr_loa_desp |  |

*Total de campos: 21*

---

## Detalhamento Plurianual Fiscal

**Nome da base SISOR:** `base_qdd_plurianual`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Ano de Exercício | ANO | ano |  |
| Órgão - Código | COD_ORGAO | orgao_cod |  |
| Órgão - Nome e Sigla | DESC_ORGAO | orgao_nome_sigla |  |
| Unidade Orçamentária - Código | COD_UO | uo_cod |  |
| Unidade Orçamentária - Nome e Sigla | DESC_UO | uo_nome_sigla |  |
| Função - Código | FUNCAO | funcao_cod |  |
| Subfunção - Código | SUBFUNCAO | subfuncao_cod |  |
| Programa - Código | COD_PROGRAMA | programa_cod |  |
| Identificador - Código | IDENT_PROJATIV | identificador_cod |  |
| Projeto Atividade - Código | PROJ_ATIV | projeto_atividade_cod |  |
| Ação - Código | AÇÃO | acao_cod |  |
| Subprojeto - Código | SUBPROJETO | subprojeto_cod |  |
| Categoria Econômica Despesa - Código | CATEGORIA | categoria_cod |  |
| Grupo Despesa - Código | GRUPO_DESPESA | grupo_cod |  |
| Fonte Recurso - Código | FONTE | fonte_cod |  |
| Procedência - Código | IPU | ipu_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Programa - Descrição | PROGRAMA | programa_desc |  |
| Ação - Descrição | ACAO | acao_desc |  |
| Valor Ano de Referência (R$) | VALOR (R$) 2026 | vlr_loa_desp_ano0 |  |
| Valor Ano de Referência + 1 (R$) | VALOR (R$) 2027 | vlr_loa_desp_ano1 |  |
| Valor Ano de Referência + 2 (R$) | VALOR (R$) 2028 | vlr_loa_desp_ano2 |  |
| Valor Ano de Referência + 3 (R$) | VALOR (R$) 2029 | vlr_loa_desp_ano3 |  |

*Total de campos: 23*

---

## Detalhamento Plurianual Investimento

**Nome da base SISOR:** `base_qdd_plurianual_invest`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Ano de Exercício | ANO | ano |  |
| Órgão - Código | COD_ORGAO | orgao_cod |  |
| Órgão - Nome e Sigla | DESC_ORGAO | orgao_nome_sigla |  |
| Unidade Orçamentária - Código | COD_UO | uo_cod |  |
| Unidade Orçamentária - Nome e Sigla | DESC_UO | uo_nome_sigla |  |
| Função - Código | FUNCAO | funcao_cod |  |
| Subfunção - Código | SUBFUNCAO | subfuncao_cod |  |
| Programa - Código | COD_PROGRAMA | programa_cod |  |
| Identificador - Código | IDENT_PROJATIV | identificador_cod |  |
| Projeto Atividade - Código | PROJ_ATIV | projeto_atividade_cod |  |
| Ação - Código | AÇÃO | acao_cod |  |
| Subprojeto - Código | SUBPROJETO | subprojeto_cod |  |
| Categoria (?) - Código | CATEGORIA | categoria__cod |  |
| Fonte Investimento - Código | FONTE | fonte_invest_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Programa - Descrição | PROGRAMA | programa_desc |  |
| Ação - Descrição | ACAO | acao_desc |  |
| Valor Ano de Referência (R$) | VALOR (R$) 2026 | vlr_loa_desp_invest_ano0 |  |
| Valor Ano de Referência + 1 (R$) | VALOR (R$) 2027 | vlr_loa_desp_invest_ano1 |  |
| Valor Ano de Referência + 2 (R$) | VALOR (R$) 2028 | vlr_loa_desp_invest_ano2 |  |
| Valor Ano de Referência + 3 (R$) | VALOR (R$) 2029 | vlr_loa_desp_invest_ano3 |  |

*Total de campos: 21*

---

## Orçamento da Despesa de Investimento

**Nome da base SISOR:** `base_orcam_despesa_investimento`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Órgão - Código | Código do Órgão | orgao_cod |  |
| Órgão - Nome e Sigla | Órgão | orgao_nome_sigla |  |
| Unidade Orçamentária - Código | Código da UO | uo_cod |  |
| Unidade Orçamentária - Nome e Sigla | Unidade Orçamentária | uo_nome_sigla |  |
| Função - Código | Função | funcao_cod |  |
| Subfunção - Código | Subfunção | subfuncao_cod |  |
| Programa - Código | Programa | programa_cod |  |
| Identificador - Código | Identificador | identificador_cod |  |
| Projeto Atividade - Código | Projeto_Atividade | projeto_atividade_cod |  |
| Ação - Código | Ação | acao_cod |  |
| Subprojeto - Código | Subprojeto | subprojeto_cod |  |
| Fonte Recurso - Código | Fonte | fonte_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Ação - Descrição | Descrição | acao_desc |  |
| Categoria (?) - Código e Nome | Categoria | categoria__cod_nome |  |
| Natureza - Código | Código da Natureza | natureza_cod |  |
| Natureza - Descrição | Natureza | natureza_desc |  |
| Valor Ano de Referência (R$) | VALOR (R$) 2026 | vlr_loa_desp_invest_ano0 |  |
| Valor Ano de Referência + 1 (R$) | VALOR (R$) 2027 | vlr_loa_desp_invest_ano1 |  |
| Valor Ano de Referência + 2 (R$) | VALOR (R$) 2028 | vlr_loa_desp_invest_ano2 |  |
| Valor Ano de Referência + 3 (R$) | VALOR (R$) 2029 | vlr_loa_desp_invest_ano3 |  |

*Total de campos: 21*

---

## Detalhamento de Obras

**Nome da base SISOR:** `base_detalhamento_obras`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária - Código | UO | uo_cod |  |
| Função - Código | FUNCAO | funcao_cod |  |
| Subfunção - Código | SUBFUNCAO | subfuncao_cod |  |
| Programa - Código | PROGRAMA | programa_cod |  |
| Ação - Código | ACAO | acao_cod |  |
| Subprojeto - Código | SUBPROJETO | subprojeto_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Obra - Número SISOR | NUMERO DA OBRA SISOR | obra_num_sisor |  |
| Obra - Número SIAD | NUMERO DA OBRA SIAD | obra_num_siad |  |
| Obra - Descrição | DESCRICAO DA OBRA | obra_desc |  |
| Obra - Status | STATUS DA OBRA | obra_status |  |
| Obra - Unidade de Medida | UNIDADE DE MEDIDA DA OBRA | obra_unidade_medida |  |
| Obra - Quantidade | QUANTIDADE | obra_quantidade |  |
| Obra - Alterar Unidade de Medida | ALTERAR UNIDADE DE MEDIDA DA OBRA | obra_alterar_unidade_medida |  |
| Obra - Região Geográfica Intermediária | REGIÃO GEOGRÁFICA INTERMEDIÁRIA | obra_regiao_geografica_intermediaria |  |
| Obra - Município | MUNICÍPIO | obra_municipio |  |
| Valor Tesouro Ano de Referência (R$) | VALOR TESOURO 2026 (R$) | vlr_tesouro_ano0 |  |
| Valor Outros Ano de Referência (R$) | VALOR OUTROS 2026 (R$) | vlr_outros_ano0 |  |
| Valor Tesouro Ano de Referência + 1 (R$) | VALOR TESOURO 2027 (R$) | vlr_tesouro_ano1 |  |
| Valor Outros Ano de Referência + 1 (R$) | VALOR OUTROS 2027 (R$) | vlr_outros_ano1 |  |
| Valor Tesouro Ano de Referência + 2 (R$) | VALOR TESOURO 2028 (R$) | vlr_tesouro_ano2 |  |
| Valor Outros Ano de Referência + 2 (R$) | VALOR OUTROS 2028 (R$) | vlr_outros_ano2 |  |
| Valor Tesouro Ano de Referência + 3 (R$) | VALOR TESOURO 2029 (R$) | vlr_tesouro_ano3 |  |
| Valor Outros Ano de Referência + 3 (R$) | VALOR OUTROS 2029 (R$) | vlr_outros_ano3 |  |

*Total de campos: 24*

---

## QDD Fiscal

**Nome da base SISOR:** `base_qdd_fiscal`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Ano de Exercício | ANO | ano |  |
| Órgão - Código | COD_ORGAO | orgao_cod |  |
| Órgão - Nome e Sigla | ORGAO | orgao_nome_sigla |  |
| Poder Unidade Orçamentária - Código | PODER | poder_cod |  |
| Situação | SITUACAO | situacao |  |
| Unidade Orçamentária - Código | COD_UO | uo_cod |  |
| Unidade Orçamentária - Nome e Sigla | UO | uo_nome_sigla |  |
| Categoria Econômica Despesa - Código | CATEGORIA | categoria_cod |  |
| Grupo Despesa - Código | GRUPO_DESPESA | grupo_cod |  |
| Modalidade Aplicação - Código | MODALIDADE | modalidade_cod |  |
| Elemento Despesa - Código | ELEMENTO_DESPESA | elemento_cod |  |
| Fonte Recurso - Código | FONTE | fonte_cod |  |
| Procedência - Código | IPU | ipu_cod |  |
| SEQ_PROGTRAB (?) | SEQ_PROGTRAB | seq_progtrab |  |
| Função - Código | FUNCAO | funcao_cod |  |
| Subfunção - Código | SUB_FUNCAO | subfuncao_cod |  |
| Programa - Código | PROGRAMA | programa_cod |  |
| Identificador - Código | IDENT_PROJATIV | identificador_cod |  |
| Projeto Atividade - Código | PROJ_ATIV | projeto_atividade_cod |  |
| Ação - Código | AÇÃO | acao_cod |  |
| Subprojeto - Código | SUB_PROJETO | subprojeto_cod |  |
| Valor UO (R$) | VALOR UO (R$) | vlr_loa_desp_uo |  |
| Valor SCPPO (R$) | VALOR SCPPO (R$) | vlr_loa_desp_scppo |  |
| Valor Final (R$) | VALOR FINAL (R$) | vlr_loa_desp |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Ação - Descrição | NOME_ACAO | acao_desc |  |
| Programa - Descrição | NOME_PROGRAMA | programa_desc |  |

*Total de campos: 27*

---

## QDD Investimento

**Nome da base SISOR:** `base_qdd_investimento`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Ano de Exercício | ANO | ano |  |
| Órgão - Código | COD_ORGAO | orgao_cod |  |
| Órgão - Nome e Sigla | ORGAO | orgao_nome_sigla |  |
| Poder Unidade Orçamentária - Código | PODER | poder_cod |  |
| Unidade Orçamentária - Código | COD_UO | uo_cod |  |
| Unidade Orçamentária - Nome e Sigla | UO | uo_nome_sigla |  |
| SEQ_PROGTRAB (?) | SEQ_PROGTRAB | seq_progtrab |  |
| Função - Código | FUNCAO | funcao_cod |  |
| Subfunção - Código | SUB_FUNCAO | subfuncao_cod |  |
| Programa - Código | PROGRAMA | programa_cod |  |
| Identificador - Código | IDENT_PROJATIV | identificador_cod |  |
| Projeto Atividade - Código | PROJ_ATIV | projeto_atividade_cod |  |
| Ação - Código | AÇÃO | acao_cod |  |
| Valor (R$) | VALOR (R$) | vlr_loa_desp_invest |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Ação - Descrição | DESC_PROJETO_ATIV | acao_desc |  |
| Categoria (?) - Código e Nome | CATEGORIA | categoria__cod_nome |  |
| Natureza - Código | COD_NATUREZA | natureza_cod |  |
| Natureza - Descrição | NATUREZA | natureza_desc |  |
| Fonte Investimento - Código | COD_FONTE | fonte_invest_cod |  |
| Fonte Investimento - Descrição | FONTE | fonte_invest_desc |  |
| Ação - Descrição | NOME_ACAO | acao_desc |  |
| Programa - Descrição | NOME_PROGRAMA | programa_desc |  |

*Total de campos: 23*

---

## Orçamento da Receita Fiscal

**Nome da base SISOR:** `base_orcam_receita_fiscal`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária - Código | UO_COD | uo_cod |  |
| Unidade Orçamentária - Nome | NOME_UO | uo_nome |  |
| Unidade Orçamentária - Sigla | SIGLA_UO | uo_sigla |  |
| Fonte Recurso - Código | COD_FONTE | fonte_cod |  |
| Fonte Recurso - Descrição | FONTE | fonte_desc |  |
| Interpretação | INTERPRETACAO | interpretacao |  |
| Categoria (?) - Código | CATEGORIA | categoria__cod |  |
| Origem - Código | ORIGEM | origem_cod |  |
| Espécie - Código | ESPECIE | especie_cod |  |
| Rubrica - Código | RUBRICA | rubrica_cod |  |
| Alínea - Código | ALINEA | alinea_cod |  |
| Subalínea - Código | SUBALINEA | subalinea_cod |  |
| Receita - Tipo | TIPO_RECEITA | receita_tipo |  |
| Item Despesa - Código | ITEM | item_cod |  |
|  | SUBITEM | subitem_cod |  |
| Classificação Receita - Código | COD_RECEITA | receita_cod |  |
| Classificação Receita - Descrição | RECEITA | receita_desc |  |
| Receita - Interpretação | INTERP_RECEITA | receita_interpretacao |  |
| Valor UO (R$) | VALOR UO (R$) | vlr_loa_rec_uo |  |
| Valor SCPPO (R$) | VALOR SCPPO (R$) | vlr_loa_rec_scppo |  |
| Valor Final (R$) | VALOR FINAL (R$) | vlr_loa_rec |  |
| Ano de Exercício | ANO | ano |  |
| Base Legal | BASE LEGAL | base_legal |  |
| Metodologia de Cálculo e Premissas Utilizadas | METODOLOGIA DE CÁLCULO E PREMISSAS UTILIZADAS | metodologia |  |

*Total de campos: 24*

---

## Orçamento da Receita Investimento

**Nome da base SISOR:** `base_orcam_receita_investimento`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária - Código | COD_UO | uo_cod |  |
| Unidade Orçamentária - Nome | NOME_UO | uo_nome |  |
| Unidade Orçamentária - Sigla | SIGLA_UO | uo_sigla |  |
| Categoria (?) - Código | CATEGORIA | categoria__cod |  |
| Subcategoria - Código | SUBCATEGORIA | subcategoria_cod |  |
| Alínea - Código | ALINEA | alinea_cod |  |
| Subalínea - Código | SUBALINEA | subalinea_cod |  |
| Classificação Receita - Código | COD_RECEITA | receita_cod |  |
| Origem - Nível | NIVEL_ORIGEM | origem_nivel |  |
| Classificação Receita - Descrição | RECEITA | receita_desc |  |
| Valor UO (R$) | VALOR UO (R$) | vlr_loa_rec_uo_invest |  |
| Valor SCPPO (R$) | VALOR SCPPO (R$) | vlr_loa_rec_scppo_invest |  |
| Valor Final (R$) | VALOR FINAL (R$) | vlr_loa_rec_invest |  |
| Ano de Exercício | ANO | ano |  |

*Total de campos: 14*

---

## Registro de Obras no SIAD

**Nome da base SISOR:** `base_obras_siad`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Órgão - Código e Nome | ORGAO_COD | orgao_cod_nome |  |
| Unidade Administrativa - Código e Nome | UNIDADE_ADIMINISTRATIVA_COD | ua_cod_nome |  |
| Obra - Número SIAD | Número da Obra SIAD | obra_num_siad |  |
| Unidade Orçamentária - Número de Referência | Número de Referência da UO | uo_num_ref |  |
| Situação | Situação | situacao |  |
| Obra - Descrição | Descrição | obra_desc |  |
| Obra - Data de Início | Data de Início | obra_data_inicio |  |
| Obra - Data de Término | Data de Término | obra_data_termino |  |
| Ano de Exercício | Ano de Exercício | ano |  |
| Valor Global (R$) | Valor Global (R$) | vlr_global |  |

*Total de campos: 10*

---

## Categoria de Pessoal

**Nome da base SISOR:** `base_categoria_pessoal`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Ano de Exercício | Ano de Exercício | ano | ano_ref |
| Unidade Orçamentária - Código e Sigla | UO | uo_cod_sigla |  |
| Pessoal - Classificação | Classificação | pessoal_classificacao |  |
| Pessoal - Categoria | Categoria | pessoal_categoria |  |
| Pessoal - Quantidade | Quantidade | pessoal_quantidade |  |

*Total de campos: 5*

---

## Repasse de Recursos

**Nome da base SISOR:** `base_repasse_recursos`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária Financiadora - Código | Cód. UO Financiadora | uo_financiadora_cod |  |
| Unidade Orçamentária Financiadora - Nome | UO Financiadora | uo_financiadora_nome |  |
| Unidade Orçamentária Beneficiada - Código | Cód. UO Beneficiada | uo_beneficiada_cod |  |
| Unidade Orçamentária Beneficiada - Nome | UO Beneficiada | uo_beneficiada_nome |  |
| Grupo Despesa - Código | Grupo de Despesa | grupo_cod |  |
| Fonte Recurso - Código | Fonte | fonte_cod |  |
| Procedência - Código | IPU | ipu_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Valor Transferido (R$) | Valor Transferido (R$) | vlr_repasse |  |

*Total de campos: 9*

---

## Limite de Cota

**Nome da base SISOR:** `base_limite_cota`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária - Código | Cód. UO | uo_cod |  |
| Unidade Orçamentária - Sigla | UO | uo_sigla |  |
| Grupo Despesa - Código | Grupo de Despesa | grupo_cod |  |
| Fonte Recurso - Código | Fonte | fonte_cod |  |
| Procedência - Código | IPU | ipu_cod |  |
| Identificador Orçamento - Código | IAG | iag_cod |  |
| Valor Limite Ano de Referência (R$) | Valor Limite 2026 | vlr_limite_ano0 |  |
| Valor Utilizado Ano de Referência (R$) | Valor Utilizado 2026 | vlr_utilizado_ano0 |  |
| Valor Transferido | Valor Transferido | vlr_transferido |  |
| Valor Limite Ano de Referência + 1 (R$) | Valor Limite 2027 | vlr_limite_ano1 |  |
| Valor Utilizado Ano de Referência + 1 (R$) | Valor Utilizado 2027 | vlr_utilizado_ano1 |  |
| Valor Limite Ano de Referência + 2 (R$) | Valor Limite 2028 | vlr_limite_ano2 |  |
| Valor Utilizado Ano de Referência + 2 (R$) | Valor Utilizado 2028 | vlr_utilizado_ano2 |  |
| Valor Limite Ano de Referência + 3 (R$) | Valor Limite 2029 | vlr_limite_ano3 |  |
| Valor Utilizado Ano de Referência + 3 (R$) | Valor Utilizado 2029 | vlr_utilizado_ano3 |  |

*Total de campos: 15*

---

## Base Intraorçamentária de Detalhamento

**Nome da base SISOR:** `base_intra_orcamentaria_detalhamento`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária - Código | Cód. UO Beneficiada | uo_cod |  |
| Unidade Orçamentária - Sigla | UO Beneficiada | uo_sigla |  |
| Valor Recebido (R$) | Valor Recebido (R$) | vlr_recebido |  |
| Valor Detalhado (R$) | Valor Detalhado (R$) | vlr_detalhado |  |

*Total de campos: 4*

---

## Base Intraorçamentária de Repasse

**Nome da base SISOR:** `base_intra_orcamentaria_repasse`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária Repassadora - Código | Cód. UO Repassadora | uo_repassadora_cod |  |
| Unidade Orçamentária Repassadora - Sigla | UO Repassadora | uo_repassadora_sigla |  |
| Programa de Trabalho - Código Formatado | Cód. Programa de Trabalho | programa_trabalho_fmt |  |
| Ação - Descrição | Ação | acao_desc |  |
| Natureza de Despesa - Código Formatado | Cód. Natureza de Despesa | natureza_desp_fmt |  |
| Item - Descrição | Elemento Item | item_desc |  |
| Valor Repassado (R$) | Valor Repassado (R$) | vlr_repassado |  |
| Unidade Orçamentária Beneficiada - Código | Cód. UO Beneficiada | uo_beneficiada_cod |  |
| Unidade Orçamentária Beneficiada - Sigla | UO Beneficiada | uo_beneficiada_sigla |  |

*Total de campos: 9*

---

## Relação das Unidades Orçamentárias e suas Versões

**Nome da base SISOR:** `base_unidades_orcamentaria_versoes`

**Nome da base PPO:** *Não definido*

| Título | SISOR | AID | PPO |
|---|---|---|---|
| Unidade Orçamentária - Código | UO_COD | uo_cod |  |
| Unidade Orçamentária - Nome | UO_DESC | uo_nome |  |
| Unidade Orçamentária - Sigla | UO_SIGLA | uo_sigla |  |
| Momento - Código | MOMENTO_COD | momento_cod |  |

*Total de campos: 4*

---

