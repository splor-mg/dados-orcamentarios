import re
import pandas as pd
from pathlib import Path
from datetime import datetime
from frictionless import Package, Resource

BASE_DIR = Path(__file__).resolve().parent.parent / 'datapackages' / 'dados_ppo'
PRE_DIR = BASE_DIR / 'data_pre'
OUT_DIR = BASE_DIR / 'data'
DATAPACKAGE_PATH = BASE_DIR / 'datapackage.json'


# --------------------------------------------------------------------------
# Helpers genéricos
# --------------------------------------------------------------------------

def read_pre(name: str) -> pd.DataFrame:
    path = PRE_DIR / f'{name}.csv'
    if not path.exists():
        raise FileNotFoundError(f'Arquivo de origem não encontrado: {path}')
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def parse_br_number(value):
    if value is None:
        return None
    s = str(value).strip()
    if s == '' or s.lower() == 'nan':
        return None
    s = s.replace('R$', '').replace('\xa0', ' ').strip()
    s = s.replace(' ', '')
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def as_int(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors='coerce').astype('Int64')


def as_num(series: pd.Series) -> pd.Series:
    return series.apply(parse_br_number)


def dot_to_space(code):
    if code is None:
        return ''
    s = str(code).strip()
    if s == '':
        return ''
    return s.replace('.', ' ')


def strip_leading_zero_int(value):
    if value is None:
        return ''
    s = str(value).strip()
    if s == '' or s.lower() == 'nan':
        return ''
    try:
        return str(int(s))
    except ValueError:
        return s


def cod_nome(cod, nome):
    cod = '' if cod is None else str(cod).strip()
    nome = '' if nome is None else str(nome).strip()
    if cod == '' and nome == '':
        return ''
    return f'{cod} - {nome}'.strip(' -')


def format_trim(value):
    if value is None:
        return ''
    if value == int(value):
        return str(int(value))
    s = f'{value:.2f}'.rstrip('0').rstrip('.')
    return s


def parse_trim(value):
    return format_trim(parse_br_number(value))


def format_2dp(value):
    n = parse_br_number(value)
    if n is None:
        return ''
    return f'{n:.2f}'


def sim_nao_to_bool(value):
    s = '' if value is None else str(value).strip()
    if s.lower() == 'sim':
        return 'True'
    if s.lower() in ('não', 'nao'):
        return 'False'
    return s


def sim_nao_to_em_apuracao(value):
    s = '' if value is None else str(value).strip()
    if s.lower() == 'sim':
        return 'Em Apuração'
    return ''


def first_nonempty(*values):
    for v in values:
        s = '' if v is None else str(v).strip()
        if s:
            return s
    return ''


def int_or_marker(series: pd.Series, marker: str):
    def conv(v):
        s = '' if v is None else str(v).strip()
        if s == '':
            return marker
        try:
            return int(float(s))
        except ValueError:
            return s
    return series.apply(conv)


def str_or_marker(series: pd.Series, marker: str):
    return series.apply(lambda v: marker if (v is None or str(v).strip() == '') else v)


def pivot_by_ano(pre: pd.DataFrame, key_cols, value_col, base_year=2027, n_years=4):
    """Agrupa por key_cols e espalha value_col em <n_years> colunas (0..n_years-1),
    posicionadas conforme o deslocamento (ano - base_year). Anos fora da faixa são
    descartados; combinações sem valor para um ano ficam com NaN. Os valores voltam
    como número (float), não como texto — quem chama decide o formato final."""
    df = pre.copy()
    df['_val'] = df[value_col].apply(parse_br_number)
    df['_idx'] = pd.to_numeric(df['ano'], errors='coerce') - base_year
    df = df[df['_idx'].between(0, n_years - 1)]
    pivot = df.pivot_table(index=key_cols, columns='_idx', values='_val', aggfunc='sum')
    pivot = pivot.reindex(columns=range(n_years))
    pivot = pivot.reset_index()
    return pivot


def sanitize_text(df: pd.DataFrame) -> pd.DataFrame:
    def clean(value):
        if not isinstance(value, str):
            return value
        s = re.sub(r'[\r\n\u2028\u2029\x0b\x0c\x85]+', ' ', value)
        s = HTML_ENTITY_RE.sub(' ', s)
        for bad, good in INVALID_CHAR_MAP.items():
            s = s.replace(bad, good)
        return s

    out = df.copy()
    for col in out.columns:
        if not pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].apply(clean)
    return out


STATUS_OBRA_MAP = {
    'Iniciado': 'INICIANDO',
    'Execução': 'EXECUÇÃO',
    'Concluído': 'CONCLUÍDO',
    'Paralisado': 'PARALISADO',
    'Cancelado': 'CANCELADO',
}

INVALID_CHAR_MAP = {
    '\x02': ' ',
    '\u200b': ' ',
    '\x95': '-',
    '\u202f': ' ',
    '\x1a': ' ',
    '\t': ' ',
    '\u00a0': ' ',
}

HTML_ENTITY_RE = re.compile(r'&#\d+;?')

SIM_NAO_MAP = {'S': 'Sim', 'N': 'Não'}


# --------------------------------------------------------------------------
# 1) BASE_INTRA_ORCAMENTARIA_DETALHAMENTO  <-  intra_orcamentaria
#    (agregado por UO beneficiada: soma vlr_recebido e vlr_detalhado)
# --------------------------------------------------------------------------

