SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_municipio.cod_municipio AS BIGINT) AS municipio_cod,
    tb_tab_municipio.descricao AS municipio_desc,
    CAST(tb_tab_regiao.cod_ibge AS BIGINT) AS regiao_geografica_intermediaria_cod,
    tb_tab_regiao.descricao AS regiao_geografica_intermediaria_desc,
    from_timestamp(CAST(tb_tab_municipio.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_municipio
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_regiao
    ON tb_tab_regiao.cod_regiao = tb_tab_municipio.cod_regiao
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.vigente = 'SIM'
    AND tb_tab_municipio.status = 'N'
ORDER BY regiao_geografica_intermediaria_cod, municipio_cod
