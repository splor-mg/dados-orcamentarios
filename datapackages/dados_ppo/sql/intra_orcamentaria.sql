SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tab_despesa_intraorcamentaria.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_despesa_intraorcamentaria.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_despesa_intraorcamentaria.cod_orcamentario_uo AS BIGINT)
        AS uo_beneficiada_cod,
    uo_beneficiada.sigla AS uo_beneficiada_sigla,
    uo_beneficiada.descricao AS uo_beneficiada_nome,
    CAST(tb_tab_acao_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_acao_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_acao_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_repassadora_cod,
    uo_repassadora.sigla AS uo_repassadora_sigla,
    uo_repassadora.descricao AS uo_repassadora_nome,
    CAST(tb_tab_acao_nova.cod_func AS BIGINT) AS funcao_cod,
    tb_tab_funcao.descricao AS funcao_desc,
    CAST(tb_tab_acao_nova.cod_subfuncao AS BIGINT) AS subfuncao_cod,
    tb_tab_subfuncao.descricao AS subfuncao_desc,
    CAST(tb_tab_programa_nova.cod_programa AS BIGINT) AS programa_cod,
    tb_tab_programa_nova.descricao AS programa_desc,
    CAST(tb_tab_acao_nova.cod_acao AS BIGINT) AS acao_cod,
    tb_tab_acao_nova.desc_aca AS acao_desc,
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
    tb_tab_despesa_intraorcamentaria.valor AS vlr_recebido,
    tb_tab_orcamento_despesa.valor AS vlr_detalhado,
    from_timestamp(CAST(tb_tab_despesa_intraorcamentaria.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_despesa_intraorcamentaria
JOIN db_dlseplag_prod_ppo_staging.tb_tab_orcamento_despesa
    ON tb_tab_orcamento_despesa.cod_orcamento_despesa = tb_tab_despesa_intraorcamentaria.cod_orcamento_despesa
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
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_categoria
    ON tb_tab_categoria.cod_categoria = tb_tab_orcamento_despesa.cod_categoria
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_grupo_despesa
    ON tb_tab_grupo_despesa.cod_grupo_despesa = tb_tab_orcamento_despesa.cod_grupo_despesa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_modalidade
    ON tb_tab_modalidade.cod_modalidade = tb_tab_orcamento_despesa.cod_modalidade
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria uo_repassadora
    ON uo_repassadora.cod_administracao_uo = tb_tab_acao_nova.cod_administracao_uo
    AND uo_repassadora.cod_orgao_uo = tb_tab_acao_nova.cod_orgao_uo
    AND uo_repassadora.cod_orcamentario_uo = tb_tab_acao_nova.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria uo_beneficiada
    ON uo_beneficiada.cod_administracao_uo = tb_tab_despesa_intraorcamentaria.cod_administracao_uo
    AND uo_beneficiada.cod_orgao_uo = tb_tab_despesa_intraorcamentaria.cod_orgao_uo
    AND uo_beneficiada.cod_orcamentario_uo = tb_tab_despesa_intraorcamentaria.cod_orcamentario_uo
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
    AND tb_tab_despesa_intraorcamentaria.status = 'N'
    AND tb_tab_orcamento_despesa.status = 'N'
