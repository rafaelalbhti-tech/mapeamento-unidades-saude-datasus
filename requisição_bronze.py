import json
import requests
import time

limit = 1000
offset = 0
todas_ubs = []

while True:
    url = f"https://apidadosabertos.saude.gov.br/assistencia-a-saude/unidade-basicas-de-saude?limit={limit}&offset={offset}"
    
    response = requests.get(url, timeout=15)
    dados = response.json()
    
    # se não houver mais dados, para o laço
    if not dados.get("ubs"):
        break
        
    todas_ubs.extend(dados["ubs"])
    print(f"Registros extraídos até agora: {len(todas_ubs)}")
    
    offset += limit
    time.sleep(1)

nome_arquivo_bruto = "bronze/dados_brutos_datasus.json"
with open("bronze/dados_brutos_datasus.json", 'w', encoding='utf-8') as f:
    json.dump({"ubs": todas_ubs}, f, ensure_ascii=False, indent=4)

print(f"Sucesso! Gravado em: {nome_arquivo_bruto}")

