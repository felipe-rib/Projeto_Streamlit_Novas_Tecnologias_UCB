# Análise de Sinistros de Trânsito no Brasil 🚦

Este projeto é um painel analítico interativo focado em expor a **subnotificação sistêmica** das estatísticas de trânsito no Brasil. Ele cruza os dados oficiais de acidentes de trânsito (RENAEST) com os atestados de óbito do Ministério da Saúde (SIM) e os custos hospitalares (SIH/SUS).

O objetivo acadêmico deste repositório é demonstrar o domínio prático do ecossistema Python em um ciclo completo de ciência de dados.

## Objetivos e Requisitos Atendidos

O projeto atende a 4 etapas fundamentais:
1. **Definição do Problema:** Expor a verdadeira letalidade do trânsito que é mascarada pelas estatísticas oficiais e o seu impacto financeiro na saúde pública.
2. **Obtenção e Preparação dos Dados:** Utilização de `Pandas` e `Numpy` para tratar dados nulos, alterar tipagens, remover duplicatas e criar novas features (Engenharia de Features) em tempo real.
3. **Análise Exploratória e Visualização:** Criação de visualizações de dados totalmente construídas com `Matplotlib`, garantindo uma apresentação executiva limpa e padronizada.
4. **Relatório e Conclusões:** Apresentação dos achados diretamente na interface da aplicação.

## Tecnologias Utilizadas

* **Python 3.x**
* **[Streamlit](https://streamlit.io/):** Criação da interface web (Dashboard) e filtros interativos (Barra Lateral).
* **[Pandas](https://pandas.pydata.org/):** Leitura, manipulação, limpeza e agregação do cubo de dados (`cubo_analitico.csv`).
* **[Numpy](https://numpy.org/):** Cálculos vetorizados, regressão linear (linha de tendência) e operações matemáticas auxiliares.
* **[Matplotlib](https://matplotlib.org/):** Renderização de todos os gráficos analíticos (Barras, Barras Horizontais, Rosca e Dispersão).

## Como o Cubo Analítico foi Formado (ETL)

A formação do **Cubo Analítico** (`cubo_analitico.csv`) é o resultado de um processo clássico de **Engenharia de Dados (ETL/ELT)**, cruzando múltiplas fontes governamentais distintas em uma base consolidada:

1. **Extração das Fontes:** Os dados brutos foram extraídos de sistemas isolados:
   * **RENAEST (Senatran):** Ocorrências oficiais de trânsito (data, tipo de via, etc). - https://dados.transportes.gov.br/dataset/renaest
   * **Ministério da Saúde:** Atestados de óbito reais, detalhados por modo de transporte (CID-10). - https://www.gov.br/saude/pt-br/acesso-a-informacao/dados-abertos/pda
   * **SIH (Datasus / SUS):** Internações hospitalares e custos financiados pelo Governo.
   * **IBGE:** Dados populacionais para cálculo per capita.
2. **Agregação e Transformação:** Os dados brutos focados em eventos únicos foram agrupados (*Group By*) utilizando a chave `(codigo_ibge, ano)`, gerando Dataframes intermediários (`.parquet`) totalizadores por cidade/ano.
3. **Cruzamento (Join):** Todos os sistemas foram unificados lateralmente via *Left/Outer Joins*.
4. **Engenharia de Features:** Criação de métricas de negócio, como percentuais (`share_`), gap de subnotificação e custos.
5. **Carga Analítica:** A tabela resultante foi denormalizada e salva como um arquivo leve (`cubo_analitico.csv`).

**O grande benefício dessa abordagem:** O aplicativo front-end (`app.py`) não precisa carregar gigabytes de dados crus ou realizar *joins* complexos em tempo de execução. O Streamlit apenas lê o cubo final otimizado, dedicando toda a memória do Python para filtragem ágil e renderização gráfica pelo Matplotlib.

## Estrutura de Arquivos

```text
.
├── app/
│   └── app.py                     # Script principal da aplicação (Streamlit + Matplotlib)
├── data/
│   └── proc/
│       ├── cubo_analitico.csv     # Base de dados consolidada e tratada
│       ├── cubo_dicionario.md     # Dicionário de dados explicando as variáveis
│       └── ...                    # Outros arquivos fonte (.parquet) originais de composição
└── README.md                      # Esta documentação
```

## Como Executar o Projeto

1. **Clone este repositório** (ou navegue até a pasta do projeto no seu terminal).
2. **Instale as dependências necessárias** (caso ainda não tenha no seu ambiente):
   ```bash
   pip install streamlit pandas numpy matplotlib
   ```
3. **Execute a aplicação** a partir da raiz do projeto (`app`):
   ```bash
   streamlit run app/app.py
   ```
4. **Acesso:** O Streamlit abrirá automaticamente no seu navegador padrão, normalmente no endereço `http://localhost:8501`.

## Principais Descobertas
* Uma enorme parcela dos óbitos não consta nos registros oficiais do trânsito, sendo registrados apenas pela saúde.
* O perfil de vítimas fatais é massivamente dominado por **motociclistas**.
* Os acidentes aumentam expressivamente nos finais de semana.
* Existe uma forte correlação linear entre a população de um município e os altos custos hospitalares gerados ao SUS devido às internações de trânsito.