def transform_base_intra_orcamentaria_detalhamento():
    pre = read_pre('intra_orcamentaria')
    df = pre.copy()
    df['vlr_recebido_num'] = df['vlr_recebido'].apply(parse_br_number).fillna(0.0)
    df['vlr_detalhado_num'] = df['vlr_detalhado'].apply(parse_br_number).fillna(0.0)
    grouped = df.groupby(
        ['uo_beneficiada_cod', 'uo_beneficiada_sigla'], as_index=False
    )[['vlr_recebido_num', 'vlr_detalhado_num']].sum()

    out = pd.DataFrame()
    out['Cód. UO Beneficiada'] = as_int(grouped['uo_beneficiada_cod'])
    out['UO Beneficiada'] = grouped['uo_beneficiada_sigla']
    out['Valor Recebido (R$)'] = grouped['vlr_recebido_num']
    out['Valor Detalhado (R$)'] = grouped['vlr_detalhado_num']
    return out


# --------------------------------------------------------------------------
# 2) BASE_INTRA_ORCAMENTARIA_REPASSE  <-  intra_orcamentaria (nível item, 1:1)
# --------------------------------------------------------------------------

def transform_base_intra_orcamentaria_repasse():
    pre = read_pre('intra_orcamentaria')
    out = pd.DataFrame()
    out['Cód. UO Repassadora'] = as_int(pre['uo_repassadora_cod'])
    out['UO Repassadora'] = pre['uo_repassadora_sigla']
    out['Cód. Programa de Trabalho'] = pre['programa_trabalho_fmt'].apply(dot_to_space)
    out['Ação'] = pre['acao_desc']
    out['Cód. Natureza de Despesa'] = pre['natureza_fmt'].apply(dot_to_space)
    out['Elemento Item'] = pre['item_desc']
    out['Valor Repassado (R$)'] = as_num(pre['vlr_recebido'])
    out['Cód. UO Beneficiada'] = int_or_marker(pre['uo_beneficiada_cod'], 'Não Repassado')
    out['UO Beneficiada'] = str_or_marker(pre['uo_beneficiada_sigla'], 'Não Repassado')
    return out


# --------------------------------------------------------------------------
# 3) BASE_ORCAM_DESPESA_ITEM_FISCAL  <-  orcamento_despesa (nível item, 1:1)
# --------------------------------------------------------------------------

def transform_orcam_despesa_item_fiscal():
    pre = read_pre('orcamento_despesa')
    out = pd.DataFrame()
    out['Código do Órgão'] = as_int(pre['orgao_cod'])
    out['Órgão'] = [cod_nome(o, u) for o, u in zip(pre['orgao_nome'], pre['uo_sigla'])]
    out['Código da UO'] = as_int(pre['uo_cod'])
    out['Unidade Orçamentária'] = [cod_nome(n, s) for n, s in zip(pre['uo_nome'], pre['uo_sigla'])]
    out['Função'] = as_int(pre['funcao_cod'])
    out['Subfunção'] = as_int(pre['subfuncao_cod'])
    out['Programa'] = as_int(pre['programa_cod'])
    out['Identificador'] = as_int(pre['identificador_cod'])
    out['Projeto_Atividade'] = as_int(pre['projeto_atividade_cod'])
    out['Ação'] = as_int(pre['acao_cod'])
    out['Subprojeto'] = as_int(pre['subprojeto_cod'])
    out['Categoria'] = as_int(pre['categoria_cod'])
    out['Grupo_Despesa'] = as_int(pre['grupo_cod'])
    out['Modalidade'] = as_int(pre['modalidade_cod'])
    out['Elemento_Despesa'] = as_int(pre['elemento_cod'])
    out['Item_Despesa'] = as_int(pre['item_cod'])
    out['Fonte'] = as_int(pre['fonte_cod'])
    out['IPU'] = as_int(pre['ipu_cod'])
    out['IAG'] = as_int(pre['iag_cod'])
    out['Descrição'] = pre['acao_desc']
    out['Valor (R$)'] = as_num(pre['vlr_loa_desp'])
    return out


# --------------------------------------------------------------------------
# 4) BASE_QDD_FISCAL  <-  orcamento_despesa (agregado por natureza, sem item)
# --------------------------------------------------------------------------

