SELECT *
FROM (
    SELECT
        CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
        CAST(tb_tab_categoria.cod_categoria AS BIGINT) AS categoria_cod,
        CAST(0 AS BIGINT) AS grupo_cod,
        CAST(0 AS BIGINT) AS modalidade_cod,
        CAST(0 AS BIGINT) AS elemento_cod,
        tb_tab_categoria.descricao AS despesa_desc,
        from_timestamp(CAST(tb_tab_categoria.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
    FROM db_dlseplag_prod_ppo_staging.tb_tab_categoria
    CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
    WHERE tb_tx_ppag.ano = '2027'
        AND tb_tab_categoria.status = 'N'
    UNION ALL
    SELECT
        CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
        CAST(tb_tab_grupo_despesa.cod_categoria AS BIGINT) AS categoria_cod,
        CAST(tb_tab_grupo_despesa.cod_grupo_despesa AS BIGINT) AS grupo_cod,
        CAST(0 AS BIGINT) AS modalidade_cod,
        CAST(0 AS BIGINT) AS elemento_cod,
        tb_tab_grupo_despesa.descricao AS despesa_desc,
        from_timestamp(CAST(tb_tab_grupo_despesa.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
    FROM db_dlseplag_prod_ppo_staging.tb_tab_grupo_despesa
    CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
    WHERE tb_tx_ppag.ano = '2027'
        AND tb_tab_grupo_despesa.status = 'N'
    UNION ALL
    SELECT
        CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
        CAST(tb_tab_natureza_despesa.cod_categoria AS BIGINT) AS categoria_cod,
        CAST(tb_tab_natureza_despesa.cod_grupo AS BIGINT) AS grupo_cod,
        CAST(tb_tab_natureza_despesa.cod_modalidade AS BIGINT) AS modalidade_cod,
        CAST(tb_tab_natureza_despesa.cod_elemento_despesa AS BIGINT) AS elemento_cod,
        min(tb_tab_natureza_despesa.interpretacao) AS despesa_desc,
        from_timestamp(max(CAST(tb_tab_natureza_despesa.data_cadastro AS TIMESTAMP)), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
    FROM db_dlseplag_prod_ppo_staging.tb_tab_natureza_despesa
    CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
    WHERE tb_tx_ppag.ano = '2027'
        AND tb_tab_natureza_despesa.status = 'N'
        AND tb_tab_natureza_despesa.vigencia = 'A'
    GROUP BY
        tb_tx_ppag.ano,
        tb_tab_natureza_despesa.cod_categoria,
        tb_tab_natureza_despesa.cod_grupo,
        tb_tab_natureza_despesa.cod_modalidade,
        tb_tab_natureza_despesa.cod_elemento_despesa
) classificacao
ORDER BY categoria_cod, grupo_cod, modalidade_cod, elemento_cod
