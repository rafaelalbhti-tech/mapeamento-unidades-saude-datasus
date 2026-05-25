import streamlit as st
import pandas as pd

st.set_page_config(page_title="SUS Analytics Gold", layout="wide")

# Carregamento dos dados das camadas Gold e Silver
@st.cache_data
def carregar_dados_gold():
    df_raw = pd.read_csv("silver/dados_tratados_ubs.csv")
    df_reg = pd.read_csv("gold/analytics_regional.csv")
    df_est = pd.read_csv("gold/analytics_estadual.csv")
    df_mun = pd.read_csv("gold/analytics_municipal.csv")
    return df_raw, df_reg, df_est, df_mun

df_silver, df_regional, df_estadual, df_municipal = carregar_dados_gold()

st.title("🏥 Sistema de Análise de Dispersão e Abrangência do SUS")
st.markdown("---")

# Definição das abas para o Drill-Down de granularidade
aba1, aba2, aba3, aba4 = st.tabs(["🌎 Visão Nacional", "🗺️ Visão Regional", "📍 Visão Estadual", "🏙️ Detalhamento Municipal"])

# --- 1. VISÃO NACIONAL ---
with aba1:
    st.subheader("Métricas Consolidadas do Território Nacional")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de UBS Ativas (Censo)", f"{len(df_silver):,}".replace(",", "."))
    c2.metric("População Coberta (Estimada)", "211.000.000")
    c3.metric("Média Nacional (UBS / 100k Hab.)", f"{(len(df_silver)/211000000)*100000:.2f}")
    
    st.markdown("#### Distribuição Espacial Absoluta")
    # Amostra estatística para o mapa nacional não travar a renderização do browser
    st.map(df_silver[["latitude", "longitude"]].sample(15000, random_state=42))

# --- 2. VISÃO REGIONAL ---
with aba2:
    st.subheader("Análise Macrorregional de Infraestrutura")
    
    col_reg1, col_reg2 = st.columns(2)
    with col_reg1:
        st.markdown("**Total de Unidades por Região**")
        st.bar_chart(data=df_regional, x="Região", y="total_ubs")
    with col_reg2:
        st.markdown("**Taxa de UBS por 100 mil Habitantes**")
        st.bar_chart(data=df_regional, x="Região", y="ubs_por_100k")
        
    st.dataframe(df_regional, use_container_width=True)

# --- 3. VISÃO ESTADUAL ---
with aba3:
    st.subheader("Disparidades e Concentração por Unidade da Federação")
    
    regiao_sel = st.selectbox("Filtre por Região para detalhar os Estados:", df_regional["Região"].unique())
    df_est_filtrado = df_estadual[df_estadual["Região"] == regiao_sel]
    
    st.bar_chart(data=df_est_filtrado, x="nome_uf", y="total_ubs")
    st.dataframe(df_est_filtrado, use_container_width=True)

# --- 4. VISÃO MUNICIPAL ---
with aba4:
    st.subheader("Foco no Município (Nível de Maior Granularidade)")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        uf_sel = st.selectbox("Selecione o Estado:", sorted(df_silver["nome_uf"].dropna().unique()))
    
    df_mun_filtrado = df_municipal[df_municipal["nome_uf"] == uf_sel]
    df_silver_mapa = df_silver[df_silver["nome_uf"] == uf_sel]
    
    with col_f2:
        st.metric("Total de UBS no Estado Selecionado", len(df_silver_mapa))
        
    st.markdown(f"#### Mapa de Dispersão Local: {uf_sel}")
    st.map(df_silver_mapa[["latitude", "longitude"]])
    
    st.markdown("#### Lista Cadastral de Unidades")
    st.dataframe(df_silver_mapa[["nome_ubs", "nome_mun", "bairro", "logradouro"]], use_container_width=True)