def transform_qdd_fiscal():
    pre = read_pre('orcamento_despesa')
    df = pre.copy()
    df['vlr_loa_desp_num'] = df['vlr_loa_desp'].apply(parse_br_number).fillna(0.0)

    group_cols = [
        'ano', 'poder_cod', 'orgao_cod', 'orgao_nome', 'uo_cod', 'uo_nome', 'uo_sigla',
        'funcao_cod', 'subfuncao_cod', 'programa_cod', 'programa_desc', 'acao_cod',
        'identificador_cod', 'projeto_atividade_cod', 'acao_desc', 'subprojeto_cod',
        'categoria_cod', 'grupo_cod', 'modalidade_cod', 'elemento_cod', 'iag_cod',
        'fonte_cod', 'ipu_cod',
    ]
    grouped = df.groupby(group_cols, as_index=False)['vlr_loa_desp_num'].sum()

    out = pd.DataFrame()
    out['ANO'] = as_int(grouped['ano'])
    out['COD_ORGAO'] = as_int(grouped['orgao_cod'])
    out['ORGAO'] = [cod_nome(o, u) for o, u in zip(grouped['orgao_nome'], grouped['uo_sigla'])]
    out['PODER'] = as_int(grouped['poder_cod'])
    out['SITUACAO'] = pd.array([pd.NA] * len(grouped), dtype='Int64')
    out['COD_UO'] = as_int(grouped['uo_cod'])
    out['UO'] = [cod_nome(n, s) for n, s in zip(grouped['uo_nome'], grouped['uo_sigla'])]
    out['CATEGORIA'] = as_int(grouped['categoria_cod'])
    out['GRUPO_DESPESA'] = as_int(grouped['grupo_cod'])
    out['MODALIDADE'] = as_int(grouped['modalidade_cod'])
    out['ELEMENTO_DESPESA'] = as_int(grouped['elemento_cod'])
    out['FONTE'] = as_int(grouped['fonte_cod'])
    out['IPU'] = as_int(grouped['ipu_cod'])
    out['SEQ_PROGTRAB'] = pd.array([pd.NA] * len(grouped), dtype='Int64')
    out['FUNCAO'] = as_int(grouped['funcao_cod'])
    out['SUB_FUNCAO'] = as_int(grouped['subfuncao_cod'])
    out['PROGRAMA'] = as_int(grouped['programa_cod'])
    out['IDENT_PROJATIV'] = as_int(grouped['identificador_cod'])
    out['PROJ_ATIV'] = as_int(grouped['projeto_atividade_cod'])
    out['AÇÃO'] = as_int(grouped['acao_cod'])
    out['SUB_PROJETO'] = as_int(grouped['subprojeto_cod'])
    out['VALOR UO (R$)'] = pd.array([pd.NA] * len(grouped), dtype='Float64')
    out['VALOR SCPPO (R$)'] = pd.array([pd.NA] * len(grouped), dtype='Float64')
    out['VALOR FINAL (R$)'] = grouped['vlr_loa_desp_num']
    out['IAG'] = as_int(grouped['iag_cod'])
    out['NOME_ACAO'] = grouped['acao_desc']
    out['NOME_PROGRAMA'] = grouped['programa_desc']
    return out


# --------------------------------------------------------------------------
# 5) BASE_ORCAM_DESPESA_INVESTIMENTO  <-  orcamento_despesa_investimento
#    (vlr_loa_desp pivotado por ano)
# --------------------------------------------------------------------------

def transform_base_orcam_despesa_investimento():
    pre = read_pre('orcamento_despesa_investimento')
    key_cols = [
        'orgao_cod', 'orgao_nome', 'uo_cod', 'uo_nome', 'uo_sigla',
        'funcao_cod', 'subfuncao_cod', 'programa_cod', 'identificador_cod',
        'projeto_atividade_cod', 'acao_cod', 'subprojeto_cod', 'fonte_invest_cod',
        'iag_cod', 'acao_desc', 'categoria_invest_cod', 'categoria_invest_desc',
        'natureza_invest_cod', 'natureza_invest_desc',
    ]
    pivot = pivot_by_ano(pre, key_cols, 'vlr_loa_desp', base_year=2027)

    out = pd.DataFrame()
    out['Código do Órgão'] = as_int(pivot['orgao_cod'])
    out['Órgão'] = [cod_nome(o, u) for o, u in zip(pivot['orgao_nome'], pivot['uo_sigla'])]
    out['Código da UO'] = as_int(pivot['uo_cod'])
    out['Unidade Orçamentária'] = [cod_nome(n, s) for n, s in zip(pivot['uo_nome'], pivot['uo_sigla'])]
    out['Função'] = as_int(pivot['funcao_cod'])
    out['Subfunção'] = as_int(pivot['subfuncao_cod'])
    out['Programa'] = as_int(pivot['programa_cod'])
    out['Identificador'] = as_int(pivot['identificador_cod'])
    out['Projeto_Atividade'] = as_int(pivot['projeto_atividade_cod'])
    out['Ação'] = as_int(pivot['acao_cod'])
    out['Subprojeto'] = as_int(pivot['subprojeto_cod'])
    out['Fonte'] = as_int(pivot['fonte_invest_cod'])
    out['IAG'] = as_int(pivot['iag_cod'])
    out['Descrição'] = pivot['acao_desc']
    out['Categoria'] = [
        cod_nome(c, d) for c, d in zip(pivot['categoria_invest_cod'], pivot['categoria_invest_desc'])
    ]
    out['Código da Natureza'] = as_int(pivot['natureza_invest_cod'])
    out['Natureza'] = pivot['natureza_invest_desc']
    out['Valor (R$) 2027'] = pivot[0]
    out['Valor (R$) 2028'] = pivot[1]
    out['Valor (R$) 2029'] = pivot[2]
    out['Valor (R$) 2030'] = pivot[3]
    return out


# --------------------------------------------------------------------------
# 6) BASE_QDD_INVESTIMENTO  <-  orcamento_despesa_investimento
# --------------------------------------------------------------------------

