SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_uo_categoria_pessoal.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_uo_categoria_pessoal.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_uo_categoria_pessoal.cod_orcamentario_uo AS BIGINT)
        AS uo_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_sigla,
    tb_tab_unidade_orcamentaria.descricao AS uo_nome,
    tb_tab_tipo_categoria_pessoal.descricao AS pessoal_classificacao,
    tb_tab_categoria_pessoal.descricao AS pessoal_categoria,
    CAST(tb_tab_uo_categoria_pessoal.valor AS BIGINT) AS pessoal_quantidade,
    from_timestamp(CAST(tb_tab_uo_categoria_pessoal.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_uo_categoria_pessoal
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria
    ON tb_tab_unidade_orcamentaria.cod_administracao_uo = tb_tab_uo_categoria_pessoal.cod_administracao_uo
    AND tb_tab_unidade_orcamentaria.cod_orgao_uo = tb_tab_uo_categoria_pessoal.cod_orgao_uo
    AND tb_tab_unidade_orcamentaria.cod_orcamentario_uo = tb_tab_uo_categoria_pessoal.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_categoria_pessoal
    ON tb_tab_categoria_pessoal.cod_categoria_pessoal = tb_tab_uo_categoria_pessoal.cod_categoria_pessoal
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_tipo_categoria_pessoal
    ON tb_tab_tipo_categoria_pessoal.cod_tipo_categoria_pessoal = tb_tab_categoria_pessoal.cod_tipo_categoria_pessoal
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_uo_categoria_pessoal.status = 'N'
    AND tb_tab_uo_categoria_pessoal.valor > 0
