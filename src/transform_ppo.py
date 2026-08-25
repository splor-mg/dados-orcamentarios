import pandas as pd
from pathlib import Path
from datetime import datetime
from frictionless import Package, Resource

BASE_DIR = Path(__file__).resolve().parent.parent / "datapackages" / "dados_ppo"
PRE_DIR = BASE_DIR / "data_pre"
OUT_DIR = BASE_DIR / "data"
DATAPACKAGE_PATH = BASE_DIR / "datapackage.json"


# --------------------------------------------------------------------------
# Helpers genéricos
# --------------------------------------------------------------------------

def read_pre(name: str) -> pd.DataFrame:
    path = PRE_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {path}")
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def parse_br_number(value):
    """Converte número no formato brasileiro ('1.234,56' ou '1234,56' ou
    'R$ 1.234,56') para float. Retorna None se vazio/])."""
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() == "nan":
        return None
    s = s.replace("R$", "").replace("\xa0", " ").strip()
    s = s.replace(" ", "")
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def dot_to_space(code):
    """'1.02.1.01.031' -> '1 02 1 01 031'"""
    if code is None:
        return ""
    s = str(code).strip()
    if s == "":
        return ""
    return s.replace(".", " ")


def strip_leading_zero_int(value):
    """'04' -> '4' ; '' -> ''"""
    if value is None:
        return ""
    s = str(value).strip()
    if s == "" or s.lower() == "nan":
        return ""
    try:
        return str(int(s))
    except ValueError:
        return s


def cod_nome(cod, nome):
    cod = "" if cod is None else str(cod).strip()
    nome = "" if nome is None else str(nome).strip()
    if cod == "" and nome == "":
        return ""
    return f"{cod} - {nome}".strip(" -")


def split_cod_nome(value):
    """'2061 - FUNDAÇÃO JOÃO PINHEIRO' -> ('2061', 'FUNDAÇÃO JOÃO PINHEIRO')"""
    if value is None:
        return "", ""
    s = str(value).strip()
    if " - " not in s:
        return s, ""
    cod, nome = s.split(" - ", 1)
    return cod.strip(), nome.strip()


def format_money(value):
    """Formata sempre com 2 casas decimais fixas (estilo moeda), ex: 1000 -> '1000.00'."""
    if value is None:
        return ""
    return f"{value:.2f}"


def format_trim(value):
    """Formata sem casas decimais desnecessárias: se o decimal for 0, não
    aparece ('1000.0' -> '1000'); se houver decimal real, mantém (sem
    arredondar), ex: '150.5' -> '150.5'."""
    if value is None:
        return ""
    if value == int(value):
        return str(int(value))
    s = f"{value:.2f}".rstrip("0").rstrip(".")
    return s


def parse_money(value):
    return format_money(parse_br_number(value))


def parse_trim(value):
    return format_trim(parse_br_number(value))


def new_df(columns, n_rows=0):
    return pd.DataFrame({c: [""] * n_rows for c in columns}, columns=columns)


def build_lookup(df, key_col, val_col):
    """Cria dict a partir de pares (key_col, val_col) únicos, ignorando
    linhas vazias."""
    sub = df[[key_col, val_col]].drop_duplicates()
    sub = sub[sub[key_col].astype(str).str.strip() != ""]
    return dict(zip(sub[key_col].astype(str).str.strip(), sub[val_col]))


GRUPO_DESC_TO_COD = {
    "PESSOAL E ENCARGOS SOCIAIS": "1",
    "JUROS E ENCARGOS DA DÍVIDA": "2",
    "OUTRAS DESPESAS CORRENTES": "3",
    "INVESTIMENTOS": "4",
    "INVERSÕES FINANCEIRAS": "5",
    "AMORTIZAÇÃO DA DÍVIDA": "6",
}

STATUS_OBRA_MAP = {
    "Iniciado": "INICIANDO",
    "Execução": "EXECUÇÃO",
    "Concluído": "CONCLUÍDO",
    "Paralisado": "PARALISADO",
    "Cancelado": "CANCELADO",
}

SIM_NAO_MAP = {"S": "Sim", "N": "Não"}
SIM_NAO_BOOL_MAP = {"Sim": "True", "Não": "False"}


# --------------------------------------------------------------------------
# 1) base_categoria_pessoal  <-  orcamento_pessoal
# --------------------------------------------------------------------------

