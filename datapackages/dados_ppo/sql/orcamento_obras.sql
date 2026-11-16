SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_orgao.cod_poder AS BIGINT) AS poder_cod,
    CASE WHEN tb_tab_orgao.cod_poder IN (1, 2, 3) THEN concat('PODER ', tb_tab_poder.descricao)
        ELSE tb_tab_poder.descricao END AS poder_desc,
    CAST(vw_vw_codigo_orgao.codigo_orgao AS BIGINT) AS orgao_cod,
    tb_tab_orgao.descricao AS orgao_nome,
    CAST(tb_tab_acao_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_acao_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_acao_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_sigla,
    tb_tab_unidade_orcamentaria.descricao AS uo_nome,
    CAST(tb_tab_acao_nova.cod_func AS BIGINT) AS funcao_cod,
    tb_tab_funcao.descricao AS funcao_desc,
    CAST(tb_tab_acao_nova.cod_subfuncao AS BIGINT) AS subfuncao_cod,
    tb_tab_subfuncao.descricao AS subfuncao_desc,
    CAST(tb_tab_programa_nova.cod_programa AS BIGINT) AS programa_cod,
    tb_tab_programa_nova.descricao AS programa_desc,
    CAST(tb_tab_acao_nova.cod_tipo_acao AS BIGINT) AS identificador_cod,
    tb_tab_tipo_acao.descricao AS identificador_desc,
    lpad(CAST(CAST(tb_tab_acao_nova.cod_acao AS BIGINT) % 1000 AS STRING), 3, '0') AS projeto_atividade_cod,
    '0001' AS subprojeto_cod,
    CAST(tb_tab_acao_nova.cod_acao AS BIGINT) AS acao_cod,
    tb_tab_acao_nova.desc_aca AS acao_desc,
    CAST(tb_tab_acao_nova.acaiagcod AS BIGINT) AS iag_cod,
    tb_tab_iag.descricao AS iag_desc,
    CAST(tb_tab_detalhamento_obra.cod_detalhamento_obra AS BIGINT) AS obra_cod,
    ROW_NUMBER() OVER (
        ORDER BY
            CAST(tb_tab_acao_nova.cod_administracao_uo AS BIGINT),
            CAST(tb_tab_acao_nova.cod_orgao_uo AS BIGINT),
            CAST(tb_tab_acao_nova.cod_orcamentario_uo AS BIGINT),
            CAST(tb_tab_programa_nova.cod_programa AS BIGINT),
            CAST(tb_tab_acao_nova.cod_acao AS BIGINT),
            CAST(tb_tab_detalhamento_obra.cod_detalhamento_obra AS BIGINT),
            CAST(tb_tab_municipio_detalhamento_obra.cod_localizador AS BIGINT)
    ) AS obra_num,
    tb_tab_detalhamento_obra.descricao AS obra_desc,
    tb_tab_detalhamento_obra.obra_siad,
    CAST(tb_tab_detalhamento_obra.cod_obra AS BIGINT) AS obra_siad_cod,
    tb_tab_detalhamento_obra.situacao AS obra_status,
    CAST(tb_tab_detalhamento_obra.quantidade AS BIGINT) AS obra_quantidade,
    tb_tab_detalhamento_obra.altera_unidade_medida AS unidade_medida_alterar,
    tb_tab_unidade_medida_obra.descricao AS unidade_medida,
    tb_tab_regiao.descricao AS regiao_geografica_intermediaria_desc,
    tb_tab_municipio.descricao AS municipio_desc,
    tb_tab_municipio_detalhamento_obra.valor_tesouro AS vlr_tesouro,
    tb_tab_municipio_detalhamento_obra.valor_outros AS vlr_outros,
    from_timestamp(CAST(tb_tab_municipio_detalhamento_obra.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_municipio_detalhamento_obra
JOIN db_dlseplag_prod_ppo_staging.tb_tab_detalhamento_obra
    ON tb_tab_detalhamento_obra.cod_detalhamento_obra = tb_tab_municipio_detalhamento_obra.cod_detalhamento_obra
JOIN db_dlseplag_prod_ppo_staging.tb_tab_localizador_nova
    ON tb_tab_localizador_nova.cod_localizador = tb_tab_municipio_detalhamento_obra.cod_localizador
JOIN db_dlseplag_prod_ppo_staging.tb_tab_acao_nova
    ON tb_tab_acao_nova.cod_acao_ppag = tb_tab_detalhamento_obra.cod_acao_ppag
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_programa_nova
    ON tb_tab_programa_nova.id_programa = tb_tab_acao_nova.cod_prg
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_funcao
    ON tb_tab_funcao.cod_funcao = tb_tab_acao_nova.cod_func
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_subfuncao
    ON tb_tab_subfuncao.cod_subfuncao = tb_tab_acao_nova.cod_subfuncao
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_tipo_acao
    ON tb_tab_tipo_acao.cod_tipo_acao = tb_tab_acao_nova.cod_tipo_acao
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_iag
    ON tb_tab_iag.cod_iag = tb_tab_acao_nova.acaiagcod
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria
    ON tb_tab_unidade_orcamentaria.cod_administracao_uo = tb_tab_acao_nova.cod_administracao_uo
    AND tb_tab_unidade_orcamentaria.cod_orgao_uo = tb_tab_acao_nova.cod_orgao_uo
    AND tb_tab_unidade_orcamentaria.cod_orcamentario_uo = tb_tab_acao_nova.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_orgao
    ON tb_tab_orgao.cod_seq_orgao = tb_tab_unidade_orcamentaria.cod_seq_orgao
LEFT JOIN db_dlseplag_prod_ppo_staging.vw_vw_codigo_orgao
    ON vw_vw_codigo_orgao.cod_seq_orgao = tb_tab_unidade_orcamentaria.cod_seq_orgao
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_poder
    ON tb_tab_poder.cod_poder = tb_tab_orgao.cod_poder
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_medida_obra
    ON tb_tab_unidade_medida_obra.cod_unidade_medida_obra = tb_tab_detalhamento_obra.cod_unidade_medida
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_municipio
    ON tb_tab_municipio.cod_municipio = tb_tab_localizador_nova.cod_municipio
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_regiao
    ON tb_tab_regiao.cod_regiao = tb_tab_municipio.cod_regiao
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_municipio_detalhamento_obra.status = 'N'
    AND tb_tab_detalhamento_obra.status = 'N'
