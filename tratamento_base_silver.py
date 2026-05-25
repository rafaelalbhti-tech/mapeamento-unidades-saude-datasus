import pandas as pd
import openpyxl
import json



with open("bronze/dados_brutos_datasus.json", "r", encoding="utf-8") as f:
    dados_json = json.load(f)

df_ubs = pd.DataFrame(dados_json["ubs"])
df_ubs["ibge"] = df_ubs["ibge"].astype(str).str.strip()

#primeiro DePara cruzando código_mun_ibge e cod_uf_ibge com planilha de municípios e suas respectivas UF's, a fim de trazer nome_mun e nome_uf (que não estavam na base original bronze/dados_brutos_datasus.json) 
df_depara = pd.read_excel("bronze/DePara_ibge.xlsx")

df_depara["ibge_6digitos"] = df_depara["Código Município Completo"].astype(str).str.strip().str[:6]

df_depara_limpo = df_depara.drop_duplicates(subset=["ibge_6digitos"])

df_tratado = pd.merge(
    df_ubs, 
    df_depara_limpo[["ibge_6digitos", "Nome_Município", "Nome_UF"]], 
    left_on="ibge", 
    right_on="ibge_6digitos", 
    how="left"
)

df_tratado = df_tratado.drop(columns=['cnes', 'ibge_6digitos'])
df_tratado = df_tratado.rename(columns={
    'ibge': 'cod_mun_ibge',
    'nome': 'nome_ubs',
    'Nome_Município': 'nome_mun',
    'Nome_UF': 'nome_uf'
})


#segundo DePara
df_depara_regiao = pd.read_excel("bronze/DePara_regiao.xlsx")

# Limpar possíveis espaços em branco nos nomes dos estados para não quebrar o merge
df_tratado["nome_uf"] = df_tratado["nome_uf"].astype(str).str.strip()
df_depara_regiao["UF"] = df_depara_regiao["UF"].astype(str).str.strip()

# Cruzamento 2: Adicionando a coluna de Região baseada no Nome_UF
df_final = pd.merge(
    df_tratado,
    df_depara_regiao[["UF", "Região"]],
    left_on="nome_uf",
    right_on="UF",
    how="left"
)

df_final = df_final.drop('UF', axis=1)
df_final["latitude"] = df_final["latitude"].astype(str).str.strip().str.replace(",", ".")
df_final["longitude"] = df_final["longitude"].astype(str).str.strip().str.replace(",", ".")

df_final["latitude"] = pd.to_numeric(df_final["latitude"], errors='coerce')
df_final["longitude"] = pd.to_numeric(df_final["longitude"], errors='coerce')

# Remove quem não tem mapa (essencial para manter o Streamlit leve e funcional)
df_final = df_final.dropna(subset=["latitude", "longitude"])


print(df_final.head())

nome_arq = 'silver/dados_tratados_ubs.csv'

df_final.to_csv("silver/dados_tratados_ubs.csv", index=False, encoding="utf-8")
print(f"Sucesso! Gravado em: {nome_arq}")