def transform_categoria_pessoal():
    pre = read_pre("orcamento_pessoal")
    out = pd.DataFrame()
    out["ano"] = pre["ano"]
    out["uo_cod_sigla"] = [cod_nome(c, s) for c, s in zip(pre["uo_cod"], pre["uo_sigla"])]
    out["classificacao"] = (
        pre["pessoal_classificacao"]
        .str.replace("PESSOAL ", "", regex=False)
        .str.title()
    )
    out["categoria"] = pre["pessoal_categoria"]
    out["quantidade"] = pre["pessoal_quantidade"]
    return out


# --------------------------------------------------------------------------
# 2) base_detalhamento_obras  <-  orcamento_obras
# --------------------------------------------------------------------------

def transform_detalhamento_obras():
    pre = read_pre("orcamento_obras")
    out = pd.DataFrame()
    out["uo_cod"] = pre["uo_cod"]
    out["funcao_cod"] = pre["funcao_cod"]
    out["subfuncao_cod"] = pre["subfuncao_cod"]
    out["programa_cod"] = pre["programa_cod"]
    out["acao_cod"] = pre["acao_cod"]
    out["subprojeto_subatividade_cod"] = pre["subprojeto_cod"]
    out["iag_cod"] = pre["iag_cod"]
    out["numero_da_obra_sisor"] = ""
    out["numero_da_obra_siad"] = pre["obra_siad_cod"]
    out["descricao_da_obra"] = pre["obra_desc"]
    out["status_da_obra"] = pre["obra_status"].map(STATUS_OBRA_MAP).fillna(
        pre["obra_status"].str.upper()
    )
    out["unidade_de_medida_da_obra"] = pre["unidade_medida_cod"]
    out["quantidade"] = pre["obra_quantidade"]
    out["alterar_unidade_de_medida_da_obra"] = pre["unidade_medida_alterar"].map(SIM_NAO_MAP).fillna("")
    out["regiao_geografica_intermediaria"] = pre["regiao_geografica_intermediaria_desc"]
    out["municipio"] = pre["municipio_desc"]
    out["vlr_tesouro_ano0"] = pre["vlr_tesouro"].apply(parse_money)
    out["vlr_outros_ano0"] = pre["vlr_outros"].apply(parse_money)
    for col in ["vlr_tesouro_ano1", "vlr_outros_ano1", "vlr_tesouro_ano2", "vlr_outros_ano2",
                "vlr_tesouro_ano3", "vlr_outros_ano3"]:
        out[col] = ""
    return out


# --------------------------------------------------------------------------
# 3) base_intra_orcamentaria_repasse  <-  intra_orcamentaria
# --------------------------------------------------------------------------

def transform_intra_orcamentaria_repasse():
    pre = read_pre("intra_orcamentaria")
    out = pd.DataFrame()
    out["uo_repassadora_cod"] = pre["uo_repassadora_cod"]
    out["uo_repassadora_sigla"] = pre["uo_repassadora_sigla"]
    out["programa_trabalho_fmt"] = pre["programa_trabalho_fmt"].apply(dot_to_space)
    out["acao_desc"] = pre["acao_desc"]
    out["natureza_desp_fmt"] = [
        f"{dot_to_space(nat)} {strip_leading_zero_int(item)}".strip()
        for nat, item in zip(pre["natureza_fmt"], pre["item_cod"])
    ]
    out["item_desc"] = pre["item_desc"]
    out["vlr_repassado"] = pre["vlr_recebido"].apply(parse_trim)
    out["uo_beneficiada_cod"] = pre["uo_beneficiada_cod"]
    out["uo_beneficiada_sigla"] = pre["uo_beneficiada_sigla"]
    return out


# --------------------------------------------------------------------------
# 4) base_intra_orcamentaria_detalhamento  <-  intra_orcamentaria (agregado)
# --------------------------------------------------------------------------

def transform_intra_orcamentaria_detalhamento():
    pre = read_pre("intra_orcamentaria")
    df = pre.copy()
    df["vlr_recebido_num"] = df["vlr_recebido"].apply(parse_br_number).fillna(0.0)
    df["vlr_detalhado_num"] = df["vlr_detalhado"].apply(parse_br_number).fillna(0.0)
    grouped = (
        df.groupby(["uo_beneficiada_cod", "uo_beneficiada_sigla"], as_index=False)
        .agg(vlr_recebido=("vlr_recebido_num", "sum"), vlr_detalhado=("vlr_detalhado_num", "sum"))
    )
    out = pd.DataFrame()
    out["uo_cod"] = grouped["uo_beneficiada_cod"]
    out["uo_sigla"] = grouped["uo_beneficiada_sigla"]
    out["vlr_recebido"] = grouped["vlr_recebido"].apply(format_trim)
    out["vlr_detalhado"] = grouped["vlr_detalhado"].apply(format_trim)
    return out


