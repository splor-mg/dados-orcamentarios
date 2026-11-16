SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_orcamento_receita.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_orcamento_receita.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_orcamento_receita.cod_orcamentario_uo AS BIGINT)
        AS uo_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_sigla,
    tb_tab_unidade_orcamentaria.descricao AS uo_nome,
    concat(
        CAST(CAST(tb_tab_classificacao_receita.cod_categoria AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_origem AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_especie AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_rubrica AS BIGINT) AS STRING),
        lpad(CAST(CAST(tb_tab_classificacao_receita.cod_alinea AS BIGINT) AS STRING), 2, '0'),
        CAST(CAST(tb_tab_classificacao_receita.cod_sub_alinea AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_tipo_receita AS BIGINT) AS STRING),
        lpad(CAST(CAST(tb_tab_classificacao_receita.cod_item AS BIGINT) AS STRING), 2, '0'),
        lpad(CAST(CAST(tb_tab_classificacao_receita.cod_sub_item AS BIGINT) AS STRING), 3, '0')
    ) AS receita_cod,
    tb_tab_classificacao_receita.descricao AS receita_desc,
    CAST(tb_tab_orcamento_receita.cod_fonte AS BIGINT) AS fonte_cod,
    tb_tab_fonte.descricao AS fonte_desc,
    classificacao_matriz.base_legal,
    classificacao_matriz.interpretacao,
    tb_tab_orcamento_receita.metodologia_calculo AS metodologia,
    tb_tab_orcamento_receita.valor_ldo AS vlr_ldo_rec,
    tb_tab_orcamento_receita.valor_loa AS vlr_loa_rec,
    from_timestamp(CAST(tb_tab_orcamento_receita.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_orcamento_receita
JOIN db_dlseplag_prod_ppo_staging.tb_tab_classificacao_receita
    ON tb_tab_classificacao_receita.cod_classificacao_receita = tb_tab_orcamento_receita.cod_classificacao_receita
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria
    ON tb_tab_unidade_orcamentaria.cod_administracao_uo = tb_tab_orcamento_receita.cod_administracao_uo
    AND tb_tab_unidade_orcamentaria.cod_orgao_uo = tb_tab_orcamento_receita.cod_orgao_uo
    AND tb_tab_unidade_orcamentaria.cod_orcamentario_uo = tb_tab_orcamento_receita.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_fonte
    ON tb_tab_fonte.cod_fonte = tb_tab_orcamento_receita.cod_fonte
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_classificacao_receita classificacao_matriz
    ON classificacao_matriz.nivel_classificacao_receita = 'MATRIZ'
    AND classificacao_matriz.cod_categoria = tb_tab_classificacao_receita.cod_categoria
    AND classificacao_matriz.cod_origem = tb_tab_classificacao_receita.cod_origem
    AND classificacao_matriz.cod_especie = tb_tab_classificacao_receita.cod_especie
    AND classificacao_matriz.cod_rubrica = tb_tab_classificacao_receita.cod_rubrica
    AND classificacao_matriz.cod_alinea = tb_tab_classificacao_receita.cod_alinea
    AND classificacao_matriz.cod_sub_alinea = tb_tab_classificacao_receita.cod_sub_alinea
    AND classificacao_matriz.cod_tipo_receita = 0
    AND classificacao_matriz.cod_item = 0
    AND classificacao_matriz.cod_sub_item = 0
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_orcamento_receita.status = 'N'
