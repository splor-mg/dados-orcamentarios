SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_limite_cota.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_limite_cota.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_limite_cota.cod_orcamentaria_uo AS BIGINT)
        AS uo_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_sigla,
    tb_tab_unidade_orcamentaria.descricao AS uo_nome,
    CAST(tb_tab_limite_cota.cod_grupo_despesa AS BIGINT) AS grupo_cod,
    tb_tab_grupo_despesa.descricao AS grupo_desc,
    CAST(tb_tab_limite_cota.cod_iag AS BIGINT) AS iag_cod,
    tb_tab_iag.descricao AS iag_desc,
    CAST(tb_tab_limite_cota.cod_fonte AS BIGINT) AS fonte_cod,
    tb_tab_fonte.descricao AS fonte_desc,
    CAST(tb_tab_limite_cota.cod_procedencia AS BIGINT) AS ipu_cod,
    tb_tab_ipu.descricao AS ipu_desc,
    tb_tab_limite_cota.valor_fixado AS vlr_limite,
    from_timestamp(CAST(tb_tab_limite_cota.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_limite_cota
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria
    ON tb_tab_unidade_orcamentaria.cod_administracao_uo = tb_tab_limite_cota.cod_administracao_uo
    AND tb_tab_unidade_orcamentaria.cod_orgao_uo = tb_tab_limite_cota.cod_orgao_uo
    AND tb_tab_unidade_orcamentaria.cod_orcamentario_uo = tb_tab_limite_cota.cod_orcamentaria_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_grupo_despesa
    ON tb_tab_grupo_despesa.cod_grupo_despesa = tb_tab_limite_cota.cod_grupo_despesa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_iag
    ON tb_tab_iag.cod_iag = tb_tab_limite_cota.cod_iag
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_fonte
    ON tb_tab_fonte.cod_fonte = tb_tab_limite_cota.cod_fonte
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_ipu
    ON tb_tab_ipu.cod_ipu = tb_tab_limite_cota.cod_procedencia
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_limite_cota.status = 'N'