# --------------------------------------------------------------------------
# 5) base_limite_cota  <-  orcamento_limite
# --------------------------------------------------------------------------

def transform_limite_cota():
    pre = read_pre("orcamento_limite")
    out = pd.DataFrame()
    out["uo_cod"] = pre["uo_cod"]
    out["uo"] = pre["uo_sigla"]
    out["grupo_cod"] = pre["grupo_cod"]
    out["fonte_cod"] = pre["fonte_cod"]
    out["ipu_cod"] = pre["ipu_cod"]
    out["iag_cod"] = pre["iag_cod"]
    out["vlr_limite_ano0"] = pre["vlr_limite"].apply(parse_trim)
    out["vlr_utilizado_ano0"] = ""
    out["vlr_transferido"] = ""
    out["vlr_limite_ano1"] = ""
    out["vlr_utilizado_ano1"] = ""
    out["vlr_limite_ano2"] = ""
    out["vlr_utilizado_ano2"] = ""
    out["vlr_limite_ano3"] = ""
    out["vlr_utilizado_ano3"] = ""
    return out


# --------------------------------------------------------------------------
# 6) base_orcam_receita_fiscal  <-  orcamento_receita
# --------------------------------------------------------------------------

def transform_orcam_receita_fiscal():
    pre = read_pre("orcamento_receita")
    out = pd.DataFrame()
    out["uo_cod"] = pre["uo_cod"]
    out["nome_uo"] = pre["uo_nome"]
    out["uo_sigla"] = pre["uo_sigla"]
    out["fonte_cod"] = pre["fonte_cod"]
    out["fonte_desc"] = ""
    out["interpretacao"] = ""
    out["categoria"] = pre["categoria_cod"]
    out["origem"] = pre["origem_cod"]
    out["especie"] = pre["especie_cod"]
    out["rubrica"] = pre["rubrica_cod"]
    out["alinea"] = pre["alinea_cod"]
    out["subalinea"] = pre["subalinea_cod"]
    out["tipo_receita"] = pre["receita_tipo_cod"]
    out["item"] = pre["item_cod"]
    out["subitem"] = pre["subitem_cod"]
    out["receita_cod"] = pre["receita_cod_fmt"].str.replace(".", "", regex=False)
    out["receita_desc"] = pre["receita_desc"]
    out["interp_receita"] = ""
    out["vlr_loa_rec_uo"] = ""
    out["vlr_loa_rec_scppo"] = ""
    out["vlr_loa_rec"] = pre["vlr_loa_rec"].apply(parse_money)
    out["ano"] = pre["ano"]
    out["base_legal"] = ""
    out["metodologia_de_calculo_e_premissas_utilizadas"] = pre["metodologia"]
    return out


# --------------------------------------------------------------------------
# 7) base_orcam_receita_investimento  <-  orcamento_receita_investimento
# --------------------------------------------------------------------------

def transform_orcam_receita_investimento():
    pre = read_pre("orcamento_receita_investimento")
    out = pd.DataFrame()
    out["uo_cod"] = pre["uo_cod"]
    out["uo_nome"] = pre["uo_nome"]
    out["uo_sigla"] = pre["uo_sigla"]
    out["categoria"] = ""
    out["subcategoria"] = ""
    out["alinea"] = ""
    out["subalinea"] = ""
    out["cod_receita"] = ""
    out["nivel_origem"] = ""
    out["receita"] = ""
    out["vlr_loa_rec_uo_invest"] = ""
    out["vlr_loa_rec_scppo_invest"] = ""
    out["vlr_loa_rec_invest"] = pre["vlr_loa_rec_invest"].apply(parse_money)
    out["ano"] = pre["ano"]
    return out


# --------------------------------------------------------------------------
# 8) base_orcam_despesa_item_fiscal  <-  orcamento_despesa (nível item, 1:1)
# --------------------------------------------------------------------------

