SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tx_ppag.cod_ppag AS BIGINT) AS ppag,
    CAST(tb_tab_programa_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_programa_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_programa_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_programa_cod,
    uo_programa.sigla AS uo_programa_sigla,
    uo_programa.descricao AS uo_programa_nome,
    tb_tab_programa_nova.unid_administrativa AS ua_programa_nome,
    CAST(tb_tab_programa_nova.cod_programa AS BIGINT) AS programa_cod,
    tb_tab_programa_nova.descricao AS programa_desc,
    CAST(tb_tab_indicador_nova.cod_ind AS BIGINT) AS indicador_cod,
    tb_tab_indicador_nova.descricao_ind AS indicador_desc,
    tb_tab_indicador_nova.descricao_font AS fonte_desc,
    tb_tab_indicador_nova.descricao_form AS formula_calculo,
    tb_tab_programa_nova.status AS programa_exclusao,
    tb_tab_programa_nova.prgsnovo AS programa_novo,
    tb_tab_indicador_nova.status AS indicador_exclusao,
    tb_tab_indicador_nova.justificativa_exclusao AS indicador_justificativa_exclusao,
    tb_tab_indicador_nova.ind_novo AS indicador_novo,
    tb_tab_indicador_nova.justificativa_inclusao AS indicador_justificativa_inclusao,
    tb_tab_indicador_nova.polaridade,
    tb_tab_periodicidade.descricao AS periodicidade,
    tb_tab_base_geografica.descricao AS base_geografica,
    tb_tab_unidade_medida_ind.descricao AS unidade_medida,
    tb_tab_indicador_nova.ind_vlr_referencia AS indice_referencia,
    tb_tab_indicador_nova.ind_apuracao_referencia AS indice_referencia_apuracao,
    tb_tab_indicador_nova.justificativa AS indice_referencia_apuracao_justificativa,
    tb_tab_indicador_nova.data_ind_ref_apuracao AS indice_referencia_data_apuracao,
    tb_tab_indicador_nova.ind_vlr_ano_1 AS previsao_ano0,
    tb_tab_indicador_nova.ind_apuracao_ano_1 AS apuracao_ano0,
    justificativa_ano0.justificativa AS previsao_apuracao_justificativa_ano0,
    tb_tab_indicador_nova.ind_vlr_ano_2 AS previsao_ano1,
    tb_tab_indicador_nova.ind_apuracao_ano_2 AS apuracao_ano1,
    justificativa_ano1.justificativa AS previsao_apuracao_justificativa_ano1,
    tb_tab_indicador_nova.ind_vlr_ano_3 AS previsao_ano2,
    tb_tab_indicador_nova.ind_apuracao_ano_3 AS apuracao_ano2,
    justificativa_ano2.justificativa AS previsao_apuracao_justificativa_ano2,
    tb_tab_indicador_nova.ind_vlr_ano_4 AS previsao_ano3,
    tb_tab_indicador_nova.ind_apuracao_ano_4 AS apuracao_ano3,
    justificativa_ano3.justificativa AS previsao_apuracao_justificativa_ano3,
    from_timestamp(CAST(tb_tab_indicador_nova.data_cadastro AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss') AS data_cadastro
FROM db_dlseplag_prod_ppo_staging.tb_tab_indicador_nova
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_programa_nova
    ON tb_tab_programa_nova.id_programa = tb_tab_indicador_nova.cod_prg
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_orcamentaria uo_programa
    ON uo_programa.cod_administracao_uo = tb_tab_programa_nova.cod_administracao_uo
    AND uo_programa.cod_orgao_uo = tb_tab_programa_nova.cod_orgao_uo
    AND uo_programa.cod_orcamentario_uo = tb_tab_programa_nova.cod_orcamentario_uo
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_unidade_medida_ind
    ON tb_tab_unidade_medida_ind.cod_uni_ind = tb_tab_indicador_nova.cod_uni_med_ind
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_periodicidade
    ON tb_tab_periodicidade.cod_per = tb_tab_indicador_nova.cod_per
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_base_geografica
    ON tb_tab_base_geografica.cod_base_geo = tb_tab_indicador_nova.cod_bas_geo
CROSS JOIN db_dlseplag_prod_ppo_staging.tb_tx_ppag
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_apu_ind_jus justificativa_ano0
    ON justificativa_ano0.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND CAST(justificativa_ano0.indice AS BIGINT) = CAST(tb_tx_ppag.ano AS BIGINT) + 0
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_apu_ind_jus justificativa_ano1
    ON justificativa_ano1.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND CAST(justificativa_ano1.indice AS BIGINT) = CAST(tb_tx_ppag.ano AS BIGINT) + 1
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_apu_ind_jus justificativa_ano2
    ON justificativa_ano2.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND CAST(justificativa_ano2.indice AS BIGINT) = CAST(tb_tx_ppag.ano AS BIGINT) + 2
LEFT JOIN db_dlseplag_prod_ppo_staging.tb_tab_apu_ind_jus justificativa_ano3
    ON justificativa_ano3.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND CAST(justificativa_ano3.indice AS BIGINT) = CAST(tb_tx_ppag.ano AS BIGINT) + 3
WHERE tb_tx_ppag.vigente = 'SIM'
    AND NOT (tb_tab_indicador_nova.status = 'S' AND tb_tab_indicador_nova.ind_novo = 'S' AND tb_tab_indicador_nova.validado = 'N')
