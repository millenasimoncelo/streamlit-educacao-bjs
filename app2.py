import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Indicadores Educacionais • Bom Jesus da Serra",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Ir para:",
    ["Início", "Plano do App", "Bases de Dados", "Exploração (placeholder)", "Sobre"]
)

if pagina == "Início":
    st.title("📊 Indicadores Educacionais de Bom Jesus da Serra – BA")
    st.subheader("Autora: Millena Simoncelo de Lima")
    st.write("""
    Este é um **protótipo** de web app em Streamlit para a disciplina **Cloud Computing** (Pós em Mineração de Dados).
    **Tema:** análise e visualização de indicadores educacionais (IDEB, taxas de rendimento e adequação docente).
    """)
    st.info("Status: estrutura inicial criada. Próximos passos: inserir dados e gráficos nas seções de Exploração.")

elif pagina == "Plano do App":
    st.header("🗺️ Plano do App (MVP e Expansões)")
    st.markdown("""
    **Objetivo:** disponibilizar um painel simples que consolide indicadores essenciais de aprendizagem e rendimento.

    **Entregas agora (MVP):**
    - Estrutura de navegação e seções.
    - Lista de bases de dados planejadas.
    - Espaço reservado para tabelas e gráficos.

    **Próximas entregas (expansões):**
    - Carregar séries históricas de **IDEB** (Anos Iniciais/Finais).
    - Inserir **Taxas de Rendimento** (aprovação, reprovação, abandono).
    - Adicionar **Adequação da Formação Docente**.
    - Gráficos de linhas e barras; comparações por etapa/ano.
    - Download de CSVs e anotações.
    """)

elif pagina == "Bases de Dados":
    st.header("🧾 Bases de Dados Planejadas")
    st.write("Lista das fontes que imagino utilizar:")
    fontes = pd.DataFrame([
        {"Fonte": "IDEB / SAEB (INEP)", "Uso previsto": "Séries históricas por etapa; metas e resultados"},
        {"Fonte": "Censo Escolar (INEP)", "Uso previsto": "Taxas de rendimento; matrículas; turmas"},
        {"Fonte": "Adequação da Formação Docente (INEP)", "Uso previsto": "Distribuição por grupos de adequação"},
            ])
    st.dataframe(fontes, use_container_width=True)
    st.caption("Obs.: Nesta etapa, as bases estão apenas declaradas. A carga ocorrerá nas próximas versões.")

elif pagina == "Exploração (placeholder)":
    st.header("🔎 Exploração de Dados (placeholder)")
    st.write("""
    Quando os arquivos forem adicionados, os dados aparecerão aqui.
    Enquanto isso, você pode **carregar um CSV opcionalmente** para testar a visualização.
    """)
    up = st.file_uploader("Enviar um CSV (opcional, para teste)", type=["csv"])
    if up is not None:
        df = pd.read_csv(up)
        st.subheader("Prévia do dataset enviado")
        st.dataframe(df.head(50), use_container_width=True)
        st.subheader("Dimensões")
        st.write(f"{df.shape[0]} linhas × {df.shape[1]} colunas")
        st.info("Gráficos serão adicionados aqui quando as colunas/medidas forem definidas.")
    else:
        st.warning("Nenhum arquivo enviado ainda. Use o seletor acima para testar com um CSV seu.")

elif pagina == "Sobre":
    st.header("ℹ️ Sobre")
    st.write("""
    **Autora:** Millena Simoncelo de Lima  
    **Curso:** Pós-graduação em Mineração de Dados — Disciplina: Cloud Computing  
    **Tecnologia:** Streamlit (Python)
    """)
    st.markdown(
        '<p style="font-size:0.95rem;color:#555;">Este app foi criado como primeiro exercício de deploy; '
        'nas próximas versões, incluirá dados do INEP (IDEB, Censo Escolar) e visualizações.</p>',
        unsafe_allow_html=True
    )