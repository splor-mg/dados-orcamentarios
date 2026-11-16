SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tx_ppag.cod_ppag AS BIGINT) AS ppag,
    CAST(tb_tab_orgao.cod_poder AS BIGINT) AS poder_cod,
    tb_tab_poder.descricao AS poder_desc,
    CAST(vw_vw_codigo_orgao.codigo_orgao AS BIGINT) AS orgao_cod,
    tb_tab_orgao.descricao AS orgao_nome,
    CAST(tb_tab_programa_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_programa_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_programa_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_cod,
    tb_tab_unidade_orcamentaria.sigla AS uo_sigla,
    tb_tab_unidade_orcamentaria.descricao AS uo_nome,
    tb_tab_programa_nova.unid_administrativa AS ua_programa_nome,
    CAST(tb_tab_programa_nova.cod_programa AS BIGINT) AS programa_cod,
    tb_tab_programa_nova.descricao AS programa_desc,
    CAST(tb_tab_area_tematica_programa.cod_area_tematica AS BIGINT) AS area_tematica_cod,
    tb_tab_area_tematica.descricao AS area_tematica_desc,
    tb_tab_programa_nova.status AS programa_exclusao,
    tb_tab_programa_nova.justificativa_exclusao AS programa_justificativa_exclusao,
    tb_tab_programa_nova.prgsnovo AS programa_novo,
    tb_tab_programa_nova.justificativa_inclusao AS programa_justificativa_inclusao,
    tb_tab_tipo_programa.descricao AS tipo_de_programa,
    tb_tab_horizonte_temporal.descricao AS horizonte_temporal,
    CAST(tb_tab_obj_des_sustentavel_prg.cod_obj_des_sus AS BIGINT) AS ods_cod,
    tb_tab_obj_desenv_sustentavel.titulo AS ods_titulo,
    tb_tab_obj_desenv_sustentavel.subtitulo AS ods_subtitulo,
    tb_tab_objetivo_estrategico_nova.descricao AS objetivo_estrategico,
    tb_tab_diretriz.descricao AS diretriz_estrategica,
    tb_tab_programa_nova.desc_estrategia AS estrategia_implementacao,
    tb_tab_programa_nova.objetivo AS programa_objetivo,
    tb_tab_programa_nova.justificativa_programa AS programa_justificativa,
    tb_tab_causa.descricao AS causas,
    vw_vw_valores_programa.vlr_custo_ano1 AS vlr_meta_orcamentaria_ano0,
    vw_vw_valores_programa.vlr_custo_ano2 AS vlr_meta_orcamentaria_ano1,
    vw_vw_valores_programa.vlr_custo_ano3 AS vlr_meta_orcamentaria_ano2,
    vw_vw_valores_programa.vlr_custo_ano4 AS vlr_meta_orcamentaria_ano3,
    from_timestamp(CAST(tb_tab_programa_nova.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_programa_nova
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria
    ON tb_tab_unidade_orcamentaria.cod_administracao_uo = tb_tab_programa_nova.cod_administracao_uo
    AND tb_tab_unidade_orcamentaria.cod_orgao_uo = tb_tab_programa_nova.cod_orgao_uo
    AND tb_tab_unidade_orcamentaria.cod_orcamentario_uo = tb_tab_programa_nova.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_orgao
    ON tb_tab_orgao.cod_seq_orgao = tb_tab_unidade_orcamentaria.cod_seq_orgao
LEFT JOIN db_dlseplag_prod_ppo_staging.vw_vw_codigo_orgao
    ON vw_vw_codigo_orgao.cod_seq_orgao = tb_tab_unidade_orcamentaria.cod_seq_orgao
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_poder
    ON tb_tab_poder.cod_poder = tb_tab_orgao.cod_poder
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_area_tematica_programa
    ON tb_tab_area_tematica_programa.cod_prg = tb_tab_programa_nova.id_programa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_area_tematica
    ON tb_tab_area_tematica.cod_area_tematica = tb_tab_area_tematica_programa.cod_area_tematica
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_tipo_programa
    ON tb_tab_tipo_programa.cod_tipo_programa = tb_tab_programa_nova.cod_tipo_prog
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_horizonte_temporal
    ON tb_tab_horizonte_temporal.cod_horiz_temporal = tb_tab_programa_nova.cod_horizonte_temp
LEFT JOIN db_dlseplag_prod_ppo_staging.vw_vw_valores_programa
    ON vw_vw_valores_programa.id_programa = tb_tab_programa_nova.id_programa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_obj_des_sustentavel_prg
    ON tb_tab_obj_des_sustentavel_prg.cod_prg = tb_tab_programa_nova.id_programa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_obj_desenv_sustentavel
    ON tb_tab_obj_desenv_sustentavel.cod_obj_des_sus = tb_tab_obj_des_sustentavel_prg.cod_obj_des_sus
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_obj_estra_programa_nova
    ON tb_tab_obj_estra_programa_nova.cod_prg = tb_tab_programa_nova.id_programa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_objetivo_estrategico_nova
    ON tb_tab_objetivo_estrategico_nova.cod_obj_estrategico = tb_tab_obj_estra_programa_nova.cod_obj_est
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_diretriz_programa
    ON tb_tab_diretriz_programa.cod_prg = tb_tab_programa_nova.id_programa
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_diretriz
    ON tb_tab_diretriz.cod_diretriz = tb_tab_diretriz_programa.cod_diretriz
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_causa
    ON tb_tab_causa.cod_prg = tb_tab_programa_nova.id_programa
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
WHERE tb_tx_ppag.ano = '2027'
