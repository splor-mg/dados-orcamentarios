SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    concat(
        CAST(CAST(tb_tab_classificacao_receita.cod_categoria AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_origem AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_especie AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_rubrica AS BIGINT) AS STRING),
        lpad(CAST(CAST(tb_tab_classificacao_receita.cod_alinea AS BIGINT) AS STRING), 2, '0'),
        CAST(CAST(tb_tab_classificacao_receita.cod_sub_alinea AS BIGINT) AS STRING),
        CAST(CAST(tb_tab_classificacao_receita.cod_tipo_receita AS BIGINT) AS STRING),
        lpad(CAST(CAST(tb_tab_classificacao_receita.cod_item AS BIGINT) AS STRING), 2, '0'),
        lpad(CAST(CAST(tb_tab_classificacao_receita.cod_sub_item AS BIGINT) AS STRING), 3, '0')
    ) AS receita_cod,
    replace(
        replace(
            regexp_replace(
                replace(tb_tab_classificacao_receita.descricao, ' ¿ ', ' – '),
                '¿(.+?)¿', '“\\1”'
            ),
            '¿', ''
        ),
        unhex('C296'), '–'
    ) AS receita_desc,
    tb_tab_classificacao_receita.nivel_classificacao_receita AS receita_nivel,
    tb_tab_classificacao_receita.vigencia AS receita_vigencia,
    from_timestamp(CAST(tb_tab_classificacao_receita.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_classificacao_receita
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_classificacao_receita.status = 'N'
ORDER BY receita_cod