def transform_qdd_investimento():
    pre = read_pre('orcamento_despesa_investimento')
    out = pd.DataFrame()
    out['ANO'] = as_int(pre['ano'])
    out['COD_ORGAO'] = as_int(pre['orgao_cod'])
    out['ORGAO'] = [cod_nome(o, u) for o, u in zip(pre['orgao_nome'], pre['uo_sigla'])]
    out['PODER'] = as_int(pre['poder_cod'])
    out['COD_UO'] = as_int(pre['uo_cod'])
    out['UO'] = [cod_nome(n, s) for n, s in zip(pre['uo_nome'], pre['uo_sigla'])]
    out['SEQ_PROGTRAB'] = pd.array([pd.NA] * len(pre), dtype='Int64')
    out['FUNCAO'] = as_int(pre['funcao_cod'])
    out['SUB_FUNCAO'] = as_int(pre['subfuncao_cod'])
    out['PROGRAMA'] = as_int(pre['programa_cod'])
    out['IDENT_PROJATIV'] = as_int(pre['identificador_cod'])
    out['PROJ_ATIV'] = as_int(pre['projeto_atividade_cod'])
    out['AÇÃO'] = as_int(pre['acao_cod'])
    out['VALOR (R$)'] = as_num(pre['vlr_loa_desp'])
    out['IAG'] = as_int(pre['iag_cod'])
    out['DESC_PROJETO_ATIV'] = pre['acao_desc']
    out['CATEGORIA'] = [cod_nome(c, d) for c, d in zip(pre['categoria_invest_cod'], pre['categoria_invest_desc'])]
    out['COD_NATUREZA'] = as_int(pre['natureza_invest_cod'])
    out['NATUREZA'] = pre['natureza_invest_desc']
    out['COD_FONTE'] = as_int(pre['fonte_invest_cod'])
    out['FONTE'] = pre['fonte_invest_desc']
    out['NOME_ACAO'] = pre['acao_desc']
    out['NOME_PROGRAMA'] = pre['programa_desc']
    return out


# --------------------------------------------------------------------------
# 7) BASE_LIMITE_COTA  <-  orcamento_limite (vlr_limite pivotado por ano)
# --------------------------------------------------------------------------

def transform_base_limite_cota():
    pre = read_pre('orcamento_limite')
    key_cols = ['uo_cod', 'uo_sigla', 'grupo_cod', 'fonte_cod', 'ipu_cod', 'iag_cod']
    pivot = pivot_by_ano(pre, key_cols, 'vlr_limite', base_year=2027)

    out = pd.DataFrame()
    out['Cód. UO'] = as_int(pivot['uo_cod'])
    out['UO'] = pivot['uo_sigla']
    out['Grupo de Despesa'] = as_int(pivot['grupo_cod'])
    out['Fonte'] = as_int(pivot['fonte_cod'])
    out['IPU'] = as_int(pivot['ipu_cod'])
    out['IAG'] = as_int(pivot['iag_cod'])
    out['Valor Limite 2027'] = pivot[0]
    out['Valor Utilizado 2027'] = pd.array([pd.NA] * len(pivot), dtype='Float64')
    out['Valor Transferido'] = pd.array([pd.NA] * len(pivot), dtype='Float64')
    out['Valor Limite 2028'] = pivot[1]
    out['Valor Utilizado 2028'] = pd.array([pd.NA] * len(pivot), dtype='Float64')
    out['Valor Limite 2029'] = pivot[2]
    out['Valor Utilizado 2029'] = pd.array([pd.NA] * len(pivot), dtype='Float64')
    out['Valor Limite 2030'] = pivot[3]
    out['Valor Utilizado 2030'] = pd.array([pd.NA] * len(pivot), dtype='Float64')
    return out


# --------------------------------------------------------------------------
# 8) BASE_DETALHAMENTO_OBRAS  <-  orcamento_obras
# --------------------------------------------------------------------------

def transform_detalhamento_obras():
    pre = read_pre('orcamento_obras')
    out = pd.DataFrame()
    out['UO'] = as_int(pre['uo_cod'])
    out['FUNCAO'] = as_int(pre['funcao_cod'])
    out['SUBFUNCAO'] = as_int(pre['subfuncao_cod'])
    out['PROGRAMA'] = as_int(pre['programa_cod'])
    out['ACAO'] = as_int(pre['acao_cod'])
    out['SUBPROJETO'] = as_int(pre['subprojeto_cod'])
    out['IAG'] = as_int(pre['iag_cod'])
    out['NUMERO DA OBRA SISOR'] = pd.Series(range(1, len(pre) + 1), dtype='Int64')
    out['NUMERO DA OBRA SIAD'] = as_int(pre['obra_siad_cod'])
    out['DESCRICAO DA OBRA'] = pre['obra_desc'].str.replace("'", "`", regex=False)
    out['STATUS DA OBRA'] = pre['obra_status'].map(STATUS_OBRA_MAP).fillna(
        pre['obra_status'].str.upper()
    )
    out['UNIDADE DE MEDIDA DA OBRA'] = pre['unidade_medida_desc']
    out['QUANTIDADE'] = as_int(pre['obra_quantidade'])
    out['ALTERAR UNIDADE DE MEDIDA DA OBRA'] = pre['unidade_medida_alterar'].map(SIM_NAO_MAP).fillna('')
    out['REGIÃO GEOGRÁFICA INTERMEDIÁRIA'] = pre['regiao_geografica_intermediaria_desc']
    out['MUNICÍPIO'] = pre['municipio_desc']
    out['VALOR TESOURO 2027 (R$)'] = as_num(pre['vlr_tesouro'])
    out['VALOR OUTROS 2027 (R$)'] = as_num(pre['vlr_outros'])
    for col in ['VALOR TESOURO 2028 (R$)', 'VALOR OUTROS 2028 (R$)',
                'VALOR TESOURO 2029 (R$)', 'VALOR OUTROS 2029 (R$)',
                'VALOR TESOURO 2030 (R$)', 'VALOR OUTROS 2030 (R$)']:
        out[col] = pd.array([pd.NA] * len(pre), dtype='Float64')
    return out


# --------------------------------------------------------------------------
# 9) BASE_CATEGORIA_PESSOAL  <-  orcamento_pessoal
# --------------------------------------------------------------------------