def transform_orcam_despesa_item_fiscal():
    pre = read_pre("orcamento_despesa")
    out = pd.DataFrame()
    out["orgao_cod"] = pre["orgao_cod"]
    out["orgao_nome_sigla"] = [cod_nome(o, u) for o, u in zip(pre["orgao_nome"], pre["uo_sigla"])]
    out["uo_cod"] = pre["uo_cod"]
    out["uo_nome_sigla"] = [cod_nome(n, s) for n, s in zip(pre["uo_nome"], pre["uo_sigla"])]
    out["funcao_cod"] = pre["funcao_cod"]
    out["subfuncao_cod"] = pre["subfuncao_cod"]
    out["programa_cod"] = pre["programa_cod"]
    out["identificador_tipo_acao_cod"] = pre["identificador_cod"]
    out["projeto_atividade_cod"] = pre["projeto_atividade_cod"].apply(strip_leading_zero_int)
    out["acao_cod"] = pre["acao_cod"]
    out["subprojeto_subatividade_cod"] = pre["subprojeto_cod"].apply(strip_leading_zero_int)
    out["categoria_cod"] = pre["categoria_cod"]
    out["grupo_cod"] = pre["grupo_cod"]
    out["modalidade_cod"] = pre["modalidade_cod"]
    out["elemento_cod"] = pre["elemento_cod"]
    out["item_cod"] = pre["item_cod"]
    out["fonte_cod"] = pre["fonte_cod"]
    out["ipu_cod"] = pre["ipu_cod"]
    out["iag_cod"] = pre["iag_cod"]
    out["acao_desc"] = pre["acao_desc"]
    out["vlr_loa_desp"] = pre["vlr_loa_desp"].apply(parse_trim)
    return out


# --------------------------------------------------------------------------
# 9) base_qdd_fiscal  <-  orcamento_despesa (agregado por natureza, sem item)
# --------------------------------------------------------------------------

def transform_qdd_fiscal():
    pre = read_pre("orcamento_despesa")
    df = pre.copy()
    df["vlr_loa_desp_num"] = df["vlr_loa_desp"].apply(parse_br_number).fillna(0.0)

    group_cols = [
        "ano", "poder_cod", "orgao_cod", "orgao_nome", "uo_cod", "uo_nome", "uo_sigla",
        "funcao_cod", "subfuncao_cod", "programa_cod", "programa_desc", "acao_cod",
        "identificador_cod", "projeto_atividade_cod", "acao_desc", "subprojeto_cod",
        "categoria_cod", "grupo_cod", "modalidade_cod", "elemento_cod", "iag_cod",
        "fonte_cod", "ipu_cod",
    ]
    grouped = df.groupby(group_cols, as_index=False)["vlr_loa_desp_num"].sum()

    out = pd.DataFrame()
    out["ano"] = grouped["ano"]
    out["orgao_cod"] = grouped["orgao_cod"]
    out["orgao_nome_sigla"] = [cod_nome(o, u) for o, u in zip(grouped["orgao_nome"], grouped["uo_sigla"])]
    out["poder_cod"] = grouped["poder_cod"]
    out["situacao"] = ""
    out["uo_cod"] = grouped["uo_cod"]
    out["uo_nome_sigla"] = [cod_nome(n, s) for n, s in zip(grouped["uo_nome"], grouped["uo_sigla"])]
    out["categoria_cod"] = grouped["categoria_cod"]
    out["grupo_cod"] = grouped["grupo_cod"]
    out["modalidade_cod"] = grouped["modalidade_cod"]
    out["elemento_cod"] = grouped["elemento_cod"]
    out["fonte_cod"] = grouped["fonte_cod"]
    out["ipu_cod"] = grouped["ipu_cod"]
    out["seq_progtrab"] = ""
    out["funcao_cod"] = grouped["funcao_cod"]
    out["subfuncao_cod"] = grouped["subfuncao_cod"]
    out["programa_cod"] = grouped["programa_cod"]
    out["identificador_tipo_acao_cod"] = grouped["identificador_cod"]
    out["projeto_atividade_cod"] = grouped["projeto_atividade_cod"].apply(strip_leading_zero_int)
    out["acao_cod"] = grouped["acao_cod"]
    out["subprojeto_subatividade_cod"] = grouped["subprojeto_cod"].apply(strip_leading_zero_int)
    out["vlr_loa_desp_uo"] = ""
    out["vlr_loa_desp_scppo"] = ""
    out["vlr_loa_desp"] = grouped["vlr_loa_desp_num"].apply(format_money)
    out["iag_cod"] = grouped["iag_cod"]
    out["acao_desc"] = grouped["acao_desc"]
    out["programa_desc"] = grouped["programa_desc"]
    return out


