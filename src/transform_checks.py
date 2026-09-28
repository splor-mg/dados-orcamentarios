import pandas as pd
from pathlib import Path
from datetime import datetime
from frictionless import Package, Resource

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent / 'datapackages' / 'dados_ppo'
DATA_DIR = BASE_DIR / 'data'
CHECK_DIR = BASE_DIR / 'data_check'


# --------------------------------------------------------------------------
# Helpers de leitura (equivalentes ao read_pre() do transform_ppo.py)
# --------------------------------------------------------------------------

def read_txt(name: str) -> pd.DataFrame:
    path = DATA_DIR / f'{name}.txt'
    if not path.exists():
        raise FileNotFoundError(f'Arquivo de origem não encontrado: {path}')
    try:
        df = pd.read_csv(path, sep='|', dtype=str, keep_default_na=False, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep='|', dtype=str, keep_default_na=False, encoding='latin-1')
    return df.apply(lambda col: col.str.strip())


def read_xlsx(name: str) -> pd.DataFrame:
    path = DATA_DIR / f'{name}.xlsx'
    if not path.exists():
        raise FileNotFoundError(f'Arquivo de origem não encontrado: {path}')
    return pd.read_excel(path)


def to_bool(col: pd.Series) -> pd.Series:
    return col.map({'Sim': True, 'Não': False, 'True': True, 'False': False}).astype('boolean')


def check_acoes_planejamento():
    df = read_txt('acoes_planejamento')
    area = df['Código da Área Temática'].str.zfill(2)
    out = pd.DataFrame()
    out['programa_cod'] = pd.to_numeric(df['Código do Programa'], errors='coerce').astype('Int64')
    out['programa_desc'] = df['Nome do Programa']
    out['area_tematica_cod'] = area + 'AT' + area
    out['area_tematica_desc'] = df['Área Temática']
    out['is_deleted_programa'] = to_bool(df['Exclusão Lógica do Programa'])
    out['is_new_programa'] = to_bool(df['Programa Novo'])
    out['justificativa_is_new_programa'] = df['Justificativa de Inclusão ou Exclusão do Programa']
    out['uo_programa_cod'] = pd.to_numeric(df['Código da Unidade Orçamentária Responsável pelo Programa'], errors='coerce').astype('Int64')
    out['uo_programa_nome'] = df['Unidade Orçamentária Responsável pelo Programa']
    out['uo_acao_cod'] = pd.to_numeric(df['Código da Unidade Orçamentária Responsável pela Ação'], errors='coerce').astype('Int64')
    out['uo_acao_nome'] = df['Unidade Orçamentária Responsável pela Ação']
    out['funcao_cod'] = df['Código da Função']
    out['funcao_desc'] = df['Função']
    out['subfuncao_cod'] = df['Código da Subfunção']
    out['subfuncao_desc'] = df['Subfunção']
    out['identificador_tipo_acao_cod'] = df['Código do Tipo de Ação']
    out['identificador_tipo_acao_desc'] = df['Tipo de Ação']
    out['acao_cod'] = pd.to_numeric(df['Código da Ação'], errors='coerce').astype('Int64')
    out['acao_desc'] = df['Título da Ação']
    out['iag_cod'] = df['Código do Identificador de Ação Governamental (IAG)']
    out['iag_desc'] = df['Identificador de Ação Governamental (IAG)']
    out['projeto_estrategico_cod'] = df['Código do Projeto Estratégico']
    out['projeto_estrategico'] = df['Projeto Estratégico']
    out['is_deleted_acao'] = to_bool(df['Exclusão Lógica da Ação'])
    out['is_new_acao'] = to_bool(df['Nova Ação'])
    out['justificativa_is_new_acao'] = df['Justificativa de Inclusão ou Exclusão da Ação']
    out['is_transferida_sisor'] = to_bool(df['Transferida para o SISOR'])
    out['ua_acao_nome'] = df['Unidade Administrativa Responsável pela Ação']
    out['base_legal'] = df['Base legal']
    out['acao_finalidade'] = df['Finalidade da Ação']
    out['acao_descricao'] = df['Descrição da Ação']
    out['publico_alvo_cod'] = df['Código do Público-alvo']
    out['publico_alvo_desc'] = df['Público-Alvo']
    out['produto_cod'] = df['Código do Produto']
    out['produto_desc'] = df['Produto']
    out['produto_especificacao'] = df['Especificação do Produto']
    out['produto_unidade_medida_cod'] = df['Código da Unidade de Medida do Produto']
    out['produto_unidade_medida_desc'] = df['Unidade de Medida do Produto']
    out['vr_meta_orcamentaria_ano0'] = df['Previsão Orçamentária 2027']
    out['vr_meta_orcamentaria_ano1'] = df['Previsão Orçamentária 2028']
    out['vr_meta_orcamentaria_ano2'] = df['Previsão Orçamentária 2029']
    out['vr_meta_orcamentaria_ano3'] = df['Previsão Orçamentária 2030']
    out['vr_meta_fisica_ano0'] = df['Previsão Física 2027']
    out['vr_meta_fisica_ano1'] = df['Previsão Física 2028']
    out['vr_meta_fisica_ano2'] = df['Previsão Física 2029']
    out['vr_meta_fisica_ano3'] = df['Previsão Física 2030']
    out['is_acao_transposta'] = to_bool(df['Ação Transposta'])
    out['setor_governo'] = df['Setor de Governo']
    out['politica_mulheres'] = df['Política para mulheres']
    return out.sort_values(['programa_cod', 'acao_cod'], kind='stable')