def transform_categoria_pessoal():
    pre = read_pre('orcamento_pessoal')

    pre = pre[pd.to_numeric(pre['uo_cod'], errors='coerce') != 1941].copy()

    out = pd.DataFrame()
    out['Ano de Exercício'] = as_int(pre['ano'])
    out['UO'] = [cod_nome(c, s) for c, s in zip(pre['uo_cod'], pre['uo_sigla'])]
    out['Classificação'] = (
        pre['pessoal_classificacao']
        .str.replace('PESSOAL ', '', regex=False)
        .str.title()
    )
    out['Categoria'] = pre['pessoal_categoria']
    out['Quantidade'] = as_int(pre['pessoal_quantidade'])
    return out


# --------------------------------------------------------------------------
# 10) BASE_ORCAM_RECEITA_FISCAL  <-  orcamento_receita
# --------------------------------------------------------------------------

def transform_orcam_receita_fiscal():
    pre = read_pre('orcamento_receita')
    out = pd.DataFrame()
    out['UO_COD'] = as_int(pre['uo_cod'])
    out['NOME_UO'] = pre['uo_nome']
    out['SIGLA_UO'] = pre['uo_sigla']
    out['COD_FONTE'] = as_int(pre['fonte_cod'])
    out['FONTE'] = ''
    out['INTERPRETACAO'] = ''
    out['CATEGORIA'] = as_int(pre['categoria_cod'])
    out['ORIGEM'] = as_int(pre['origem_cod'])
    out['ESPECIE'] = as_int(pre['especie_cod'])
    out['RUBRICA'] = as_int(pre['rubrica_cod'])
    out['ALINEA'] = as_int(pre['alinea_cod'])
    out['SUBALINEA'] = as_int(pre['subalinea_cod'])
    out['TIPO_RECEITA'] = as_int(pre['receita_tipo_cod'])
    out['ITEM'] = as_int(pre['item_cod'])
    out['SUBITEM'] = as_int(pre['subitem_cod'])
    out['COD_RECEITA'] = as_int(pre['receita_cod_fmt'].str.replace('.', '', regex=False))
    out['RECEITA'] = pre['receita_desc']
    out['INTERP_RECEITA'] = ''
    out['VALOR UO (R$)'] = pd.array([pd.NA] * len(pre), dtype='Float64')
    out['VALOR SCPPO (R$)'] = pd.array([pd.NA] * len(pre), dtype='Float64')
    out['VALOR FINAL (R$)'] = as_num(pre['vlr_loa_rec'])
    out['ANO'] = as_int(pre['ano'])
    out['BASE LEGAL'] = '-'
    out['METODOLOGIA DE CÁLCULO E PREMISSAS UTILIZADAS'] = pre['metodologia']
    return out


# --------------------------------------------------------------------------
# 11) BASE_ORCAM_RECEITA_INVESTIMENTO  <-  orcamento_receita_investimento (1:1)
# --------------------------------------------------------------------------

def transform_base_orcam_receita_investimento():
    pre = read_pre('orcamento_receita_investimento')
    out = pd.DataFrame()
    out['COD_UO'] = as_int(pre['uo_cod'])
    out['NOME_UO'] = pre['uo_nome']
    out['SIGLA_UO'] = pre['uo_sigla']
    out['CATEGORIA'] = pd.array([pd.NA] * len(pre), dtype='Int64')
    out['SUBCATEGORIA'] = pd.array([pd.NA] * len(pre), dtype='Int64')
    out['ALINEA'] = pd.array([pd.NA] * len(pre), dtype='Int64')
    out['SUBALINEA'] = pd.array([pd.NA] * len(pre), dtype='Int64')
    out['COD_RECEITA'] = ''
    out['NIVEL_ORIGEM'] = ''
    out['RECEITA'] = ''
    out['VALOR UO (R$)'] = pd.array([pd.NA] * len(pre), dtype='Float64')
    out['VALOR SCPPO (R$)'] = pd.array([pd.NA] * len(pre), dtype='Float64')
    out['VALOR FINAL (R$)'] = as_num(pre['vlr_loa_rec_invest'])
    out['ANO'] = as_int(pre['ano'])
    return out


# --------------------------------------------------------------------------
# 12) BASE_REPASSE_RECURSOS  <-  orcamento_repasse
# --------------------------------------------------------------------------

def transform_repasse_recursos():
    pre = read_pre('orcamento_repasse')
    out = pd.DataFrame()
    out['Cód. UO Financiadora'] = as_int(pre['uo_financiadora_cod'])
    out['UO Financiadora'] = pre['uo_financiadora_nome']
    out['Cód. UO Beneficiada'] = as_int(pre['uo_beneficiada_cod'])
    out['UO Beneficiada'] = pre['uo_beneficiada_nome']
    out['Grupo de Despesa'] = as_int(pre['grupo_cod'])
    out['Fonte'] = as_int(pre['fonte_cod'])
    out['IPU'] = as_int(pre['ipu_cod'])
    out['IAG'] = as_int(pre['iag_cod'])
    out['Valor Transferido (R$)'] = as_num(pre['vlr_repasse'])
    return out


# --------------------------------------------------------------------------
# 13) acoes_planejamento  <-  planejamento_acao
# --------------------------------------------------------------------------