# --------------------------------------------------------------------------
# 10) base_orcam_despesa_investimento  <-  orcamento_despesa_investimento
# --------------------------------------------------------------------------

def transform_orcam_despesa_investimento():
    pre = read_pre("orcamento_despesa_investimento")
    out = pd.DataFrame()
    out["orgao_cod"] = pre["orgao_cod"]
    out["orgao_nome_sigla"] = [cod_nome(o, u) for o, u in zip(pre["orgao_nome"], pre["uo_sigla"])]
    out["uo_cod"] = pre["uo_cod"]
    out["uo_nome_sigla"] = [cod_nome(n, s) for n, s in zip(pre["uo_nome"], pre["uo_sigla"])]
    out["funcao_cod"] = pre["funcao_cod"]
    out["subfuncao_cod"] = pre["subfuncao_cod"]
    out["programa_cod"] = pre["programa_cod"]
    out["identificador"] = pre["identificador_cod"]
    out["projeto_atividade"] = pre["projeto_atividade_cod"].apply(strip_leading_zero_int)
    out["acao_cod"] = pre["acao_cod"]
    out["subprojeto_cod"] = pre["subprojeto_cod"].apply(strip_leading_zero_int)
    out["fonte_cod"] = pre["fonte_invest_cod"]
    out["iag_cod"] = pre["iag_cod"]
    out["descricao"] = pre["acao_desc"]
    out["categoria_cod"] = pre["categoria_invest_cod"]
    out["natureza_cod"] = pre["natureza_invest_cod"]
    out["natureza"] = ""
    out["vlr_loa_desp_invest_ano0"] = pre["vlr_loa_desp"].apply(parse_trim)
    for col in ["vlr_loa_desp_invest_ano1", "vlr_loa_desp_invest_ano2", "vlr_loa_desp_invest_ano3"]:
        out[col] = ""
    return out


# --------------------------------------------------------------------------
# 11) base_qdd_investimento  <-  orcamento_despesa_investimento
# --------------------------------------------------------------------------

def transform_qdd_investimento():
    pre = read_pre("orcamento_despesa_investimento")
    out = pd.DataFrame()
    out["ano"] = pre["ano"]
    out["orgao_cod"] = pre["orgao_cod"]
    out["orgao_nome_sigla"] = [cod_nome(o, u) for o, u in zip(pre["orgao_nome"], pre["uo_sigla"])]
    out["poder_cod"] = pre["poder_cod"]
    out["uo_cod"] = pre["uo_cod"]
    out["uo_nome_sigla"] = [cod_nome(n, s) for n, s in zip(pre["uo_nome"], pre["uo_sigla"])]
    out["seq_progtrab"] = ""
    out["funcao_cod"] = pre["funcao_cod"]
    out["subfuncao_cod"] = pre["subfuncao_cod"]
    out["programa_cod"] = pre["programa_cod"]
    out["ident_projativ"] = pre["identificador_cod"]
    out["proj_ativ"] = pre["projeto_atividade_cod"].apply(strip_leading_zero_int)
    out["acao_cod"] = pre["acao_cod"]
    out["vlr_loa_desp_invest"] = pre["vlr_loa_desp"].apply(parse_trim)
    out["iag_cod"] = pre["iag_cod"]
    out["desc_projeto_ativ"] = pre["acao_desc"]
    out["categoria_cod"] = pre["categoria_invest_cod"]
    out["natureza_cod"] = pre["natureza_invest_cod"]
    out["natureza"] = ""
    out["fonte_cod"] = pre["fonte_invest_cod"]
    out["fonte"] = pre["fonte_invest_desc"]
    out["acao_desc"] = pre["acao_desc"]
    out["programa_desc"] = pre["programa_desc"]
    return out


# --------------------------------------------------------------------------
# 12) base_repasse_recursos  <-  orcamento_repasse
# --------------------------------------------------------------------------

def transform_repasse_recursos():
    pre = read_pre("orcamento_repasse")
    out = pd.DataFrame()
    out["uo_financiadora_cod"] = pre["uo_financiadora_cod"]
    out["uo_financiadora_nome"] = pre["uo_financiadora_nome"]
    out["uo_beneficiada_cod"] = pre["uo_beneficiada_cod"]
    out["uo_beneficiada_nome"] = pre["uo_beneficiada_nome"]
    out["grupo_cod"] = pre["grupo_cod"]
    out["fonte_cod"] = pre["fonte_cod"]
    out["ipu_cod"] = pre["ipu_cod"]
    out["iag_cod"] = pre["iag_cod"]
    out["vlr_repasse"] = pre["vlr_repasse"].apply(parse_money)
    return out


