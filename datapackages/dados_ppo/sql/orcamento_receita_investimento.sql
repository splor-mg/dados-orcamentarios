SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_orcamento_receita_investimento.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_orcamento_receita_investimento.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_orcamento_receita_investimento.cod_orcamentario_uo AS BIGINT)
        AS uo_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_sigla,
    tb_tab_unidade_orcamentaria.descricao AS uo_nome,
    CAST(tb_tab_orcamento_receita_investimento.cod_fonte_investimento AS BIGINT) AS fonte_invest_cod,
    tb_tab_fonte_investimento.descricao AS fonte_invest_desc,
    tb_tab_orcamento_receita_investimento.valor AS vlr_loa_rec_invest,
    from_timestamp(CAST(tb_tab_orcamento_receita_investimento.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_orcamento_receita_investimento
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria
    ON tb_tab_unidade_orcamentaria.cod_administracao_uo = tb_tab_orcamento_receita_investimento.cod_administracao_uo
    AND tb_tab_unidade_orcamentaria.cod_orgao_uo = tb_tab_orcamento_receita_investimento.cod_orgao_uo
    AND tb_tab_unidade_orcamentaria.cod_orcamentario_uo = tb_tab_orcamento_receita_investimento.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_fonte_investimento
    ON tb_tab_fonte_investimento.cod_fonte_investimento = tb_tab_orcamento_receita_investimento.cod_fonte_investimento
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.vigente = 'SIM'
    AND tb_tab_orcamento_receita_investimento.status = 'N'