def transform_acoes_planejamento():
    pre = read_pre('planejamento_acao')
    out = pd.DataFrame()
    out['Código do Programa'] = pre['programa_cod'].str.zfill(4)
    out['Nome do Programa'] = pre['programa_desc']
    out['Código da Área Temática'] = pre['area_tematica_cod']
    out['Área Temática'] = pre['area_tematica_desc']
    out['Exclusão Lógica do Programa'] = pre['programa_exclusao']
    out['Programa Novo'] = pre['programa_novo']
    out['Justificativa de Inclusão ou Exclusão do Programa'] = pre['programa_justificativa_inclusao']
    out['Código da Unidade Orçamentária Responsável pelo Programa'] = pre['uo_programa_cod']
    out['Unidade Orçamentária Responsável pelo Programa'] = pre['uo_programa_nome']
    out['Código da Unidade Orçamentária Responsável pela Ação'] = pre['uo_acao_cod']
    out['Unidade Orçamentária Responsável pela Ação'] = pre['uo_acao_nome']
    out['Código da Função'] = pre['funcao_cod']
    out['Função'] = pre['funcao_desc']
    out['Código da Subfunção'] = pre['subfuncao_cod']
    out['Subfunção'] = pre['subfuncao_desc']
    out['Código do Tipo de Ação'] = pre['identificador_cod']
    out['Tipo de Ação'] = pre['identificador_desc']
    out['Código da Ação'] = pre['acao_cod']
    out['Título da Ação'] = pre['acao_desc']
    out['Código do Identificador de Ação Governamental (IAG)'] = pre['iag_cod']
    out['Identificador de Ação Governamental (IAG)'] = pre['iag_desc']
    out['Código do Projeto Estratégico'] = pre['projeto_estrategico_cod']
    out['Projeto Estratégico'] = pre['projeto_estrategico_desc']
    out['Exclusão Lógica da Ação'] = pre['acao_exclusao']
    out['Nova Ação'] = pre['acao_novo']
    out['Justificativa de Inclusão ou Exclusão da Ação'] = pre['acao_justificativa_inclusao']
    out['Transferida para o SISOR'] = ''
    out['Unidade Administrativa Responsável pela Ação'] = pre['ua_acao_nome']
    out['Base legal'] = pre['base_legal']
    out['Finalidade da Ação'] = pre['acao_finalidade']
    out['Descrição da Ação'] = pre['acao_descricao']
    out['Código do Público-alvo'] = pre['publico_alvo_cod']
    out['Público-Alvo'] = pre['publico_alvo_desc']
    out['Código do Produto'] = pre['produto_cod']
    out['Produto'] = pre['produto_desc']
    out['Especificação do Produto'] = pre['produto_especificacao']
    out['Código da Unidade de Medida do Produto'] = pre['unidade_medida_cod']
    out['Unidade de Medida do Produto'] = pre['unidade_medida_desc']
    for ano_label, i in zip(['2027', '2028', '2029', '2030'], range(4)):
        out[f'Previsão Orçamentária {ano_label}'] = pre[f'vlr_meta_orcamentaria_ano{i}'].apply(parse_trim)
    for ano_label, i in zip(['2027', '2028', '2029', '2030'], range(4)):
        out[f'Previsão Física {ano_label}'] = pre[f'vlr_meta_fisica_ano{i}'].apply(parse_trim)
    out['Ação Transposta'] = ''
    out['Setor de Governo'] = pre['governo_setor']
    out['Política para mulheres'] = pre['politica_mulheres']
    return out


# --------------------------------------------------------------------------
# 14) indicadores_planejamento  <-  planejamento_indicador
# --------------------------------------------------------------------------

def transform_indicadores_planejamento():
    pre = read_pre('planejamento_indicador')
    out = pd.DataFrame()
    out['Código do Programa'] = pre['programa_cod'].str.zfill(4)
    out['Nome do Programa'] = pre['programa_desc']
    out['Exclusão Lógica do Programa'] = pre['programa_exclusao'].apply(sim_nao_to_bool)
    out['Indicador'] = pre['indicador_desc']
    out['Exclusão Lógica do Indicador'] = pre['indicador_exclusao'].apply(sim_nao_to_bool)
    out['Unidade de Medida'] = pre['unidade_medida_desc']
    out['Índice de Referência'] = pre['indice_referencia'].apply(format_2dp)
    out['Em apuração? (Índice de Referência)'] = pre['indice_referencia_apuracao'].apply(sim_nao_to_em_apuracao)
    out['Data de Apuração'] = pre['indice_referencia_data_apuracao']
    for ano_label, i in zip(['2027', '2028', '2029', '2030'], range(4)):
        out[f'Previsão para {ano_label}'] = pre[f'previsao_ano{i}'].apply(format_2dp)
        out[f'Em apuração? ({ano_label})'] = pre[f'apuracao_ano{i}'].apply(sim_nao_to_em_apuracao)
    out['Fonte'] = pre['fonte_desc']
    out['Periodicidade'] = pre['periodicidade']
    out['Base Geográfica'] = pre['base_geografica']
    out['Fórmula de Cálculo'] = pre['formula_calculo']
    out['Justificativa do Status em apuração da(s) Previsão(es) do(s) Índice(s)'] = [
        first_nonempty(a, b, c, d) for a, b, c, d in zip(
            pre['previsao_apuracao_justificativa_ano0'],
            pre['previsao_apuracao_justificativa_ano1'],
            pre['previsao_apuracao_justificativa_ano2'],
            pre['previsao_apuracao_justificativa_ano3'],
        )
    ]
    out['Justificativa do Status em apuração do Índice de Referência'] = pre['indice_referencia_apuracao_justificativa']
    out['Data Alteração'] = ''
    out['Indicador Novo?'] = pre['indicador_novo'].apply(sim_nao_to_bool)
    out['Polaridade'] = pre['polaridade']
    return out


# --------------------------------------------------------------------------
# 15) localizadores_todos_planejamento  <-  planejamento_localizador
# --------------------------------------------------------------------------

