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
    CAST(tb_tab_orcamento_despesa.cod_categoria AS BIGINT) AS categoria_cod,
    tb_tab_categoria.descricao AS categoria_desc,
    CAST(tb_tab_orcamento_despesa.cod_grupo_despesa AS BIGINT) AS grupo_cod,
    tb_tab_grupo_despesa.descricao AS grupo_desc,
    CAST(tb_tab_orcamento_despesa.cod_modalidade AS BIGINT) AS modalidade_cod,
    tb_tab_modalidade.descricao AS modalidade_desc,
    CAST(tb_tab_orcamento_despesa.cod_elemento_despesa AS BIGINT) AS elemento_cod,
    tb_tab_elemento_despesa.descricao AS elemento_desc,
    CAST(tb_tab_orcamento_despesa.cod_elemento_despesa AS BIGINT) * 100
        + CAST(tb_tab_item_despesa.cod_item_despesa AS BIGINT) AS elemento_item_cod,
    tb_tab_item_despesa.descricao AS elemento_item_desc,
    CAST(tb_tab_orcamento_despesa.cod_fonte AS BIGINT) AS fonte_cod,
    tb_tab_fonte.descricao AS fonte_desc,
    CAST(tb_tab_orcamento_despesa.cod_ipu AS BIGINT) AS ipu_cod,
    tb_tab_ipu.descricao AS ipu_desc,
    tb_tab_orcamento_despesa.valor AS vlr_loa_desp,
    from_timestamp(CAST(tb_tab_orcamento_despesa.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_orcamento_despesa
JOIN db_dlseplag_prod_ppo_staging.tb_tab_item_despesa
    ON tb_tab_item_despesa.id_item_despesa = tb_tab_orcamento_despesa.id_item_despesa
JOIN db_dlseplag_prod_ppo_staging.tb_tab_elemento_despesa
    ON tb_tab_elemento_despesa.cod_elemento_despesa = tb_tab_item_despesa.cod_elemento_despesa
JOIN db_dlseplag_prod_ppo_staging.tb_tab_acao_nova
    ON tb_tab_acao_nova.cod_acao_ppag = tb_tab_orcamento_despesa.cod_acao_ppag
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
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_categoria
    ON tb_tab_categoria.cod_categoria = tb_tab_orcamento_despesa.cod_categoria
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_grupo_despesa
    ON tb_tab_grupo_despesa.cod_grupo_despesa = tb_tab_orcamento_despesa.cod_grupo_despesa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_modalidade
    ON tb_tab_modalidade.cod_modalidade = tb_tab_orcamento_despesa.cod_modalidade
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_fonte
    ON tb_tab_fonte.cod_fonte = tb_tab_orcamento_despesa.cod_fonte
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_ipu
    ON tb_tab_ipu.cod_ipu = tb_tab_orcamento_despesa.cod_ipu
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_orcamento_despesa.status = 'N'
