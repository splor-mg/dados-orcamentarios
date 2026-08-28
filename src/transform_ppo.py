import re
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
    'R$ 1.234,56') para float. Retorna None se vazio."""
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


def as_int(series: pd.Series) -> pd.Series:
    """Converte uma série de códigos (dígitos em texto) para inteiro
    anulável do pandas (Int64). Vazio vira <NA> (célula vazia no Excel)."""
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def as_num(series: pd.Series) -> pd.Series:
    """Converte uma série de valores no formato BR para float. Vazio
    vira NaN (célula vazia no Excel)."""
    return series.apply(parse_br_number)


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


def format_trim(value):
    """Formata sem casas decimais desnecessárias: se o decimal for 0, não
    aparece ('1000.0' -> '1000'); se houver decimal real, mantém (sem
    arredondar), ex: '150.5' -> '150.5'. Usado só onde a saída ainda é
    texto (acoes_planejamento.txt)."""
    if value is None:
        return ""
    if value == int(value):
        return str(int(value))
    s = f"{value:.2f}".rstrip("0").rstrip(".")
    return s


def parse_trim(value):
    return format_trim(parse_br_number(value))


def sanitize_text(df: pd.DataFrame) -> pd.DataFrame:
    """Substitui quebras de linha embutidas, caracteres inválidos
    conhecidos e entidades HTML numéricas (ex: &#9642;) por
    equivalentes seguros. Só mexe em colunas que não são numéricas —
    funciona tanto pra dtype 'object' quanto pra dtype 'string' do
    pandas, ao contrário de comparar '== object' diretamente."""

    def clean(value):
        if not isinstance(value, str):
            return value
        s = re.sub(r"[\r\n\u2028\u2029\x0b\x0c\x85]+", " ", value)
        s = HTML_ENTITY_RE.sub(" ", s)
        for bad, good in INVALID_CHAR_MAP.items():
            s = s.replace(bad, good)
        return s

    out = df.copy()
    for col in out.columns:
        if not pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].apply(clean)
    return out


STATUS_OBRA_MAP = {
    "Iniciado": "INICIANDO",
    "Execução": "EXECUÇÃO",
    "Concluído": "CONCLUÍDO",
    "Paralisado": "PARALISADO",
    "Cancelado": "CANCELADO",
}

CATEGORIA_INVEST_MAP = {
    "4510": "PARTICIPAÇÃO SOCIETÁRIA",
    "4610": "IMOBILIZAÇÕES",
    "4710": "AMORTIZAÇÃO DE DÍVIDAS",
    "4810": "OUTRAS APLICAÇÕES",
}

UNIDADE_MEDIDA_MAP = {
    "207": "UNIDADE",
    "130": "METRO QUADRADO"
}

INVALID_CHAR_MAP = {
    "\x02": " ",
    "\u200b": " ",
    "\x95": "-",
    "\u202f": " ",
    "\x1a": " ",
    "\t": " ",
    "\u00a0": " ",
}

HTML_ENTITY_RE = re.compile(r"&#\d+;?")

SIM_NAO_MAP = {"S": "Sim", "N": "Não"}


# --------------------------------------------------------------------------
# 1) BASE_CATEGORIA_PESSOAL  <-  orcamento_pessoal
# --------------------------------------------------------------------------

def transform_categoria_pessoal():
    pre = read_pre("orcamento_pessoal")
    out = pd.DataFrame()
    out["Ano de Exercício"] = as_int(pre["ano"])
    out["UO"] = [cod_nome(c, s) for c, s in zip(pre["uo_cod"], pre["uo_sigla"])]
    out["Classificação"] = (
        pre["pessoal_classificacao"]
        .str.replace("PESSOAL ", "", regex=False)
        .str.title()
    )
    out["Categoria"] = pre["pessoal_categoria"]
    out["Quantidade"] = as_int(pre["pessoal_quantidade"])
    return out


# --------------------------------------------------------------------------
# 2) BASE_DETALHAMENTO_OBRAS  <-  orcamento_obras
# --------------------------------------------------------------------------

def transform_detalhamento_obras():
    pre = read_pre("orcamento_obras")
    out = pd.DataFrame()
    out["UO"] = as_int(pre["uo_cod"])
    out["FUNCAO"] = as_int(pre["funcao_cod"])
    out["SUBFUNCAO"] = as_int(pre["subfuncao_cod"])
    out["PROGRAMA"] = as_int(pre["programa_cod"])
    out["ACAO"] = as_int(pre["acao_cod"])
    out["SUBPROJETO"] = as_int(pre["subprojeto_cod"])
    out["IAG"] = as_int(pre["iag_cod"])
    out["NUMERO DA OBRA SISOR"] = pd.Series(range(1, len(pre) + 1), dtype="Int64")
    out["NUMERO DA OBRA SIAD"] = as_int(pre["obra_siad_cod"])
    out["DESCRICAO DA OBRA"] = pre["obra_desc"]
    out["STATUS DA OBRA"] = pre["obra_status"].map(STATUS_OBRA_MAP).fillna(
        pre["obra_status"].str.upper()
    )
    out["UNIDADE DE MEDIDA DA OBRA"] = pre["unidade_medida_cod"].astype(str).map(
        UNIDADE_MEDIDA_MAP).fillna(pre["unidade_medida_cod"].astype(str))
    out["QUANTIDADE"] = as_int(pre["obra_quantidade"])
    out["ALTERAR UNIDADE DE MEDIDA DA OBRA"] = pre["unidade_medida_alterar"].map(SIM_NAO_MAP).fillna("")
    out["REGIÃO GEOGRÁFICA INTERMEDIÁRIA"] = pre["regiao_geografica_intermediaria_desc"]
    out["MUNICÍPIO"] = pre["municipio_desc"]
    out["VALOR TESOURO 2026 (R$)"] = as_num(pre["vlr_tesouro"])
    out["VALOR OUTROS 2026 (R$)"] = as_num(pre["vlr_outros"])
    for col in ["VALOR TESOURO 2027 (R$)", "VALOR OUTROS 2027 (R$)",
                "VALOR TESOURO 2028 (R$)", "VALOR OUTROS 2028 (R$)",
                "VALOR TESOURO 2029 (R$)", "VALOR OUTROS 2029 (R$)"]:
        out[col] = pd.array([pd.NA] * len(pre), dtype="Float64")
    return out


# --------------------------------------------------------------------------
# 3) BASE_ORCAM_DESPESA_ITEM_FISCAL  <-  orcamento_despesa (nível item, 1:1)
# --------------------------------------------------------------------------

def transform_orcam_despesa_item_fiscal():
    pre = read_pre("orcamento_despesa")
    out = pd.DataFrame()
    out["Código do Órgão"] = as_int(pre["orgao_cod"])
    out["Órgão"] = [cod_nome(o, u) for o, u in zip(pre["orgao_nome"], pre["uo_sigla"])]
    out["Código da UO"] = as_int(pre["uo_cod"])
    out["Unidade Orçamentária"] = [cod_nome(n, s) for n, s in zip(pre["uo_nome"], pre["uo_sigla"])]
    out["Função"] = as_int(pre["funcao_cod"])
    out["Subfunção"] = as_int(pre["subfuncao_cod"])
    out["Programa"] = as_int(pre["programa_cod"])
    out["Identificador"] = as_int(pre["identificador_cod"])
    out["Projeto_Atividade"] = as_int(pre["projeto_atividade_cod"])
    out["Ação"] = as_int(pre["acao_cod"])
    out["Subprojeto"] = as_int(pre["subprojeto_cod"])
    out["Categoria"] = as_int(pre["categoria_cod"])
    out["Grupo_Despesa"] = as_int(pre["grupo_cod"])
    out["Modalidade"] = as_int(pre["modalidade_cod"])
    out["Elemento_Despesa"] = as_int(pre["elemento_cod"])
    out["Item_Despesa"] = as_int(pre["item_cod"])
    out["Fonte"] = as_int(pre["fonte_cod"])
    out["IPU"] = as_int(pre["ipu_cod"])
    out["IAG"] = as_int(pre["iag_cod"])
    out["Descrição"] = pre["acao_desc"]
    out["Valor (R$)"] = as_num(pre["vlr_loa_desp"])
    return out


# --------------------------------------------------------------------------
# 4) BASE_QDD_FISCAL  <-  orcamento_despesa (agregado por natureza, sem item)
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
    out["ANO"] = as_int(grouped["ano"])
    out["COD_ORGAO"] = as_int(grouped["orgao_cod"])
    out["ORGAO"] = [cod_nome(o, u) for o, u in zip(grouped["orgao_nome"], grouped["uo_sigla"])]
    out["PODER"] = as_int(grouped["poder_cod"])
    out["SITUACAO"] = pd.array([pd.NA] * len(grouped), dtype="Int64")
    out["COD_UO"] = as_int(grouped["uo_cod"])
    out["UO"] = [cod_nome(n, s) for n, s in zip(grouped["uo_nome"], grouped["uo_sigla"])]
    out["CATEGORIA"] = as_int(grouped["categoria_cod"])
    out["GRUPO_DESPESA"] = as_int(grouped["grupo_cod"])
    out["MODALIDADE"] = as_int(grouped["modalidade_cod"])
    out["ELEMENTO_DESPESA"] = as_int(grouped["elemento_cod"])
    out["FONTE"] = as_int(grouped["fonte_cod"])
    out["IPU"] = as_int(grouped["ipu_cod"])
    out["SEQ_PROGTRAB"] = pd.array([pd.NA] * len(grouped), dtype="Int64")
    out["FUNCAO"] = as_int(grouped["funcao_cod"])
    out["SUB_FUNCAO"] = as_int(grouped["subfuncao_cod"])
    out["PROGRAMA"] = as_int(grouped["programa_cod"])
    out["IDENT_PROJATIV"] = as_int(grouped["identificador_cod"])
    out["PROJ_ATIV"] = as_int(grouped["projeto_atividade_cod"])
    out["AÇÃO"] = as_int(grouped["acao_cod"])
    out["SUB_PROJETO"] = as_int(grouped["subprojeto_cod"])
    out["VALOR UO (R$)"] = pd.array([pd.NA] * len(grouped), dtype="Float64")
    out["VALOR SCPPO (R$)"] = pd.array([pd.NA] * len(grouped), dtype="Float64")
    out["VALOR FINAL (R$)"] = grouped["vlr_loa_desp_num"]
    out["IAG"] = as_int(grouped["iag_cod"])
    out["NOME_ACAO"] = grouped["acao_desc"]
    out["NOME_PROGRAMA"] = grouped["programa_desc"]
    return out


# --------------------------------------------------------------------------
# 5) BASE_QDD_INVESTIMENTO  <-  orcamento_despesa_investimento
# --------------------------------------------------------------------------

def transform_qdd_investimento():
    pre = read_pre("orcamento_despesa_investimento")
    out = pd.DataFrame()
    out["ANO"] = as_int(pre["ano"])
    out["COD_ORGAO"] = as_int(pre["orgao_cod"])
    out["ORGAO"] = [cod_nome(o, u) for o, u in zip(pre["orgao_nome"], pre["uo_sigla"])]
    out["PODER"] = as_int(pre["poder_cod"])
    out["COD_UO"] = as_int(pre["uo_cod"])
    out["UO"] = [cod_nome(n, s) for n, s in zip(pre["uo_nome"], pre["uo_sigla"])]
    out["SEQ_PROGTRAB"] = pd.array([pd.NA] * len(pre), dtype="Int64")
    out["FUNCAO"] = as_int(pre["funcao_cod"])
    out["SUB_FUNCAO"] = as_int(pre["subfuncao_cod"])
    out["PROGRAMA"] = as_int(pre["programa_cod"])
    out["IDENT_PROJATIV"] = as_int(pre["identificador_cod"])
    out["PROJ_ATIV"] = as_int(pre["projeto_atividade_cod"])
    out["AÇÃO"] = as_int(pre["acao_cod"])
    out["VALOR (R$)"] = as_num(pre["vlr_loa_desp"])
    out["IAG"] = as_int(pre["iag_cod"])
    out["DESC_PROJETO_ATIV"] = pre["acao_desc"]
    out["CATEGORIA"] = pre["categoria_invest_cod"].map(
        lambda x: f"{x} - {CATEGORIA_INVEST_MAP.get(x, '')}" if x else ""
    )
    out["COD_NATUREZA"] = as_int(pre["natureza_invest_cod"])
    out["NATUREZA"] = ""
    out["COD_FONTE"] = as_int(pre["fonte_invest_cod"])
    out["FONTE"] = pre["fonte_invest_desc"]
    out["NOME_ACAO"] = pre["acao_desc"]
    out["NOME_PROGRAMA"] = pre["programa_desc"]
    return out


# --------------------------------------------------------------------------
# 6) BASE_ORCAM_RECEITA_FISCAL  <-  orcamento_receita
# --------------------------------------------------------------------------

def transform_orcam_receita_fiscal():
    pre = read_pre("orcamento_receita")
    out = pd.DataFrame()
    out["UO_COD"] = as_int(pre["uo_cod"])
    out["NOME_UO"] = pre["uo_nome"]
    out["SIGLA_UO"] = pre["uo_sigla"]
    out["COD_FONTE"] = as_int(pre["fonte_cod"])
    out["FONTE"] = ""
    out["INTERPRETACAO"] = ""
    out["CATEGORIA"] = as_int(pre["categoria_cod"])
    out["ORIGEM"] = as_int(pre["origem_cod"])
    out["ESPECIE"] = as_int(pre["especie_cod"])
    out["RUBRICA"] = as_int(pre["rubrica_cod"])
    out["ALINEA"] = as_int(pre["alinea_cod"])
    out["SUBALINEA"] = as_int(pre["subalinea_cod"])
    out["TIPO_RECEITA"] = as_int(pre["receita_tipo_cod"])
    out["ITEM"] = as_int(pre["item_cod"])
    out["SUBITEM"] = as_int(pre["subitem_cod"])
    out["COD_RECEITA"] = as_int(pre["receita_cod_fmt"].str.replace(".", "", regex=False))
    out["RECEITA"] = pre["receita_desc"]
    out["INTERP_RECEITA"] = ""
    out["VALOR UO (R$)"] = pd.array([pd.NA] * len(pre), dtype="Float64")
    out["VALOR SCPPO (R$)"] = pd.array([pd.NA] * len(pre), dtype="Float64")
    out["VALOR FINAL (R$)"] = as_num(pre["vlr_loa_rec"])
    out["ANO"] = as_int(pre["ano"])
    out["BASE LEGAL"] = "-"
    out["METODOLOGIA DE CÁLCULO E PREMISSAS UTILIZADAS"] = pre["metodologia"]
    return out


# --------------------------------------------------------------------------
# 7) BASE_REPASSE_RECURSOS  <-  orcamento_repasse
# --------------------------------------------------------------------------

def transform_repasse_recursos():
    pre = read_pre("orcamento_repasse")
    out = pd.DataFrame()
    out["Cód. UO Financiadora"] = as_int(pre["uo_financiadora_cod"])
    out["UO Financiadora"] = pre["uo_financiadora_nome"]
    out["Cód. UO Beneficiada"] = as_int(pre["uo_beneficiada_cod"])
    out["UO Beneficiada"] = pre["uo_beneficiada_nome"]
    out["Grupo de Despesa"] = as_int(pre["grupo_cod"])
    out["Fonte"] = as_int(pre["fonte_cod"])
    out["IPU"] = as_int(pre["ipu_cod"])
    out["IAG"] = as_int(pre["iag_cod"])
    out["Valor Transferido (R$)"] = as_num(pre["vlr_repasse"])
    return out


# --------------------------------------------------------------------------
# 8) acoes_planejamento  <-  planejamento_acao
# --------------------------------------------------------------------------

def transform_acoes_planejamento():
    pre = read_pre("planejamento_acao")
    out = pd.DataFrame()
    out["Código do Programa"] = pre["programa_cod"].str.zfill(4)
    out["Nome do Programa"] = pre["programa_desc"]
    out["Código da Área Temática"] = pre["area_tematica_cod"]
    out["Área Temática"] = pre["area_tematica_desc"]
    out["Exclusão Lógica do Programa"] = pre["programa_exclusao"]
    out["Programa Novo"] = pre["programa_novo"]
    out["Justificativa de Inclusão ou Exclusão do Programa"] = pre["programa_justificativa_inclusao"]
    out["Código da Unidade Orçamentária Responsável pelo Programa"] = pre["uo_programa_cod"]
    out["Unidade Orçamentária Responsável pelo Programa"] = pre["uo_programa_nome"]
    out["Código da Unidade Orçamentária Responsável pela Ação"] = pre["uo_acao_cod"]
    out["Unidade Orçamentária Responsável pela Ação"] = pre["uo_acao_nome"]
    out["Código da Função"] = pre["funcao_cod"]
    out["Função"] = pre["funcao_desc"]
    out["Código da Subfunção"] = pre["subfuncao_cod"]
    out["Subfunção"] = pre["subfuncao_desc"]
    out["Código do Tipo de Ação"] = pre["identificador_cod"]
    out["Tipo de Ação"] = pre["identificador_desc"]
    out["Código da Ação"] = pre["acao_cod"]
    out["Título da Ação"] = pre["acao_desc"]
    out["Código do Identificador de Ação Governamental (IAG)"] = pre["iag_cod"]
    out["Identificador de Ação Governamental (IAG)"] = pre["iag_desc"]
    out["Código do Projeto Estratégico"] = pre["projeto_estrategico_cod"]
    out["Projeto Estratégico"] = pre["projeto_estrategico_desc"]
    out["Exclusão Lógica da Ação"] = pre["acao_exclusao"]
    out["Nova Ação"] = pre["acao_novo"]
    out["Justificativa de Inclusão ou Exclusão da Ação"] = pre["acao_justificativa_inclusao"]
    out["Transferida para o SISOR"] = ""
    out["Unidade Administrativa Responsável pela Ação"] = pre["ua_acao_nome"]
    out["Base legal"] = pre["base_legal"]
    out["Finalidade da Ação"] = pre["acao_finalidade"]
    out["Descrição da Ação"] = pre["acao_descricao"]
    out["Código do Público-alvo"] = pre["publico_alvo_cod"]
    out["Público-Alvo"] = pre["publico_alvo_desc"]
    out["Código do Produto"] = pre["produto_cod"]
    out["Produto"] = pre["produto_desc"]
    out["Especificação do Produto"] = pre["produto_especificacao"]
    out["Código da Unidade de Medida do Produto"] = pre["unidade_medida_cod"]
    out["Unidade de Medida do Produto"] = pre["unidade_medida_desc"]
    for ano_label, i in zip(["2026", "2027", "2028", "2029"], range(4)):
        out[f"Previsão Orçamentária {ano_label}"] = pre[f"vlr_meta_orcamentaria_ano{i}"].apply(parse_trim)
    for ano_label, i in zip(["2026", "2027", "2028", "2029"], range(4)):
        out[f"Previsão Física {ano_label}"] = pre[f"vlr_meta_fisica_ano{i}"].apply(parse_trim)
    out["Ação Transposta"] = ""
    out["Setor de Governo"] = pre["governo_setor"]
    out["Política para mulheres"] = pre["politica_mulheres"]
    return out


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

TRANSFORMS = {
    "BASE_CATEGORIA_PESSOAL": transform_categoria_pessoal,
    "BASE_DETALHAMENTO_OBRAS": transform_detalhamento_obras,
    "BASE_ORCAM_DESPESA_ITEM_FISCAL": transform_orcam_despesa_item_fiscal,
    "BASE_ORCAM_RECEITA_FISCAL": transform_orcam_receita_fiscal,
    "BASE_QDD_FISCAL": transform_qdd_fiscal,
    "BASE_QDD_INVESTIMENTO": transform_qdd_investimento,
    "BASE_REPASSE_RECURSOS": transform_repasse_recursos,
    "acoes_planejamento": transform_acoes_planejamento,
}

OUTPUT_OVERRIDES = {
    "acoes_planejamento": {"filename": "acoes_planejamento.txt", "sep": "|", "format": "txt"},
}


def write_output(name: str, df: pd.DataFrame) -> Path:
    override = OUTPUT_OVERRIDES.get(name, {})
    fmt = override.get("format", "xlsx")
    filename = override.get("filename", f"{name}.xlsx")
    dest = OUT_DIR / filename

    if fmt == "xlsx":
        df.to_excel(dest, index=False, engine="openpyxl")
    else:
        sep = override.get("sep", ",")
        df.to_csv(dest, index=False, sep=sep, encoding='utf-8')
    return dest


def build_datapackage():
    output_files = sorted(OUT_DIR.glob("*.xlsx")) + sorted(OUT_DIR.glob("*.txt"))
    resource_descriptors = []

    for file_path in output_files:
        name = file_path.stem.lower()
        ext = file_path.suffix.lstrip(".")

        if ext == "xlsx":
            probe_descriptor = {
                "name": name,
                "path": f"data/{file_path.name}",
                "format": "xlsx",
            }
            probe = Resource.from_descriptor(probe_descriptor, basepath=str(BASE_DIR))
            probe.infer(stats=True)
            fields = probe.schema.to_dict().get("fields", [])

            if name == "base_detalhamento_obras":
                for field in fields:
                    if field["name"] == "QUANTIDADE":
                        field["type"] = "integer"

                    if field["name"] == "UNIDADE DE MEDIDA DA OBRA":
                        field["type"] = "string"

            descriptor = {
                "profile": "tabular-data-resource",
                "name": name,
                "title": name,
                "path": f"data/{file_path.name}",
                "scheme": "file",
                "format": "xlsx",
                "mediatype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "schema": {"fields": fields},
            }

        else:
            sep = OUTPUT_OVERRIDES.get(name, {}).get("sep", ",")
            try:
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    header_line = f.readline().rstrip('\r\n')
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    header_line = f.readline().rstrip('\r\n')
            field_names = [fn.strip() for fn in header_line.split(sep)]
            fields = [{"name": fn} for fn in field_names]

            descriptor = {
                "profile": "tabular-data-resource",
                "name": name,
                "title": name,
                "path": f"data/{file_path.name}",
                "scheme": "file",
                "format": "csv",
                "mediatype": "text/csv",
                "encoding": "utf-8",
                "dialect": {"csv": {"delimiter": sep}},
                "schema": {"fields": fields},
            }

        resource_descriptors.append(descriptor)

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

        df = sanitize_text(df)
        dest = write_output(out_name, df)
        print(f"OK  {dest.name}  ({len(df)} linhas, {len(df.columns)} colunas) -> {dest}")

        empties = [c for c in df.columns if df[c].isna().all() or (df[c].astype(str).str.strip().eq("")).all()]
        if empties:
            empty_col_report[out_name] = empties

    if empty_col_report:
        print("\n=== Colunas de saída sem dado equivalente em data_pre (ficaram vazias) ===")
        for name, cols in empty_col_report.items():
            print(f"- {name}: {', '.join(cols)}")

    build_datapackage()


if __name__ == "__main__":
    main()