def transform_localizadores_planejamento():
    pre = read_pre('planejamento_localizador')
    out = pd.DataFrame()
    out['Código do Programa'] = pre['programa_cod'].str.zfill(4)
    out['Nome do Programa'] = pre['programa_desc']
    out['Código da Área Temática'] = pre['area_tematica_cod']
    out['Área Temática'] = pre['area_tematica_desc']
    out['Exclusão Lógica do Programa'] = pre['programa_exclusao'].apply(sim_nao_to_bool)
    out['Código da Ação'] = pre['acao_cod']
    out['Título da Ação'] = pre['acao_desc']
    out['Código do Identificador de Ação Governamental (IAG)'] = pre['iag_cod']
    out['Identificador de Ação Governamental (IAG)'] = pre['iag_desc']
    out['Código do Projeto Estratégico'] = pre['projeto_estrategico_cod']
    out['Projeto Estratégico'] = pre['projeto_estrategico_desc']
    out['Código da Função'] = pre['funcao_cod']
    out['Função'] = pre['funcao_desc']
    out['Código da Subfunção'] = pre['subfuncao_cod']
    out['SubFunção'] = pre['subfuncao_desc']
    out['Código da Unidade Orçamentária Responsável pela Ação'] = pre['uo_acao_cod'].str.zfill(5)
    out['Unidade Orçamentária Responsável pela Ação'] = pre['uo_acao_nome']
    out['Exclusão Lógica da Ação'] = pre['acao_exclusao'].apply(sim_nao_to_bool)
    out['Código do Localizador'] = ''
    out['Exclusão Lógica do Localizador'] = ''
    out['Código da Região Geográfica Intermediária'] = pre['regiao_geografica_intermediaria_cod']
    out['Região Geográfica Intermediária'] = pre['regiao_geografica_intermediaria_desc']
    out['Código do Município IBGE'] = pre['municipio_ibge_cod']
    out['Código do Município Sigplan'] = pre['municipio_sigplan_cod']
    out['Município'] = pre['municipio_desc']
    for ano_label, i in zip(['2027', '2028', '2029', '2030'], range(4)):
        out[f'Previsão Orçamentária {ano_label}'] = pre[f'vlr_meta_orcamentaria_ano{i}'].apply(parse_trim)
        out[f'Previsão Física {ano_label}'] = pre[f'vlr_meta_fisica_ano{i}'].apply(parse_trim)
    return out


# --------------------------------------------------------------------------
# 16) programas_planejamento  <-  planejamento_programa
# --------------------------------------------------------------------------

def transform_programas_planejamento():
    pre = read_pre('planejamento_programa')
    out = pd.DataFrame()
    out['Código do Programa'] = pre['programa_cod'].str.zfill(4)
    out['Nome do Programa'] = pre['programa_desc']
    out['Exclusão Lógica do Programa'] = pre['programa_exclusao']
    out['Programa Novo'] = pre['programa_novo']
    out['Código da Área Temática'] = pre['area_tematica_cod']
    out['Área Temática'] = pre['area_tematica_desc']
    out['Código do Objetivo Estratégico'] = pre['objetivo_estrategico_cod']
    out['Objetivo Estratégico'] = pre['objetivo_estrategico_desc']
    out['Código da Diretriz Estratégica'] = pre['diretriz_estrategica_cod']
    out['Diretriz Estratégica'] = pre['diretriz_estrategica_desc']
    out['Justificativa de Inclusão ou Exclusão do Programa'] = pre['programa_justificativa_inclusao']
    out['Código do Órgão Responsável pelo Programa'] = pre['orgao_programa_cod'].str.zfill(5)
    out['Órgão Responsável pelo Programa'] = pre['orgao_programa_nome']
    out['Código da Unidade Orçamentária Responsável pelo Programa'] = pre['uo_programa_cod']
    out['Unidade Orçamentária Responsável pelo Programa'] = pre['uo_programa_nome']
    out['Objetivo'] = pre['programa_objetivo']
    out['Justificativa'] = pre['programa_justificativa']
    out['Tipo de Programa'] = pre['tipo_de_programa']
    out['Horizonte Temporal'] = pre['horizonte_temporal'].replace({'CONTINUO': 'Contínuo'})
    out['Estratégia de Implementação'] = pre['estrategia_implementacao']
    out['Unidade Administrativa Responsável pelo Programa'] = pre['ua_programa_nome']
    for ano_label, i in zip(['2027', '2028', '2029', '2030'], range(4)):
        out[f'Previsão Orçamentária {ano_label}'] = pre[f'vlr_meta_orcamentaria_ano{i}'].apply(parse_trim)
    out['Programa Transposto'] = ''
    out['Causas'] = pre['causas']
    out['Título do Objetivo de Desenvolvimento Sustentável'] = [
        cod_nome(c, t) for c, t in zip(pre['ods_cod'], pre['ods_titulo'])
    ]
    out['Subtítulo do Objetivo de Desenvolvimento Sustentável'] = ''
    return out


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

