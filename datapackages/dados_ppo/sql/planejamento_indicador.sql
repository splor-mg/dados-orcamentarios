WITH justificativa AS (
    SELECT cod_indicador, indice, justificativa
    FROM (
        SELECT
            cod_indicador,
            CAST(indice AS BIGINT) AS indice,
            justificativa,
            ROW_NUMBER() OVER (
                PARTITION BY cod_indicador, CAST(indice AS BIGINT)
                ORDER BY data__cadastro DESC, cod_apu_ind DESC
            ) AS ordem
        FROM db_dlseplag_prod_ppo_staging.tb_tab_apu_ind_jus
    ) justificativas
    WHERE ordem = 1
)
SELECT
    CAST(tb_tx_ppag.ano AS BIGINT) AS ano,
    CAST(tb_tx_ppag.cod_ppag AS BIGINT) AS ppag,
    CAST(tb_tab_programa_nova.cod_administracao_uo AS BIGINT) * 1000
        + CAST(tb_tab_programa_nova.cod_orgao_uo AS BIGINT) * 10
        + CAST(tb_tab_programa_nova.cod_orcamentario_uo AS BIGINT)
        AS uo_programa_cod,
    uo_programa.sigla AS uo_programa_sigla,
    replace(regexp_replace(uo_programa.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS uo_programa_nome,
    replace(regexp_replace(tb_tab_programa_nova.unid_administrativa, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS ua_programa_nome,
    CAST(tb_tab_programa_nova.cod_programa AS BIGINT) AS programa_cod,
    replace(regexp_replace(tb_tab_programa_nova.descricao, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS programa_desc,
    CAST(tb_tab_indicador_nova.cod_ind AS BIGINT) AS indicador_cod,
    replace(regexp_replace(tb_tab_indicador_nova.descricao_ind, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS indicador_desc,
    replace(regexp_replace(tb_tab_indicador_nova.descricao_font, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS fonte_desc,
    replace(regexp_replace(tb_tab_indicador_nova.descricao_form, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS formula_calculo,
    tb_tab_programa_nova.status AS programa_exclusao,
    COALESCE(tb_tab_programa_nova.prgsnovo, 'N') AS programa_novo,
    tb_tab_indicador_nova.status AS indicador_exclusao,
    tb_tab_indicador_nova.ind_novo AS indicador_novo,
    replace(regexp_replace(
        CASE
            WHEN tb_tab_indicador_nova.status = 'S' THEN tb_tab_indicador_nova.justificativa_exclusao
            ELSE tb_tab_indicador_nova.justificativa_inclusao
        END,
        '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS indicador_justificativa_inclusao_exclusao,
    tb_tab_indicador_nova.polaridade,
    tb_tab_periodicidade.descricao AS periodicidade,
    tb_tab_base_geografica.descricao AS base_geografica,
    tb_tab_unidade_medida_ind.descricao AS unidade_medida,
    tb_tab_indicador_nova.ind_vlr_referencia AS indice_referencia,
    tb_tab_indicador_nova.ind_apuracao_referencia AS indice_referencia_apuracao,
    replace(regexp_replace(tb_tab_indicador_nova.justificativa, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS indice_referencia_apuracao_justificativa,
    tb_tab_indicador_nova.data_ind_ref_apuracao AS indice_referencia_data_apuracao,
    tb_tab_indicador_nova.ind_vlr_ano_1 AS previsao_ano0,
    tb_tab_indicador_nova.ind_apuracao_ano_1 AS apuracao_ano0,
    replace(regexp_replace(justificativa_ano0.justificativa, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS previsao_apuracao_justificativa_ano0,
    tb_tab_indicador_nova.ind_vlr_ano_2 AS previsao_ano1,
    tb_tab_indicador_nova.ind_apuracao_ano_2 AS apuracao_ano1,
    replace(regexp_replace(justificativa_ano1.justificativa, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS previsao_apuracao_justificativa_ano1,
    tb_tab_indicador_nova.ind_vlr_ano_3 AS previsao_ano2,
    tb_tab_indicador_nova.ind_apuracao_ano_3 AS apuracao_ano2,
    replace(regexp_replace(justificativa_ano2.justificativa, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS previsao_apuracao_justificativa_ano2,
    tb_tab_indicador_nova.ind_vlr_ano_4 AS previsao_ano3,
    tb_tab_indicador_nova.ind_apuracao_ano_4 AS apuracao_ano3,
    replace(regexp_replace(justificativa_ano3.justificativa, '[\\x00-\\x1f]', ' '), unhex('C2A0'), ' ') AS previsao_apuracao_justificativa_ano3,
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
LEFT JOIN justificativa justificativa_ano0
    ON justificativa_ano0.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND justificativa_ano0.indice = CAST(tb_tx_ppag.ano AS BIGINT) + 0
LEFT JOIN justificativa justificativa_ano1
    ON justificativa_ano1.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND justificativa_ano1.indice = CAST(tb_tx_ppag.ano AS BIGINT) + 1
LEFT JOIN justificativa justificativa_ano2
    ON justificativa_ano2.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND justificativa_ano2.indice = CAST(tb_tx_ppag.ano AS BIGINT) + 2
LEFT JOIN justificativa justificativa_ano3
    ON justificativa_ano3.cod_indicador = tb_tab_indicador_nova.cod_ind
    AND justificativa_ano3.indice = CAST(tb_tx_ppag.ano AS BIGINT) + 3
WHERE tb_tx_ppag.vigente = 'SIM'
    AND tb_tab_programa_nova.status = 'N'
    AND tb_tab_indicador_nova.status = 'N'
ORDER BY programa_cod, indicador_cod
