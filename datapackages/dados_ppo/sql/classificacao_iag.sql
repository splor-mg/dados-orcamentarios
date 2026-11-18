SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_iag.cod_iag AS BIGINT) AS iag_cod,
    tb_tab_iag.descricao AS iag_desc,
    from_timestamp(CAST(tb_tab_iag.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_iag
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.vigente = 'SIM'
    AND tb_tab_iag.status = 'N'
ORDER BY iag_cod