TRANSFORMS = {
    'BASE_INTRA_ORCAMENTARIA_DETALHAMENTO': transform_base_intra_orcamentaria_detalhamento,
    'BASE_INTRA_ORCAMENTARIA_REPASSE': transform_base_intra_orcamentaria_repasse,
    'BASE_ORCAM_DESPESA_ITEM_FISCAL': transform_orcam_despesa_item_fiscal,
    'BASE_QDD_FISCAL': transform_qdd_fiscal,
    'BASE_ORCAM_DESPESA_INVESTIMENTO': transform_base_orcam_despesa_investimento,
    'BASE_QDD_INVESTIMENTO': transform_qdd_investimento,
    'BASE_LIMITE_COTA': transform_base_limite_cota,
    'BASE_DETALHAMENTO_OBRAS': transform_detalhamento_obras,
    'BASE_CATEGORIA_PESSOAL': transform_categoria_pessoal,
    'BASE_ORCAM_RECEITA_FISCAL': transform_orcam_receita_fiscal,
    'BASE_ORCAM_RECEITA_INVESTIMENTO': transform_base_orcam_receita_investimento,
    'BASE_REPASSE_RECURSOS': transform_repasse_recursos,
    'acoes_planejamento': transform_acoes_planejamento,
    'indicadores_planejamento': transform_indicadores_planejamento,
    'localizadores_todos_planejamento': transform_localizadores_planejamento,
    'programas_planejamento': transform_programas_planejamento,
}

OUTPUT_OVERRIDES = {
    'acoes_planejamento': {'filename': 'acoes_planejamento.txt', 'sep': '|', 'format': 'txt'},
    'programas_planejamento': {'filename': 'programas_planejamento.txt', 'sep': '|', 'format': 'txt'},
    'localizadores_todos_planejamento': {'filename': 'localizadores_todos_planejamento.txt', 'sep': '|', 'format': 'txt'},
    'indicadores_planejamento': {'filename': 'indicadores_planejamento.txt', 'sep': '|', 'format': 'txt'},
}


def write_output(name: str, df: pd.DataFrame) -> Path:
    override = OUTPUT_OVERRIDES.get(name, {})
    fmt = override.get('format', 'xlsx')
    filename = override.get('filename', f'{name}.xlsx')
    dest = OUT_DIR / filename

    if fmt == 'xlsx':
        df.to_excel(dest, index=False, engine='openpyxl')
    else:
        sep = override.get('sep', ',')
        df.to_csv(dest, index=False, sep=sep, encoding='utf-8')
    return dest


def build_datapackage():
    output_files = sorted(OUT_DIR.glob('*.xlsx')) + sorted(OUT_DIR.glob('*.txt'))
    resource_descriptors = []

    for file_path in output_files:
        name = file_path.stem.lower()
        ext = file_path.suffix.lstrip('.')

        if ext == 'xlsx':
            probe_descriptor = {
                'name': name,
                'path': f'data/{file_path.name}',
                'format': 'xlsx',
            }
            probe = Resource.from_descriptor(probe_descriptor, basepath=str(BASE_DIR))
            probe.infer(stats=True)
            fields = probe.schema.to_dict().get('fields', [])

            if name == 'base_detalhamento_obras':
                for field in fields:
                    if field['name'] == 'QUANTIDADE':
                        field['type'] = 'integer'

                    if field['name'] == 'UNIDADE DE MEDIDA DA OBRA':
                        field['type'] = 'string'

            descriptor = {
                'profile': 'tabular-data-resource',
                'name': name,
                'title': name,
                'path': f'data/{file_path.name}',
                'scheme': 'file',
                'format': 'xlsx',
                'mediatype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'schema': {'fields': fields},
            }

        else:
            sep = OUTPUT_OVERRIDES.get(name, {}).get('sep', ',')
            try:
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    header_line = f.readline().rstrip('\r\n')
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    header_line = f.readline().rstrip('\r\n')
            field_names = [fn.strip() for fn in header_line.split(sep)]
            fields = [{'name': fn} for fn in field_names]

            descriptor = {
                'profile': 'tabular-data-resource',
                'name': name,
                'title': name,
                'path': f'data/{file_path.name}',
                'scheme': 'file',
                'format': 'csv',
                'mediatype': 'text/csv',
                'encoding': 'utf-8',
                'dialect': {'csv': {'delimiter': sep}},
                'schema': {'fields': fields},
            }

        resource_descriptors.append(descriptor)

    target_descriptor = {
        'profile': 'tabular-data-package',
        'name': 'dados_ppo_2027',
        'title': 'Portal de Planejamento e Orçamento - PPO-MG',
        'owner_org': 'secretaria-de-estado-de-planejamento-e-gestao-seplag',
        'dpetl_load': {
            'owner': 'splor-mg',
            'repo': 'dados-ppo-2027',
            'level': 'orgs',
            'visibility': 'public',
        },
        'resources': resource_descriptors,
    }

    target = Package.from_descriptor(target_descriptor, basepath=str(BASE_DIR))
    target.custom['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    for resource in target.resources:
        resource.infer(stats=True)

    target.to_json(str(DATAPACKAGE_PATH))
    print(f'OK  datapackage.json  ({len(target.resources)} resources) -> {DATAPACKAGE_PATH}')


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    empty_col_report = {}

    for out_name, fn in TRANSFORMS.items():
        try:
            df = fn()
        except FileNotFoundError as e:
            print(f'[AVISO] Pulando {out_name}: {e}')
            continue

        df = sanitize_text(df)
        dest = write_output(out_name, df)
        print(f'OK  {dest.name}  ({len(df)} linhas, {len(df.columns)} colunas) -> {dest}')

        empties = [c for c in df.columns if df[c].isna().all() or (df[c].astype(str).str.strip().eq('')).all()]
        if empties:
            empty_col_report[out_name] = empties

    if empty_col_report:
        print('\n=== Colunas de saída sem dado equivalente em data_pre (ficaram vazias) ===')
        for name, cols in empty_col_report.items():
            print(f'- {name}: {', '.join(cols)}')

    build_datapackage()


if __name__ == '__main__':
    main()