def check_indicadores_planejamento():
    df = read_txt('indicadores_planejamento')
    out = pd.DataFrame()
    out['programa_cod'] = pd.to_numeric(df['Código do Programa'], errors='coerce').astype('Int64')
    out['programa_nome'] = df['Nome do Programa']
    out['is_deleted_programa'] = to_bool(df['Exclusão Lógica do Programa'])
    out['indicador'] = df['Indicador']
    out['is_deleted_indicador'] = to_bool(df['Exclusão Lógica do Indicador'])
    out['unidade_de_medida'] = df['Unidade de Medida']
    out['indice_de_referencia'] = df['Índice de Referência']
    out['is_em_apuracao_indice_de_referencia'] = df['Em apuração? (Índice de Referência)'].eq('Em Apuração')
    out['dt_apuracao'] = pd.to_datetime(df['Data de Apuração'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
    out['previsao_para_ano0'] = df['Previsão para 2027']
    out['is_em_apuracao_ano0'] = df['Em apuração? (2027)'].eq('Em Apuração')
    out['previsao_para_ano1'] = df['Previsão para 2028']
    out['is_em_apuracao_ano1'] = df['Em apuração? (2028)'].eq('Em Apuração')
    out['previsao_para_ano2'] = df['Previsão para 2029']
    out['is_em_apuracao_ano2'] = df['Em apuração? (2029)'].eq('Em Apuração')
    out['previsao_para_ano3'] = df['Previsão para 2030']
    out['is_em_apuracao_ano3'] = df['Em apuração? (2030)'].eq('Em Apuração')
    out['fonte'] = df['Fonte']
    out['periodicidade'] = df['Periodicidade']
    out['base_geografica'] = df['Base Geográfica']
    out['formula_de_calculo'] = df['Fórmula de Cálculo']
    out['justificativa_status_apuracao_previsoes'] = df['Justificativa do Status em apuração da(s) Previsão(es) do(s) Índice(s)']
    out['justificativa_status_apuracao_indice_ref'] = df['Justificativa do Status em apuração do Índice de Referência']
    updated_at = pd.to_datetime(df['Data Alteração'], dayfirst=True, errors='coerce')
    out['updated_at'] = updated_at.fillna(pd.Timestamp.now().floor('s')).dt.strftime('%Y-%m-%d %H:%M:%S')
    out['is_indicador_new'] = to_bool(df['Indicador Novo?'])
    out['polaridade'] = df['Polaridade']
    return out.sort_values('programa_cod', kind='stable')


def check_localizadores_todos_planejamento():
    df = read_txt('localizadores_todos_planejamento')
    df = df.drop(columns=['Código do Projeto Estratégico', 'Projeto Estratégico']).drop_duplicates()
    area = df['Código da Área Temática'].str.zfill(2)
    localizador = df['Código do Localizador']
    out = pd.DataFrame()
    out['programa_cod'] = pd.to_numeric(df['Código do Programa'], errors='coerce').astype('Int64')
    out['programa_desc'] = df['Nome do Programa']
    out['area_tematica_cod'] = area + 'AT' + area
    out['area_tematica_desc'] = df['Área Temática']
    out['is_deleted_programa'] = to_bool(df['Exclusão Lógica do Programa'])
    out['acao_cod'] = pd.to_numeric(df['Código da Ação'], errors='coerce').astype('Int64')
    out['acao_desc'] = df['Título da Ação']
    out['iag_cod'] = df['Código do Identificador de Ação Governamental (IAG)']
    out['iag_desc'] = df['Identificador de Ação Governamental (IAG)']
    out['funcao_cod'] = df['Código da Função']
    out['funcao_desc'] = df['Função']
    out['subfuncao_cod'] = df['Código da Subfunção']
    out['subfuncao_desc'] = df['SubFunção']
    out['uo_acao_cod'] = pd.to_numeric(df['Código da Unidade Orçamentária Responsável pela Ação'], errors='coerce').astype('Int64')
    out['uo_acao_nome'] = df['Unidade Orçamentária Responsável pela Ação']
    out['is_deleted_acao'] = to_bool(df['Exclusão Lógica da Ação'])
    out['localizador_cod'] = localizador.where(localizador.ne(''), df['Código do Município Sigplan'])
    out['is_deleted_localizador'] = to_bool(df['Exclusão Lógica do Localizador']).fillna(False)
    out['regiao_geografica_cod'] = df['Código da Região Geográfica Intermediária']
    out['regiao_geografica_desc'] = df['Região Geográfica Intermediária']
    out['municipio_ibge_cod'] = df['Código do Município IBGE']
    out['municipio_sigplan_cod'] = df['Código do Município Sigplan']
    out['municipio'] = df['Município']
    out['vr_meta_orcamentaria_ano0'] = df['Previsão Orçamentária 2027']
    out['vr_meta_fisica_ano0'] = df['Previsão Física 2027']
    out['vr_meta_orcamentaria_ano1'] = df['Previsão Orçamentária 2028']
    out['vr_meta_fisica_ano1'] = df['Previsão Física 2028']
    out['vr_meta_orcamentaria_ano2'] = df['Previsão Orçamentária 2029']
    out['vr_meta_fisica_ano2'] = df['Previsão Física 2029']
    out['vr_meta_orcamentaria_ano3'] = df['Previsão Orçamentária 2030']
    out['vr_meta_fisica_ano3'] = df['Previsão Física 2030']

    chave = ['programa_cod', 'uo_acao_cod', 'acao_cod']
    projetos = check_acoes_planejamento()[chave + ['projeto_estrategico_cod', 'projeto_estrategico']]
    colunas = list(out.columns)
    posicao = colunas.index('iag_desc') + 1
    colunas[posicao:posicao] = ['projeto_estrategico_cod', 'projeto_estrategico_desc']
    out = (
        out.merge(projetos.rename(columns={'projeto_estrategico': 'projeto_estrategico_desc'}), on=chave, how='left')
        [colunas]
    )
    return out.sort_values('programa_cod', kind='stable')


def check_programas_planejamento():
    df = read_txt('programas_planejamento')
    area = df['Código da Área Temática'].str.zfill(2)
    out = pd.DataFrame()
    out['programa_cod'] = pd.to_numeric(df['Código do Programa'], errors='coerce').astype('Int64')
    out['programa_desc'] = df['Nome do Programa']
    out['is_deleted_programa'] = to_bool(df['Exclusão Lógica do Programa'])
    out['is_new_programa'] = to_bool(df['Programa Novo'])
    out['area_tematica_cod'] = area + 'AT' + area
    out['area_tematica_desc'] = df['Área Temática']
    out['objetivo_estrategico_cod'] = df['Código do Objetivo Estratégico']
    out['objetivo_estrategico_desc'] = df['Objetivo Estratégico']
    out['diretriz_estrategica_cod'] = df['Código da Diretriz Estratégica']
    out['diretriz_estrategica_desc'] = df['Diretriz Estratégica']
    out['justificativa_is_new_programa'] = df['Justificativa de Inclusão ou Exclusão do Programa']
    out['orgao_programa_cod'] = pd.to_numeric(df['Código do Órgão Responsável pelo Programa'], errors='coerce').astype('Int64')
    out['orgao_programa_nome'] = df['Órgão Responsável pelo Programa']
    out['uo_programa_cod'] = pd.to_numeric(df['Código da Unidade Orçamentária Responsável pelo Programa'], errors='coerce').astype('Int64')
    out['uo_programa_nome'] = df['Unidade Orçamentária Responsável pelo Programa']
    out['objetivo'] = df['Objetivo']
    out['justificativa'] = df['Justificativa']
    out['tipo_de_programa'] = df['Tipo de Programa']
    out['horizonte_temporal'] = df['Horizonte Temporal']
    out['estrategia_de_implementacao'] = df['Estratégia de Implementação']
    out['ua_programa_nome'] = df['Unidade Administrativa Responsável pelo Programa']
    out['vr_meta_orcamentaria_ano0'] = df['Previsão Orçamentária 2027']
    out['vr_meta_orcamentaria_ano1'] = df['Previsão Orçamentária 2028']
    out['vr_meta_orcamentaria_ano2'] = df['Previsão Orçamentária 2029']
    out['vr_meta_orcamentaria_ano3'] = df['Previsão Orçamentária 2030']
    out['is_programa_transposto'] = to_bool(df['Programa Transposto'])
    out['causas'] = df['Causas']
    out['ods_titulo'] = df['Título do Objetivo de Desenvolvimento Sustentável']
    out['ods_subtitulo'] = df['Subtítulo do Objetivo de Desenvolvimento Sustentável']

    colunas = list(out.columns)
    chaves = [col for col in colunas if col != 'causas']
    out = (
        out.groupby(chaves, sort=False, dropna=False)['causas']
        .agg(lambda causas: ''.join(f'{causa} / ' for causa in dict.fromkeys(causas) if causa))
        .reset_index()[colunas]
    )
    return out.sort_values('programa_cod', kind='stable')


def check_base_orcam_despesa_item_fiscal():
    df = read_xlsx('BASE_ORCAM_DESPESA_ITEM_FISCAL')
    out = pd.DataFrame()
    out['orgao_cod'] = df['Código do Órgão']
    out['orgao_nome_sigla'] = df['Órgão']
    out['uo_cod'] = df['Código da UO']
    out['uo_nome_sigla'] = df['Unidade Orçamentária']
    out['funcao_cod'] = df['Função']
    out['subfuncao_cod'] = df['Subfunção']
    out['programa_cod'] = df['Programa']
    out['identificador_tipo_acao_cod'] = df['Identificador']
    out['projeto_atividade_cod'] = df['Projeto_Atividade']
    out['acao_cod'] = df['Ação']
    out['subprojeto_subatividade_cod'] = df['Subprojeto']
    out['categoria_cod'] = df['Categoria']
    out['grupo_cod'] = df['Grupo_Despesa']
    out['modalidade_cod'] = df['Modalidade']
    out['elemento_cod'] = df['Elemento_Despesa']
    out['item_cod'] = df['Item_Despesa']
    out['fonte_cod'] = df['Fonte']
    out['ipu_cod'] = df['IPU']
    out['iag_cod'] = df['IAG']
    out['acao_desc'] = df['Descrição']
    out['vlr_loa_desp'] = df['Valor (R$)']
    return out


def check_base_orcam_despesa_investimento():
    df = read_xlsx('BASE_ORCAM_DESPESA_INVESTIMENTO')
    out = pd.DataFrame()
    out['orgao_cod'] = df['Código do Órgão']
    out['orgao_nome_sigla'] = df['Órgão']
    out['uo_cod'] = df['Código da UO']
    out['uo_nome_sigla'] = df['Unidade Orçamentária']
    out['funcao_cod'] = df['Função']
    out['subfuncao_cod'] = df['Subfunção']
    out['programa_cod'] = df['Programa']
    out['identificador'] = df['Identificador']
    out['projeto_atividade'] = df['Projeto_Atividade']
    out['acao_cod'] = df['Ação']
    out['subprojeto_cod'] = df['Subprojeto']
    out['fonte_cod'] = df['Fonte']
    out['iag_cod'] = df['IAG']
    out['descricao'] = df['Descrição']
    out['categoria_cod'] = df['Categoria']
    out['natureza_cod'] = df['Código da Natureza']
    out['natureza'] = df['Natureza']
    out['vlr_loa_desp_invest_ano0'] = df['Valor (R$)\xa02027']
    out['vlr_loa_desp_invest_ano1'] = df['Valor (R$)\xa02028']
    out['vlr_loa_desp_invest_ano2'] = df['Valor (R$)\xa02029']
    out['vlr_loa_desp_invest_ano3'] = df['Valor (R$)\xa02030']
    return out


def check_base_detalhamento_obras():
    df = read_xlsx('BASE_DETALHAMENTO_OBRAS')
    out = pd.DataFrame()
    out['uo_cod'] = df['UO']
    out['funcao_cod'] = df['FUNCAO']
    out['subfuncao_cod'] = df['SUBFUNCAO']
    out['programa_cod'] = df['PROGRAMA']
    out['acao_cod'] = df['ACAO']
    out['subprojeto_subatividade_cod'] = df['SUBPROJETO']
    out['iag_cod'] = df['IAG']
    out['numero_da_obra_sisor'] = df['NUMERO DA OBRA SISOR']
    out['numero_da_obra_siad'] = pd.to_numeric(df['NUMERO DA OBRA SIAD'], errors='coerce').astype('Int64')
    out['descricao_da_obra'] = df['DESCRICAO DA OBRA']
    out['status_da_obra'] = df['STATUS DA OBRA']
    out['unidade_de_medida_da_obra'] = df['UNIDADE DE MEDIDA DA OBRA']
    out['quantidade'] = pd.to_numeric(df['QUANTIDADE'], errors='coerce').astype('Int64')
    out['alterar_unidade_de_medida_da_obra'] = df['ALTERAR UNIDADE DE MEDIDA DA OBRA']
    out['regiao_geografica_intermediaria'] = df['REGIÃO GEOGRÁFICA INTERMEDIÁRIA']
    out['municipio'] = df['MUNICÍPIO']
    out['vlr_tesouro_ano0'] = df['VALOR TESOURO 2027 (R$)']
    out['vlr_outros_ano0'] = df['VALOR OUTROS 2027 (R$)']
    out['vlr_tesouro_ano1'] = df['VALOR TESOURO 2028 (R$)']
    out['vlr_outros_ano1'] = df['VALOR OUTROS 2028 (R$)']
    out['vlr_tesouro_ano2'] = df['VALOR TESOURO 2029 (R$)']
    out['vlr_outros_ano2'] = df['VALOR OUTROS 2029 (R$)']
    out['vlr_tesouro_ano3'] = df['VALOR TESOURO 2030 (R$)']
    out['vlr_outros_ano3'] = df['VALOR OUTROS 2030 (R$)']
    return out


def check_base_qdd_fiscal():
    df = read_xlsx('BASE_QDD_FISCAL')
    out = pd.DataFrame()
    out['ano'] = df['ANO']
    out['orgao_cod'] = df['COD_ORGAO']
    out['orgao_nome_sigla'] = df['ORGAO']
    out['poder_cod'] = df['PODER']
    out['situacao'] = df['SITUACAO']
    out['uo_cod'] = df['COD_UO']
    out['uo_nome_sigla'] = df['UO']
    out['categoria_cod'] = df['CATEGORIA']
    out['grupo_cod'] = df['GRUPO_DESPESA']
    out['modalidade_cod'] = df['MODALIDADE']
    out['elemento_cod'] = df['ELEMENTO_DESPESA']
    out['fonte_cod'] = df['FONTE']
    out['ipu_cod'] = df['IPU']
    out['seq_progtrab'] = df['SEQ_PROGTRAB']
    out['funcao_cod'] = df['FUNCAO']
    out['subfuncao_cod'] = df['SUB_FUNCAO']
    out['programa_cod'] = df['PROGRAMA']
    out['identificador_tipo_acao_cod'] = df['IDENT_PROJATIV']
    out['projeto_atividade_cod'] = df['PROJ_ATIV']
    out['acao_cod'] = df['AÇÃO']
    out['subprojeto_subatividade_cod'] = df['SUB_PROJETO']
    out['vlr_loa_desp_uo'] = df['VALOR UO (R$)']
    out['vlr_loa_desp_scppo'] = df['VALOR SCPPO (R$)']
    out['vlr_loa_desp'] = df['VALOR FINAL (R$)']
    out['iag_cod'] = df['IAG']
    out['acao_desc'] = df['NOME_ACAO']
    out['programa_desc'] = df['NOME_PROGRAMA']
    return out


def check_base_qdd_investimento():
    df = read_xlsx('BASE_QDD_INVESTIMENTO')
    out = pd.DataFrame()
    out['ano'] = df['ANO']
    out['orgao_cod'] = df['COD_ORGAO']
    out['orgao_nome_sigla'] = df['ORGAO']
    out['poder_cod'] = df['PODER']
    out['uo_cod'] = df['COD_UO']
    out['uo_nome_sigla'] = df['UO']
    out['seq_progtrab'] = df['SEQ_PROGTRAB']
    out['funcao_cod'] = df['FUNCAO']
    out['subfuncao_cod'] = df['SUB_FUNCAO']
    out['programa_cod'] = df['PROGRAMA']
    out['ident_projativ'] = df['IDENT_PROJATIV']
    out['proj_ativ'] = df['PROJ_ATIV']
    out['acao_cod'] = df['AÇÃO']
    out['vlr_loa_desp_invest'] = df['VALOR (R$)']
    out['iag_cod'] = df['IAG']
    out['desc_projeto_ativ'] = df['DESC_PROJETO_ATIV']
    out['categoria_cod'] = df['CATEGORIA']
    out['natureza_cod'] = df['COD_NATUREZA']
    out['natureza'] = df['NATUREZA']
    out['fonte_cod'] = df['COD_FONTE']
    out['fonte'] = df['FONTE']
    out['acao_desc'] = df['NOME_ACAO']
    out['programa_desc'] = df['NOME_PROGRAMA']
    return out


def check_base_orcam_receita_fiscal():
    df = read_xlsx('BASE_ORCAM_RECEITA_FISCAL')
    out = pd.DataFrame()
    out['uo_cod'] = df['UO_COD']
    out['nome_uo'] = df['NOME_UO']
    out['uo_sigla'] = df['SIGLA_UO']
    out['fonte_cod'] = df['COD_FONTE']
    out['fonte_desc'] = df['FONTE']
    out['interpretacao'] = df['INTERPRETACAO']
    out['categoria'] = df['CATEGORIA']
    out['origem'] = df['ORIGEM']
    out['especie'] = df['ESPECIE']
    out['rubrica'] = df['RUBRICA']
    out['alinea'] = df['ALINEA']
    out['subalinea'] = df['SUBALINEA']
    out['tipo_receita'] = df['TIPO_RECEITA']
    out['item'] = df['ITEM']
    out['subitem'] = df['SUBITEM']
    out['receita_cod'] = df['COD_RECEITA']
    out['receita_desc'] = df['RECEITA']
    out['interp_receita'] = df['INTERP_RECEITA']
    out['vlr_loa_rec_uo'] = df['VALOR UO (R$)']
    out['vlr_loa_rec_scppo'] = df['VALOR SCPPO (R$)']
    out['vlr_loa_rec'] = df['VALOR FINAL (R$)']
    out['ano'] = df['ANO']
    out['base_legal'] = df['BASE LEGAL']
    out['metodologia_de_calculo_e_premissas_utilizadas'] = df['METODOLOGIA DE CÁLCULO E PREMISSAS UTILIZADAS']
    return out


def check_base_orcam_receita_investimento():
    df = read_xlsx('BASE_ORCAM_RECEITA_INVESTIMENTO')
    out = pd.DataFrame()
    out['uo_cod'] = df['COD_UO']
    out['uo_nome'] = df['NOME_UO']
    out['uo_sigla'] = df['SIGLA_UO']
    out['categoria'] = df['CATEGORIA']
    out['subcategoria'] = df['SUBCATEGORIA']
    out['alinea'] = df['ALINEA']
    out['subalinea'] = df['SUBALINEA']
    out['cod_receita'] = df['COD_RECEITA']
    out['nivel_origem'] = df['NIVEL_ORIGEM']
    out['receita'] = df['RECEITA']
    out['vlr_loa_rec_uo_invest'] = df['VALOR UO (R$)']
    out['vlr_loa_rec_scppo_invest'] = df['VALOR SCPPO (R$)']
    out['vlr_loa_rec_invest'] = df['VALOR FINAL (R$)']
    out['ano'] = df['ANO']
    return out


def check_base_categoria_pessoal():
    df = read_xlsx('BASE_CATEGORIA_PESSOAL')
    out = pd.DataFrame()
    out['ano'] = df['Ano de Exercício']
    out['uo_cod_sigla'] = df['UO']
    out['classificacao'] = df['Classificação']
    out['categoria'] = df['Categoria']
    out['quantidade'] = df['Quantidade']
    return out


def check_base_repasse_recursos():
    df = read_xlsx('BASE_REPASSE_RECURSOS')
    out = pd.DataFrame()
    out['uo_financiadora_cod'] = df['Cód. UO Financiadora']
    out['uo_financiadora_nome'] = df['UO Financiadora']
    out['uo_beneficiada_cod'] = df['Cód. UO Beneficiada']
    out['uo_beneficiada_nome'] = df['UO Beneficiada']
    out['grupo_cod'] = df['Grupo de Despesa']
    out['fonte_cod'] = df['Fonte']
    out['ipu_cod'] = df['IPU']
    out['iag_cod'] = df['IAG']
    out['vlr_repasse'] = df['Valor Transferido (R$)']
    return out


def check_base_limite_cota():
    df = read_xlsx('BASE_LIMITE_COTA')
    out = pd.DataFrame()
    out['uo_cod'] = df['Cód. UO']
    out['uo'] = df['UO']
    out['grupo_cod'] = df['Grupo de Despesa']
    out['fonte_cod'] = df['Fonte']
    out['ipu_cod'] = df['IPU']
    out['iag_cod'] = df['IAG']
    out['vlr_limite_ano0'] = df['Valor Limite\xa02027']
    out['vlr_utilizado_ano0'] = df['Valor Utilizado\xa02027']
    out['vlr_transferido'] = df['Valor Transferido']
    out['vlr_limite_ano1'] = df['Valor Limite\xa02028']
    out['vlr_utilizado_ano1'] = df['Valor Utilizado\xa02028']
    out['vlr_limite_ano2'] = df['Valor Limite\xa02029']
    out['vlr_utilizado_ano2'] = df['Valor Utilizado\xa02029']
    out['vlr_limite_ano3'] = df['Valor Limite\xa02030']
    out['vlr_utilizado_ano3'] = df['Valor Utilizado\xa02030']
    return out


def check_base_intra_orcamentaria_detalhamento():
    df = read_xlsx('BASE_INTRA_ORCAMENTARIA_DETALHAMENTO')
    out = pd.DataFrame()
    out['uo_cod'] = df['Cód. UO Beneficiada']
    out['uo_sigla'] = df['UO Beneficiada']
    out['vlr_recebido'] = df['Valor Recebido (R$)']
    out['vlr_detalhado'] = df['Valor Detalhado (R$)']
    return out


def check_base_intra_orcamentaria_repasse():
    df = read_xlsx('BASE_INTRA_ORCAMENTARIA_REPASSE')
    out = pd.DataFrame()
    out['uo_repassadora_cod'] = df['Cód. UO Repassadora']
    out['uo_repassadora_sigla'] = df['UO Repassadora']
    out['programa_trabalho_fmt'] = df['Cód. Programa de Trabalho'].str.split().str.join('\u00a0')
    out['acao_desc'] = df['Ação']
    out['natureza_desp_fmt'] = df['Cód. Natureza de Despesa'].str.split().str.join('\u00a0')
    out['item_desc'] = df['Elemento Item']
    out['vlr_repassado'] = df['Valor Repassado (R$)']
    out['uo_beneficiada_cod'] = df['Cód. UO Beneficiada']
    out['uo_beneficiada_sigla'] = df['UO Beneficiada']
    return out


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

CHECKS = {
    'acoes_planejamento': check_acoes_planejamento,
    'indicadores_planejamento': check_indicadores_planejamento,
    'localizadores_todos_planejamento': check_localizadores_todos_planejamento,
    'programas_planejamento': check_programas_planejamento,
    'base_orcam_despesa_item_fiscal': check_base_orcam_despesa_item_fiscal,
    'base_orcam_despesa_investimento': check_base_orcam_despesa_investimento,
    'base_detalhamento_obras': check_base_detalhamento_obras,
    'base_qdd_fiscal': check_base_qdd_fiscal,
    'base_qdd_investimento': check_base_qdd_investimento,
    'base_orcam_receita_fiscal': check_base_orcam_receita_fiscal,
    'base_orcam_receita_investimento': check_base_orcam_receita_investimento,
    'base_categoria_pessoal': check_base_categoria_pessoal,
    'base_repasse_recursos': check_base_repasse_recursos,
    'base_limite_cota': check_base_limite_cota,
    'base_intra_orcamentaria_detalhamento': check_base_intra_orcamentaria_detalhamento,
    'base_intra_orcamentaria_repasse': check_base_intra_orcamentaria_repasse,
}

SIGPLAN_RESOURCES = {
    'acoes_planejamento',
    'indicadores_planejamento',
    'localizadores_todos_planejamento',
    'programas_planejamento',
}


def build_resource_descriptor(file_path: Path) -> dict:
    name = file_path.stem.lower()

    resource = Resource.from_descriptor({
        'name': name,
        'path': file_path.name,
        'format': 'csv',
    }, basepath=str(CHECK_DIR))
    resource.infer(stats=True)

    descriptor = resource.to_dict()
    descriptor.setdefault('profile', 'tabular-data-resource')
    descriptor.setdefault('scheme', 'file')
    descriptor.setdefault('mediatype', 'text/csv')
    descriptor.setdefault('encoding', 'utf-8')
    descriptor['title'] = name
    descriptor['path'] = f'data/{file_path.name}'
    return descriptor


def build_package(name: str, title: str, resource_descriptors: list) -> Package:
    target_descriptor = {
        'profile': 'tabular-data-package',
        'name': name,
        'title': title,
        'resources': resource_descriptors,
    }
    target = Package.from_descriptor(target_descriptor, basepath=str(BASE_DIR))
    target.custom['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    return target


def build_datapackages():
    csv_files = sorted(CHECK_DIR.glob('*.csv'))

    sigplan_resources = []
    sisor_resources = []
    for file_path in csv_files:
        name = file_path.stem.lower()
        descriptor = build_resource_descriptor(file_path)
        if name in SIGPLAN_RESOURCES:
            sigplan_resources.append(descriptor)
        else:
            sisor_resources.append(descriptor)

    sigplan = build_package('dados_sigplan_2027', 'Planejamento - SIGPLAN', sigplan_resources)
    sigplan_path = CHECK_DIR / 'datapackage_sigplan.json'
    sigplan.to_json(str(sigplan_path))
    print(f'OK  datapackage_sigplan.json  ({len(sigplan.resources)} resources) -> {sigplan_path}')

    sisor = build_package('dados_sisor_2027', 'Orçamento - SISOR', sisor_resources)
    sisor_path = CHECK_DIR / 'datapackage_sisor.json'
    sisor.to_json(str(sisor_path))
    print(f'OK  datapackage_sisor.json  ({len(sisor.resources)} resources) -> {sisor_path}')


def main():
    CHECK_DIR.mkdir(parents=True, exist_ok=True)

    for name, fn in CHECKS.items():
        try:
            df = fn()
        except FileNotFoundError as e:
            print(f'[AVISO] Pulando {name}: {e}')
            continue

        dest = CHECK_DIR / f'{name}.csv'
        df.to_csv(dest, index=False, encoding='utf-8')
        print(f'OK  {dest.name}  ({len(df)} linhas, {len(df.columns)} colunas) -> {dest}')

    build_datapackages()


if __name__ == '__main__':
    main()
