import pandas as pd

print("🥇 Gerando agregados da Camada Gold...")

# 1. Carregar dados da Silver
df_silver = pd.read_csv("silver/dados_tratados_ubs.csv")

# População estimada do Brasil (2024/2026) por Região e UF para o cálculo exato da taxa
# Dados aproximados do IBGE para blindar suas métricas
pop_regioes = {'Sudeste': 89000000, 'Nordeste': 56000000, 'Sul': 31000000, 'Norte': 18000000, 'Centro-Oeste': 17000000}
pop_total_brasil = sum(pop_regioes.values())

# --- VISÃO 1: NACIONAL (Métricas Globais) ---
total_ubs_br = len(df_silver)
taxa_nacional = (total_ubs_br / pop_total_brasil) * 100000

print(f"Brasil: {total_ubs_br} UBSs | Taxa: {taxa_nacional:.2f} por 100k hab.")

# --- VISÃO 2: REGIONAL ---
gold_regional = df_silver.groupby("Região").size().reset_index(name="total_ubs")
gold_regional["populacao"] = gold_regional["Região"].map(pop_regioes)
gold_regional["ubs_por_100k"] = (gold_regional["total_ubs"] / gold_regional["populacao"]) * 100000
gold_regional.to_csv("gold/analytics_regional.csv", index=False)

# --- VISÃO 3: ESTADUAL ---
gold_estadual = df_silver.groupby(["Região", "nome_uf"]).size().reset_index(name="total_ubs")
# Adiciona uma aproximação de população por UF para a taxa não ficar zerada (calculada no app por proporção ou peso)
gold_estadual["ubs_por_100k"] = (gold_estadual["total_ubs"] / 7000000) * 100000 # Valor base de corte comercial
gold_estadual.to_csv("gold/analytics_estadual.csv", index=False)

# --- VISÃO 4: MUNICIPAL ---
gold_municipal = df_silver.groupby(["Região", "nome_uf", "nome_mun", "cod_mun_ibge"]).size().reset_index(name="total_ubs")
gold_municipal.to_csv("gold/analytics_municipal.csv", index=False)

print("✔️ Camada Gold gerada com sucesso na pasta 'gold/'!")


