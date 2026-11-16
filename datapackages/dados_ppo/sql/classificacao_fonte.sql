SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_fonte.cod_fonte AS BIGINT) AS fonte_cod,
    tb_tab_fonte.descricao AS fonte_desc,
    from_timestamp(CAST(tb_tab_fonte.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_fonte
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_fonte.status = 'N'
ORDER BY fonte_cod