# --------------------------------------------------------------------------
# 13) acoes_planejamento  <-  planejamento_acao
# --------------------------------------------------------------------------

def transform_acoes_planejamento():
    pre = read_pre("planejamento_acao")
    out = pd.DataFrame()
    out["programa_cod"] = pre["programa_cod"]
    out["programa_desc"] = pre["programa_desc"]
    out["area_tematica_cod"] = pre["area_tematica_cod"]
    out["area_tematica_desc"] = pre["area_tematica_desc"]
    out["is_deleted_programa"] = pre["programa_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["is_new_programa"] = pre["programa_novo"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["justificativa_is_new_programa"] = pre["programa_justificativa_inclusao"]
    out["uo_programa_cod"] = pre["uo_programa_cod"]
    out["uo_programa_nome"] = pre["uo_programa_nome"]
    out["uo_acao_cod"] = pre["uo_acao_cod"]
    out["uo_acao_nome"] = pre["uo_acao_nome"]
    out["funcao_cod"] = pre["funcao_cod"]
    out["funcao_desc"] = pre["funcao_desc"]
    out["subfuncao_cod"] = pre["subfuncao_cod"]
    out["subfuncao_desc"] = pre["subfuncao_desc"]
    out["identificador_tipo_acao_cod"] = pre["identificador_cod"]
    out["identificador_tipo_acao_desc"] = pre["identificador_desc"]
    out["acao_cod"] = pre["acao_cod"]
    out["acao_desc"] = pre["acao_desc"]
    out["iag_cod"] = pre["iag_cod"]
    out["iag_desc"] = pre["iag_desc"]
    out["projeto_estrategico_cod"] = pre["projeto_estrategico_cod"]
    out["projeto_estrategico"] = pre["projeto_estrategico_desc"]
    out["is_deleted_acao"] = pre["acao_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["is_new_acao"] = pre["acao_novo"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["justificativa_is_new_acao"] = pre["acao_justificativa_inclusao"]
    out["is_transferida_sisor"] = ""
    out["ua_acao_nome"] = pre["ua_acao_nome"]
    out["base_legal"] = pre["base_legal"]
    out["acao_finalidade"] = pre["acao_finalidade"]
    out["acao_descricao"] = pre["acao_descricao"]
    out["publico_alvo_cod"] = pre["publico_alvo_cod"]
    out["publico_alvo_desc"] = pre["publico_alvo_desc"]
    out["produto_cod"] = pre["produto_cod"]
    out["produto_desc"] = pre["produto_desc"]
    out["produto_especificacao"] = pre["produto_especificacao"]
    out["produto_unidade_medida_cod"] = pre["unidade_medida_cod"]
    out["produto_unidade_medida_desc"] = pre["unidade_medida_desc"]
    for i in range(4):
        out[f"vr_meta_orcamentaria_ano{i}"] = pre[f"vlr_meta_orcamentaria_ano{i}"].apply(parse_trim)
        out[f"vr_meta_fisica_ano{i}"] = pre[f"vlr_meta_fisica_ano{i}"].apply(parse_trim)
    out["is_acao_transposta"] = ""
    out["setor_governo"] = pre["governo_setor"]
    out["politica_mulheres"] = pre["politica_mulheres"]
    return out


# --------------------------------------------------------------------------
# 14) indicadores_planejamento  <-  planejamento_indicador
# --------------------------------------------------------------------------

def transform_indicadores_planejamento():
    pre = read_pre("planejamento_indicador")
    out = pd.DataFrame()
    out["programa_cod"] = pre["programa_cod"]
    out["programa_nome"] = pre["programa_desc"]
    out["is_deleted_programa"] = pre["programa_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["indicador"] = pre["indicador_desc"]
    out["is_deleted_indicador"] = pre["indicador_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["unidade_de_medida"] = pre["unidade_medida_desc"]
    out["indice_de_referencia"] = pre["indice_referencia"]
    out["is_em_apuracao_indice_de_referencia"] = pre["indice_referencia_apuracao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["dt_apuracao"] = pre["indice_referencia_data_apuracao"]
    for i in range(4):
        out[f"previsao_para_ano{i}"] = pre[f"previsao_ano{i}"].apply(parse_trim)
        out[f"is_em_apuracao_ano{i}"] = pre[f"apuracao_ano{i}"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["fonte"] = pre["fonte_desc"]
    out["periodicidade"] = pre["periodicidade"]
    out["base_geografica"] = pre["base_geografica"]
    out["formula_de_calculo"] = pre["formula_calculo"]
    justs = pre[[f"previsao_apuracao_justificativa_ano{i}" for i in range(4)]]
    out["justificativa_status_apuracao_previsoes"] = justs.apply(
        lambda row: next((v for v in row if str(v).strip() != ""), ""), axis=1
    )
    out["justificativa_status_apuracao_indice_ref"] = pre["indice_referencia_apuracao_justificativa"]
    out["updated_at"] = ""
    out["is_indicador_new"] = pre["indicador_novo"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["polaridade"] = pre["polaridade"]
    return out


# --------------------------------------------------------------------------
# 15) localizadores_todos_planejamento  <-  planejamento_localizador
# --------------------------------------------------------------------------

def transform_localizadores_todos_planejamento():
    pre = read_pre("planejamento_localizador")
    out = pd.DataFrame()
    out["programa_cod"] = pre["programa_cod"]
    out["programa_desc"] = pre["programa_desc"]
    out["area_tematica_cod"] = pre["area_tematica_cod"]
    out["area_tematica_desc"] = pre["area_tematica_desc"]
    out["is_deleted_programa"] = pre["programa_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["acao_cod"] = pre["acao_cod"]
    out["acao_desc"] = pre["acao_desc"]
    out["iag_cod"] = pre["iag_cod"]
    out["iag_desc"] = pre["iag_desc"]
    out["projeto_estrategico_cod"] = pre["projeto_estrategico_cod"]
    out["projeto_estrategico_desc"] = pre["projeto_estrategico_desc"]
    out["funcao_cod"] = pre["funcao_cod"]
    out["funcao_desc"] = pre["funcao_desc"]
    out["subfuncao_cod"] = pre["subfuncao_cod"]
    out["subfuncao_desc"] = pre["subfuncao_desc"]
    out["uo_acao_cod"] = pre["uo_acao_cod"]
    out["uo_acao_nome"] = pre["uo_acao_nome"]
    out["is_deleted_acao"] = pre["acao_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["localizador_cod"] = ""
    out["is_deleted_localizador"] = ""
    out["regiao_geografica_cod"] = pre["regiao_geografica_intermediaria_cod"]
    out["regiao_geografica_desc"] = pre["regiao_geografica_intermediaria_desc"]
    out["municipio_ibge_cod"] = pre["municipio_ibge_cod"]
    out["municipio_sigplan_cod"] = pre["municipio_sigplan_cod"]
    out["municipio"] = pre["municipio_desc"]
    for i in range(4):
        out[f"vr_meta_orcamentaria_ano{i}"] = pre[f"vlr_meta_orcamentaria_ano{i}"].apply(parse_trim)
        out[f"vr_meta_fisica_ano{i}"] = pre[f"vlr_meta_fisica_ano{i}"].apply(parse_trim)
    return out


# --------------------------------------------------------------------------
# 16) programas_planejamento  <-  planejamento_programa
# --------------------------------------------------------------------------

def transform_programas_planejamento():
    pre = read_pre("planejamento_programa")
    out = pd.DataFrame()
    out["programa_cod"] = pre["programa_cod"]
    out["programa_desc"] = pre["programa_desc"]
    out["is_deleted_programa"] = pre["programa_exclusao"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["is_new_programa"] = pre["programa_novo"].map(SIM_NAO_BOOL_MAP).fillna("")
    out["area_tematica_cod"] = pre["area_tematica_cod"]
    out["area_tematica_desc"] = pre["area_tematica_desc"]
    out["objetivo_estrategico_cod"] = pre["objetivo_estrategico_cod"]
    out["objetivo_estrategico_desc"] = pre["objetivo_estrategico_desc"]
    out["diretriz_estrategica_cod"] = pre["diretriz_estrategica_cod"]
    out["diretriz_estrategica_desc"] = pre["diretriz_estrategica_desc"]
    out["justificativa_is_new_programa"] = pre["programa_justificativa_inclusao"]
    out["orgao_programa_cod"] = pre["orgao_programa_cod"]
    out["orgao_programa_nome"] = pre["orgao_programa_nome"]
    out["uo_programa_cod"] = pre["uo_programa_cod"]
    out["uo_programa_nome"] = pre["uo_programa_nome"]
    out["objetivo"] = pre["programa_objetivo"]
    out["justificativa"] = pre["programa_justificativa"]
    out["tipo_de_programa"] = pre["tipo_de_programa"]
    out["horizonte_temporal"] = pre["horizonte_temporal"]
    out["estrategia_de_implementacao"] = pre["estrategia_implementacao"]
    out["ua_programa_nome"] = pre["ua_programa_nome"]
    for i in range(4):
        out[f"vr_meta_orcamentaria_ano{i}"] = pre[f"vlr_meta_orcamentaria_ano{i}"].apply(parse_trim)
    out["is_programa_transposto"] = ""
    out["causas"] = pre["causas"]
    out["ods_titulo"] = pre["ods_titulo"]
    out["ods_subtitulo"] = ""
    return out


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

TRANSFORMS = {
    "base_categoria_pessoal": transform_categoria_pessoal,
    "base_detalhamento_obras": transform_detalhamento_obras,
    "base_intra_orcamentaria_repasse": transform_intra_orcamentaria_repasse,
    "base_intra_orcamentaria_detalhamento": transform_intra_orcamentaria_detalhamento,
    "base_limite_cota": transform_limite_cota,
    "base_orcam_receita_fiscal": transform_orcam_receita_fiscal,
    "base_orcam_receita_investimento": transform_orcam_receita_investimento,
    "base_orcam_despesa_item_fiscal": transform_orcam_despesa_item_fiscal,
    "base_qdd_fiscal": transform_qdd_fiscal,
    "base_orcam_despesa_investimento": transform_orcam_despesa_investimento,
    "base_qdd_investimento": transform_qdd_investimento,
    "base_repasse_recursos": transform_repasse_recursos,
    "acoes_planejamento": transform_acoes_planejamento,
    "indicadores_planejamento": transform_indicadores_planejamento,
    "localizadores_todos_planejamento": transform_localizadores_todos_planejamento,
    "programas_planejamento": transform_programas_planejamento,
}


def build_datapackage():
    resource_descriptors = []
    for csv_path in sorted(OUT_DIR.glob("*.csv")):
        name = csv_path.stem
        probe = Resource(str(csv_path))
        probe.infer()
        fields = [{"name": field.name, "type": field.type} for field in probe.schema.fields]
        resource_descriptors.append({
            "profile": "tabular-data-resource",
            "name": name,
            "title": name,
            "path": f"data/{name}.csv",
            "scheme": "file",
            "format": "csv",
            "mediatype": "text/csv",
            "encoding": "utf-8",
            "schema": {"fields": fields},
        })

    target_descriptor = {
        "profile": "tabular-data-package",
        "name": "dados_ppo_2027",
        "title": "Portal de Planejamento e Orçamento - PPO-MG",
        "owner_org": "secretaria-de-estado-de-planejamento-e-gestao-seplag",
        "dpetl_load": {
            "owner": "splor-mg",
            "repo": "dados-ppo-2027",
            "level": "orgs",
            "visibility": "public",
        },
        "resources": resource_descriptors,
    }

    target = Package.from_descriptor(target_descriptor, basepath=str(BASE_DIR))
    target.custom["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for resource in target.resources:
        resource.infer(stats=True)

    target.to_json(str(DATAPACKAGE_PATH))
    print(f"OK  datapackage.json  ({len(target.resources)} resources) -> {DATAPACKAGE_PATH}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    empty_col_report = {}

    for out_name, fn in TRANSFORMS.items():
        try:
            df = fn()
        except FileNotFoundError as e:
            print(f"[AVISO] Pulando {out_name}: {e}")
            continue

        dest = OUT_DIR / f"{out_name}.csv"
        df.to_csv(dest, index=False)
        print(f"OK  {out_name}.csv  ({len(df)} linhas, {len(df.columns)} colunas) -> {dest}")

        empties = [c for c in df.columns if df[c].astype(str).str.strip().eq("").all()]
        if empties:
            empty_col_report[out_name] = empties

    if empty_col_report:
        print("\n=== Colunas de saída sem dado equivalente em data_pre (ficaram vazias) ===")
        for name, cols in empty_col_report.items():
            print(f"- {name}: {', '.join(cols)}")

    build_datapackage()


if __name__ == "__main__":
    main()
