SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tx_ppag.cod_ppag AS BIGINT) AS ppag,
    CAST(tb_tab_programa_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_programa_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_programa_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_programa_cod,
    uo_programa.sigla AS uo_programa_sigla,
    replace(regexp_replace(uo_programa.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS uo_programa_nome,
    CAST(tb_tab_orgao.cod_poder AS BIGINT) AS poder_cod,
    tb_tab_poder.descricao AS poder_desc,
    tb_tab_setor.descricao AS governo_setor,
    CAST(vw_vw_codigo_orgao.codigo_orgao AS BIGINT) AS orgao_cod,
    tb_tab_orgao.descricao AS orgao_nome,
    CAST(tb_tab_acao_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_acao_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_acao_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_acao_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_acao_sigla,
    replace(regexp_replace(tb_tab_unidade_orcamentaria.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS uo_acao_nome,
    replace(regexp_replace(tb_tab_acao_nova.acaobs, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS ua_acao_nome,
    CAST(tb_tab_area_tematica_programa.cod_area_tematica AS BIGINT) AS area_tematica_cod,
    tb_tab_area_tematica.descricao AS area_tematica_desc,
    CAST(tb_tab_acao_nova.cod_func AS BIGINT) AS funcao_cod,
    tb_tab_funcao.descricao AS funcao_desc,
    CAST(tb_tab_acao_nova.cod_subfuncao AS BIGINT) AS subfuncao_cod,
    tb_tab_subfuncao.descricao AS subfuncao_desc,
    CAST(tb_tab_programa_nova.cod_programa AS BIGINT) AS programa_cod,
    replace(regexp_replace(tb_tab_programa_nova.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS programa_desc,
    CAST(tb_tab_acao_nova.cod_tipo_acao AS BIGINT) AS identificador_cod,
    tb_tab_tipo_acao.descricao AS identificador_desc,
    CAST(tb_tab_acao_nova.cod_acao AS BIGINT) AS acao_cod,
    replace(regexp_replace(tb_tab_acao_nova.desc_aca, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS acao_desc,
    CAST(tb_tab_acao_nova.acaiagcod AS BIGINT) AS iag_cod,
    tb_tab_iag.descricao AS iag_desc,
    tb_tab_programa_nova.status AS programa_exclusao,
    COALESCE(tb_tab_programa_nova.prgsnovo, 'N') AS programa_novo,
    replace(regexp_replace(
        CASE
            WHEN tb_tab_programa_nova.status = 'S' THEN tb_tab_programa_nova.justificativa_exclusao
            ELSE tb_tab_programa_nova.justificativa_inclusao
        END,
        '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS programa_justificativa_inclusao_exclusao,
    tb_tab_acao_nova.status AS acao_exclusao,
    tb_tab_acao_nova.acasnnova AS acao_novo,
    replace(regexp_replace(
        CASE
            WHEN tb_tab_acao_nova.status = 'S' THEN tb_tab_acao_nova.justificativa_exclusao
            ELSE tb_tab_acao_nova.justificativa_inclusao
        END,
        '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS acao_justificativa_inclusao_exclusao,
    replace(regexp_replace(tb_tab_projeto_estrategico.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS projeto_estrategico,
    replace(regexp_replace(tb_tab_publico_alvo.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS publico_alvo,
    replace(regexp_replace(tb_tab_produto.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS produto,
    replace(regexp_replace(tb_tab_acao_nova.aca_desc_produto, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS produto_especificacao,
    tb_tab_unidade_medidas.desc_unid_medida AS unidade_medida,
    tb_tab_politica_mulher.descricao AS politica_mulheres,
    replace(regexp_replace(tb_tab_acao_nova.desc_finalidade, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS acao_finalidade,
    replace(regexp_replace(tb_tab_acao_nova.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS acao_descricao,
    replace(regexp_replace(tb_tab_acao_nova.base_legal, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS base_legal,
    vw_vw_valores_acao.qtde_ano1 AS vlr_meta_fisica_ano0,
    vw_vw_valores_acao.qtde_ano2 AS vlr_meta_fisica_ano1,
    vw_vw_valores_acao.qtde_ano3 AS vlr_meta_fisica_ano2,
    vw_vw_valores_acao.qtde_ano4 AS vlr_meta_fisica_ano3,
    vw_vw_valores_acao.vlr_custo_ano1 AS vlr_meta_orcamentaria_ano0,
    vw_vw_valores_acao.vlr_custo_ano2 AS vlr_meta_orcamentaria_ano1,
    vw_vw_valores_acao.vlr_custo_ano3 AS vlr_meta_orcamentaria_ano2,
    vw_vw_valores_acao.vlr_custo_ano4 AS vlr_meta_orcamentaria_ano3,
    from_timestamp(CAST(tb_tab_acao_nova.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_acao_nova
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
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_setor
    ON tb_tab_setor.cod_setor = tb_tab_orgao.cod_setor
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_area_tematica_programa
    ON tb_tab_area_tematica_programa.cod_prg = tb_tab_programa_nova.id_programa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_area_tematica
    ON tb_tab_area_tematica.cod_area_tematica = tb_tab_area_tematica_programa.cod_area_tematica
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria uo_programa
    ON uo_programa.cod_administracao_uo = tb_tab_programa_nova.cod_administracao_uo
    AND uo_programa.cod_orgao_uo = tb_tab_programa_nova.cod_orgao_uo
    AND uo_programa.cod_orcamentario_uo = tb_tab_programa_nova.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_projeto_estrategico
    ON tb_tab_projeto_estrategico.cod_projeto_estrategico = tb_tab_acao_nova.acaprojetoestrategico
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_publico_alvo
    ON tb_tab_publico_alvo.cod_publico_alvo = tb_tab_acao_nova.acapacod
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_politica_mulher
    ON tb_tab_politica_mulher.cod_pol_mulher = tb_tab_acao_nova.polmulhercod
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_produto
    ON tb_tab_produto.cod_produto = tb_tab_acao_nova.cod_produto
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_medidas
    ON tb_tab_unidade_medidas.cod_unidade_medida = tb_tab_acao_nova.cod_unid_medida
LEFT JOIN db_dlseplag_prod_ppo_staging.vw_vw_valores_acao
    ON vw_vw_valores_acao.cod_acao_ppag = tb_tab_acao_nova.cod_acao_ppag
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.vigente = 'SIM'
    AND NOT (tb_tab_acao_nova.status = 'S' AND tb_tab_acao_nova.acasnnova = 'S' AND tb_tab_acao_nova.validado = 'N')
ORDER BY programa_cod, uo_acao_cod, acao_cod
