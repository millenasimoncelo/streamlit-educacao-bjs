import streamlit as st
import pandas as pd  # mantido para uso futuro

st.set_page_config(
    page_title="Indicadores Educacionais • Bom Jesus da Serra",
    page_icon="📊",
    layout="wide",
)

# SIDEBAR (navegação)
with st.sidebar:
    st.title("Navegação")
    pagina = st.radio(
        "Ir para:",
        ["Início", "Plano do App", "Bases de Dados", "Exploração (placeholder)", "Sobre"],
        index=0,
    )
    st.divider()
    st.caption("Versão: Layouts & Containers • Sem dados")

# INÍCIO
if pagina == "Início":
    with st.container():
        st.title("📊 Indicadores Educacionais de Bom Jesus da Serra – BA")
        st.subheader("Autora: Millena Simoncelo de Lima")
        st.write("Protótipo usando **Layouts & Containers** do Streamlit. Sem dados nesta etapa.")
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.write("**Tema**: Indicadores educacionais")
    col2.write("**Status**: Estrutura criada")
    col3.write("**Próximos passos**: Inserir dados e gráficos")

# PLANO DO APP
elif pagina == "Plano do App":
    st.header("🗺️ Plano do App")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("MVP")
        st.write("- Seções definidas\n- Layout aplicado\n- Placeholders")
    with col2:
        st.subheader("Expansões")
        st.write("- IDEB\n- Rendimento\n- Adequação docente\n- Gráficos")

# BASES DE DADOS
elif pagina == "Bases de Dados":
    st.header("🧾 Bases Planejadas")
    c1, c2, c3 = st.columns(3)
    c1.caption("IDEB/SAEB (INEP)")
    c2.caption("Censo Escolar (INEP)")
    c3.caption("Adequação da Formação Docente")

# EXPLORAÇÃO (placeholders)
elif pagina == "Exploração (placeholder)":
    st.header("🔎 Exploração de Dados")
    tab1, tab2 = st.tabs(["Tabelas", "Gráficos"])
    with tab1:
        st.info("Placeholder para tabelas (sem dados).")
    with tab2:
        st.info("Placeholder para gráficos (sem dados).")

# SOBRE
elif pagina == "Sobre":
    st.header("ℹ️ Sobre")
    st.write("**Autora:** Millena Simoncelo de Lima")
    st.write("**Disciplina:** Cloud Computing (Pós em Mineração de Dados)")
    st.write("**Tecnologia:** Streamlit (Python)")
