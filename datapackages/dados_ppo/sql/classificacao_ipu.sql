SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_ipu.cod_ipu AS BIGINT) AS ipu_cod,
    tb_tab_ipu.descricao AS ipu_desc,
    from_timestamp(CAST(tb_tab_ipu.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_ipu
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_ipu.status = 'N'
ORDER BY ipu_cod
