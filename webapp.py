
import re
import glob
import pandas as pd
import streamlit as st
import plotly.express as px

# ------------------------------
# Config da página
# ------------------------------
st.set_page_config(page_title="IDEB — Comparação IDEB × Meta", layout="wide")

st.title("📊 IDEB — Comparação IDEB × Meta")
st.markdown(
    "**Autora:** Millena Simoncelo de Lima  \n"
    "**Fonte:** INEP — Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira  \n"
    "**Abrangência:** Municípios do Espírito Santo"
)
with st.expander("ℹ️ Sobre o app / dados utilizados"):
    st.write("Tema: comparação do IDEB observado com a Meta prevista, por etapa (Anos Iniciais/Finais).")
    st.write("Base atual: INEP (IDEB – escolas dos municípios do Espírito Santo; planilha .xlsx fornecida pela disciplina).")


# ------------------------------
# Carregamento da base
# 1) tenta ler um .xlsx da pasta (prioriza o nome padrão)
# 2) se não achar, oferece uploader
# ------------------------------
PADRAO = "divulgacao_anos_finais_escolas_2023 - Copia.xlsx"

def try_load_local():
    xlsx_files = [f for f in glob.glob("*.xlsx")]
    preferida = PADRAO if PADRAO in xlsx_files else (xlsx_files[0] if xlsx_files else None)
    if preferida:
        try:
            return pd.read_excel(preferida), preferida
        except Exception:
            return None, None
    return None, None

df_raw, nome_arquivo = try_load_local()

if df_raw is None:
    st.info("Envie a base (.xlsx) para continuar.")
    up = st.file_uploader("Arquivo Excel", type=["xlsx"])
    if up is not None:
        df_raw = pd.read_excel(up)
        nome_arquivo = up.name

if df_raw is None:
    st.stop()

# ------------------------------
# Normalização das colunas
# A base tem colunas "IDEB\n2015", "META \n2015", etc.
# Vamos identificar anos e montar em formato longo.
# ------------------------------
df = df_raw.rename(columns={
    "Nome do Município": "Município",
    "Nome da Escola": "Escola",
    "Rede": "Rede",
    "ETAPA": "Etapa"
})

# pega colunas de IDEB e META (ignorando espaços e quebras de linha)
def limpa(c: str) -> str:
    return re.sub(r"\s+", " ", str(c)).strip()

cols = {c: limpa(c) for c in df.columns}
df = df.rename(columns=cols)

ideb_cols = [c for c in df.columns if re.match(r"^IDEB\s*\d{4}$", c)]
meta_cols = [c for c in df.columns if re.match(r"^META\s*\d{4}$", c)]

# cria dicionários {ano: coluna}
def ano_de(c):  # extrai yyyy
    return int(re.search(r"(\d{4})", c).group(1))

ideb_map = {ano_de(c): c for c in ideb_cols}
meta_map = {ano_de(c): c for c in meta_cols}
anos_comuns = sorted(set(ideb_map.keys()) & set(meta_map.keys()))

# formato longo
long_rows = []
base_cols = ["Município", "Escola", "Rede", "Etapa"]
for ano in anos_comuns:
    bloco = df[base_cols].copy()
    bloco["Ano"] = ano
    bloco["Resultado"] = pd.to_numeric(df[ideb_map[ano]], errors="coerce")
    bloco["Meta"] = pd.to_numeric(df[meta_map[ano]], errors="coerce")
    long_rows.append(bloco)

df_long = pd.concat(long_rows, ignore_index=True)

# ------------------------------
# Filtros (SEM seleção inicial)
# ------------------------------
with st.sidebar:
    st.header("Filtros")
    muni_opt = sorted(df_long["Município"].dropna().unique())
    escola_opt = sorted(df_long["Escola"].dropna().unique())
    rede_opt = sorted(df_long["Rede"].dropna().unique())
    etapa_opt = sorted(df_long["Etapa"].dropna().unique())

    sel_muni = st.multiselect("Município", muni_opt)           # sem default
    sel_escola = st.multiselect("Escola", escola_opt)          # sem default
    sel_rede = st.multiselect("Rede", rede_opt)                # sem default
    sel_etapa = st.multiselect("Etapa", etapa_opt)             # sem default

df_f = df_long.copy()
if sel_muni:
    df_f = df_f[df_f["Município"].isin(sel_muni)]
if sel_escola:
    df_f = df_f[df_f["Escola"].isin(sel_escola)]
if sel_rede:
    df_f = df_f[df_f["Rede"].isin(sel_rede)]
if sel_etapa:
    df_f = df_f[df_f["Etapa"].isin(sel_etapa)]

st.caption(f"Arquivo: *{nome_arquivo}* • Linhas totais: {len(df_long):,} • Linhas após filtros: {len(df_f):,}".replace(",", "."))

# ------------------------------
# Abas
# ------------------------------
tab_tabela, tab_desc, tab_graf = st.tabs(["📋 Tabela", "📊 Descritivas", "📈 Gráfico"])

# TABELA
with tab_tabela:
    st.subheader("Tabela detalhada (linhas por Escola/Ano)")
    st.dataframe(df_f, use_container_width=True)
    st.download_button(
        "Baixar CSV (filtrado)",
        df_f.to_csv(index=False).encode("utf-8"),
        file_name="tabela_filtrada.csv"
    )

# DESCRITIVAS — SOMENTE a por Etapa (removemos a “geral” da esquerda)
with tab_desc:
    st.subheader("Estatísticas descritivas — IDEB Observado (por Etapa)")
    if df_f.empty:
        st.warning("Sem dados após os filtros.")
    else:
        desc_etapa = df_f.groupby("Etapa")["Resultado"].describe().reset_index()
        st.dataframe(desc_etapa, use_container_width=True)

# GRÁFICOS — por etapa; eixo X somente ANOS ÍMPARES
with tab_graf:
    st.subheader("Comparação IDEB (barras) × Meta (linha) — por Etapa")
    if df_f.empty:
        st.warning("Sem dados após os filtros.")
    else:
        col_a, col_b = st.columns(2)
        etapas_presentes = [e for e in ["Anos Iniciais", "Anos Finais"] if e in df_f["Etapa"].unique()]

        def plot_etapa(container, etapa_nome):
            df_e = (df_f[df_f["Etapa"] == etapa_nome]
                    .groupby("Ano")[["Resultado", "Meta"]]
                    .mean()
                    .reset_index()
                    .sort_values("Ano"))

            if df_e.empty:
                container.info(f"Sem dados para **{etapa_nome}** com os filtros atuais.")
                return

            fig = px.bar(
                df_e, x="Ano", y="Resultado",
                labels={"Resultado": "IDEB observado", "Ano": "Ano"},
                color_discrete_sequence=["#1f77b4"]
            )
            fig.add_scatter(
                x=df_e["Ano"], y=df_e["Meta"],
                mode="lines+markers", name="Meta",
                line=dict(color="#7fc8ff")
            )

            # apenas anos ímpares no eixo x
            anos_impares = [a for a in df_e["Ano"].unique() if int(a) % 2 == 1]
            anos_impares = sorted(anos_impares)
            if anos_impares:
                fig.update_xaxes(tickvals=anos_impares)

            container.markdown(f"**{etapa_nome}**")
            container.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

        # desenha lado a lado quando existir
        if "Anos Iniciais" in etapas_presentes:
            plot_etapa(col_a, "Anos Iniciais")
        if "Anos Finais" in etapas_presentes:
            if "Anos Iniciais" in etapas_presentes:
                plot_etapa(col_b, "Anos Finais")
            else:
                plot_etapa(col_a, "Anos Finais")
