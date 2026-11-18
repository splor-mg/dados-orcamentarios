SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_categoria_invest.cod_categoria_invest AS BIGINT) AS categoria_invest_cod,
    tb_tab_categoria_invest.descricao AS categoria_invest_desc,
    CAST(tb_tab_natureza_invest.cod_natureza_invest AS BIGINT) AS natureza_invest_cod,
    tb_tab_natureza_invest.descricao AS natureza_invest_desc,
    from_timestamp(CAST(tb_tab_natureza_invest.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_natureza_invest
JOIN db_dlseplag_prod_ppo_staging.tb_tab_categoria_invest
    ON tb_tab_categoria_invest.cod_categoria_invest = tb_tab_natureza_invest.cod_categoria
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.vigente = 'SIM'
    AND tb_tab_categoria_invest.status = 'N'
    AND tb_tab_natureza_invest.status = 'N'
