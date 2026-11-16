SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_repasse_recurso.cod_administracao_uo_c AS BIGINT) * 1000
        + CAST(tb_tab_repasse_recurso.cod_orgao_uo_c AS BIGINT) * 10
        + CAST(tb_tab_repasse_recurso.cod_orcamentario_uo_c AS BIGINT)
        AS uo_financiadora_cod,
    uo_financiadora.sigla AS uo_financiadora_sigla,
    uo_financiadora.descricao AS uo_financiadora_nome,
    CAST(tb_tab_repasse_recurso.cod_administracao_uo_b AS BIGINT) * 1000
        + CAST(tb_tab_repasse_recurso.cod_orgao_uo_b AS BIGINT) * 10
        + CAST(tb_tab_repasse_recurso.cod_orcamentario_uo_b AS BIGINT)
        AS uo_beneficiada_cod,
    uo_beneficiada.sigla AS uo_beneficiada_sigla,
    uo_beneficiada.descricao AS uo_beneficiada_nome,
    CAST(tb_tab_repasse_recurso.cod_grupo_despesa AS BIGINT) AS grupo_cod,
    tb_tab_grupo_despesa.descricao AS grupo_desc,
    CAST(tb_tab_repasse_recurso.cod_iag AS BIGINT) AS iag_cod,
    tb_tab_iag.descricao AS iag_desc,
    CAST(tb_tab_repasse_recurso.cod_grupo_fonte AS BIGINT) AS grupo_fonte_cod,
    tb_tab_grupo_fonte.descricao AS grupo_fonte_desc,
    CAST(tb_tab_repasse_recurso.cod_fonte AS BIGINT) AS fonte_cod,
    tb_tab_fonte.descricao AS fonte_desc,
    CAST(tb_tab_repasse_recurso.cod_ipu AS BIGINT) AS ipu_cod,
    tb_tab_ipu.descricao AS ipu_desc,
    tb_tab_repasse_recurso.valor AS vlr_repasse,
    from_timestamp(CAST(tb_tab_repasse_recurso.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_repasse_recurso
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria uo_financiadora
    ON uo_financiadora.cod_administracao_uo = tb_tab_repasse_recurso.cod_administracao_uo_c
    AND uo_financiadora.cod_orgao_uo = tb_tab_repasse_recurso.cod_orgao_uo_c
    AND uo_financiadora.cod_orcamentario_uo = tb_tab_repasse_recurso.cod_orcamentario_uo_c
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria uo_beneficiada
    ON uo_beneficiada.cod_administracao_uo = tb_tab_repasse_recurso.cod_administracao_uo_b
    AND uo_beneficiada.cod_orgao_uo = tb_tab_repasse_recurso.cod_orgao_uo_b
    AND uo_beneficiada.cod_orcamentario_uo = tb_tab_repasse_recurso.cod_orcamentario_uo_b
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_grupo_despesa
    ON tb_tab_grupo_despesa.cod_grupo_despesa = tb_tab_repasse_recurso.cod_grupo_despesa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_iag
    ON tb_tab_iag.cod_iag = tb_tab_repasse_recurso.cod_iag
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_grupo_fonte
    ON tb_tab_grupo_fonte.cod_grupo_fonte = tb_tab_repasse_recurso.cod_grupo_fonte
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_fonte
    ON tb_tab_fonte.cod_fonte = tb_tab_repasse_recurso.cod_fonte
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_ipu
    ON tb_tab_ipu.cod_ipu = tb_tab_repasse_recurso.cod_ipu
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_repasse_recurso.status = 'N'
