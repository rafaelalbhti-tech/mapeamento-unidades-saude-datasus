# 🏥 Análise da distribuição e alcance das UBS's no Brasil

## 📝 Descrição do Projeto
Este projeto usa conceitos básicos de Ciência de Dados para organizar e analisar a localização das Unidades Básicas de Saúde
(UBS) ativas no Brasil. A solução coleta dados públicos, trata essas informações e cruza alguns dados geográficos, como 
códigos de municípios do IBGE e regiões do país. Depois disso, os resultados são mostrados em um dashboard interativo que 
facilita a visualização e a análise das informações.

---

## 🎯 Justificativa do Tema e Relevância Social
A Atenção Primária à Saúde (APS) é a principal porta de entrada do Sistema Único de Saúde (SUS) no Brasil. 
Compreender como as mais de 44 mil unidades estão distribuídas geograficamente é fundamental para identificar vazios 
assistenciais, disparidades macrorregionais e gargalos na infraestrutura de atendimento. 

Este projeto se justifica pela necessidade de transformar dados brutos governamentais em informações visuais acionáveis, 
permitindo que decisores políticos e a população em geral auditem a capilaridade e a abrangência da saúde pública no país.

---

## 🔍 Perguntas-Chave que o Dashboard Responde
1. **De que forma as UBS estão espalhadas pelo território brasileiro e qual é o seu real alcance geográfico?**
2. **Existe uma concentração desigual de unidades entre as regiões do país quando analisamos a taxa de UBS por
   100 mil habitantes?**
4. **Como se comporta a densidade de unidades de saúde quando aumentamos a granularidade descendo do nível Nacional
   para o Estadual e Municipal?**

---

## 💾 Fonte dos Dados e Infraestrutura
* **Dados das UBSs:** Extraídos via requisição de dados públicos do censo de infraestrutura do Ministério da Saúde / DataSUS.
       https://apidadosabertos.saude.gov.br/assistencia-a-saude/unidade-basicas-de-saude

* **Dados de Municípios (De-Para):** Tabela DTB (Divisão Territorial Brasileira) oficial do **IBGE (2024)**, utilizada
  para correlacionar códigos de 6 e 7 dígitos e evitar inconsistências de registro.
       https://www.ibge.gov.br/explica/codigos-dos-municipios.php
  
* **Dados de Regiões:** planilha imputada manualmente, contendo os dados referentes às UF's brasileiras como:
     - Código IBGE da UF
     - Nome da UF
     - Região da UF
* **Uso de IA (Gemini)** Para ganhar eficiência, além de executar tarefas repetitivas. Foi usada principalmente na montagem final do Dashboard devido ao curto conhecimento a respeito da biblioteca Streamlit.

---

## 📂 Estrutura de Pastas (Arquitetura Medalhão)
├── bronze/          # Dados JSON puros coletados diretamente do DataSUS e tabelas originais do IBGE
├── silver/          # Dados limpos, com coordenadas tratadas e de-para de municípios e UF's unificados
├── gold/            # Tabelas agregadas por Região, UF e Município prontas para o Dashboard
├── insights.py      # Arquivo principal de execução do Dashboard Streamlit
└── ubs_gold.py      # Script de processamento e agregação da camada Gold

🚀 **Instruções de Instalação e Execução Local**
Para rodar este projeto localmente na sua máquina e reconstruir o banco de dados do zero, siga os passos abaixo:

1. **Clonar o Repositório**
Inicialmente, abra o terminal ou CMD e entre na pasta em que quer salvar o clone
Após isso, execute o seguinte prompt: git clone https://github.com/rafaelalbhti-tech/mapeamento-unidades-saude-datasus.git
Logo após, uma pasta com o projeto será criada automaticamente.
  para entrar nela:
    cd NOME_REPOSITORIO
  E ver os arquivos:
    ls

2. **Instalar as Dependências Obrigatórias**
Certifique-se de ter o Python instalado e execute no terminal:
pip install streamlit pandas requests xlrd openpyxl

3. **Fluxo de Processamento e Execução (Ordem dos Scripts)**
Como o projeto utiliza a arquitetura Medalhão, os dados precisam ser processados na sequência exata de dependência.
Execute os comandos no seu terminal seguindo a ordem abaixo:

Passo 1: Execução das requisições à API na Bronze (requisicao_bronze.py)
Este script faz as requisições diretas para a API pública do DataSUS, extrai as mais de 44 mil unidades de saúde e 
salva o arquivo dados_brutos_datasus.json na pasta bronze/.

Passo 2: Processamento da Camada Silver (tratamento_base_silver.py)
Este script lê o JSON bruto gerado no passo anterior, corrige problemas de coordenadas inválidas, faz dois DePara com outras
duas bases .xlsx, uma de código_mun_ibge, a fim de trazer seus nomes, e um outro que cruza o estado da UBS com o intuito de trazer
suas respectivas regiões, além de unificar as tabelas e salva na pasta silver/dados_tratados_ubs.csv.

Passo 3: Processamento da Camada Gold (ubs_gold.py)
Este script consome a base limpa da Silver, injeta a tabela de macrorregiões do país, calcula de forma performática 
as taxas de UBS por 100 mil habitantes e exporta os arquivos leves que alimentarão o BI.

Passo 4: Inicialização do Dashboard (insights.py)
Com todas as camadas de dados processadas e consolidadas, inicialize o servidor do Streamlit para abrir a interface
interativa no seu navegador padrão: **streamlit run insights.py**

📊 Capturas de Tela do Dashboard Final
<img width="1909" height="940" alt="image" src="https://github.com/user-attachments/assets/194b4efa-dc44-4928-ba31-4e2193060d77" />
<img width="1916" height="938" alt="image" src="https://github.com/user-attachments/assets/0c51d72a-35d8-4dc8-ac5c-44cc1cbecdea" />
<img width="1918" height="931" alt="image" src="https://github.com/user-attachments/assets/8da08b43-578b-4a53-8627-26e752baeb44" />
<img width="1919" height="928" alt="image" src="https://github.com/user-attachments/assets/ebbc8ced-c17b-4d55-9827-8c3102f545e7" />
