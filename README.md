# PLACE Challenge - ETL e Análise Econômica Urbana de Belo Horizonte

Este projeto tem como objetivo o desenvolvimento de um pipeline de ETL local e geração de visualizações para **identificação de regiões promissoras para novos negócios em Belo Horizonte**, utilizando dados públicos fornecidos pela Prefeitura.

---

## Desafio Proposto:

Inspirada na dinâmica anterior do "Scranton Rising", a proposta é utilizar dados públicos da cidade de Belo Horizonte para:

- Desenvolver um pipeline de **ETL** (Extração, Transformação e Carga)
- Realizar análises urbanas com foco **econômico e de infraestrutura**
- Construir visualizações com potencial de gerar **insights acionáveis** para stakeholders e investidores

---

### Motivação e Raciocínio Lógico por Trás da Solução:

A motivação central deste projeto é utilizar essas fontes para **identificar bairros subutilizados economicamente**, mas com **boa infraestrutura de transporte público**, que são ideais para estimular novos investimentos e fomentar o desenvolvimento urbano.

Para isso, foi desenvolvido um pipeline de dados que realiza a extração, padronização e cruzamento de informações sobre empresas, bairros e transporte urbano. Como resultado, geramos um score de potencial econômico por bairro, priorizando regiões com alta mobilidade e pouca ocupação atual. Essa abordagem fornece uma base objetiva para apoiar decisões de investimento e planejamento urbano.


---

## Objetivo da Solução:

A solução visa responder à seguinte pergunta:

> **“Quais bairros de Belo Horizonte são mais promissores para abertura de novos negócios, considerando infraestrutura de transporte e presença empresarial atual?”**

Para isso, utilizamos uma abordagem de engenharia de dados moderna e modular, estruturada em camadas (Bronze → Silver → Gold), com o objetivo de entregar dados limpos, padronizados e prontos para consumo analítico.

---

## Estrutura do Pipeline ETL:

```plaintext
projeto/
├── data/
│   ├── bronze/                # Dados brutos carregados (extraídos diretamente dos arquivos originais)
│   ├── silver/                # Dados tratados, padronizados e enriquecidos
│   └── gold/                  # Dados analíticos prontos para geração de insights
│
├── dataviz/
│   └── analise_bairros_bh_gold.ipynb   # Notebook com gráficos de análise final
│
├── docs/
│   ├── arquitetura-sugerida.png  # Arquitetura sugerida para ambiente em nuvem usando AWS.
│
├── notebooks/
│   ├── load_to_bronze/
│   │   ├── load_bairros_to_bronze.py
│   │   ├── load_to_silver_empresas_to_bronze.py
│   │   └── load_to_silver_ponto_onibus_to_bronze.py
│   │
│   ├── bronze_to_silver/
│   │   ├── bronze_to_silver_bairros.py
│   │   ├── bronze_to_silver_empresas.py
│   │   └── bronze_to_silver_ponto_onibus.py
│   │
│   └── silver_to_gold/
│       └── silver_to_gold.py
│
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação principal do projeto
```

---

## 🧪 Bases de Dados Utilizadas:

| Base                  | Fonte                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| Empresas              | https://dados.pbh.gov.br/dataset/atividade-economica                 |
| Bairros Oficiais      | https://dados.pbh.gov.br/dataset/bairro-oficial                      |
| Pontos de Ônibus      | https://dados.pbh.gov.br/dataset/ponto-de-onibus                     |

---

## Tecnologias Utilizadas:

- `Python`
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `pyproj` (conversão de coordenadas)
- `scikit-learn` (normalização z-score)
- `shapely` (análise espacial)
- `BallTree` para geolocalização eficiente

---

## Como Rodar o Projeto Localmente:

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/place-challenge.git
cd place-challenge
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute os scripts por camada

1. `notebooks/load_to_bronze/*.py` – para carregar os arquivos originais
2. `notebooks/bronze_to_silver/*.py` – para padronizar, limpar e enriquecer os dados
3. `notebooks/silver_to_gold/silver_to_gold.py` – para gerar o dataset final com **scores de potencial**

---

## Visualizações e Análises:

As análises estão disponíveis em:

[`dataviz/analise_bairros_bh_gold.ipynb`](dataviz/analise_bairros_bh_gold.ipynb)

Incluindo:
- Gráficos de distribuição de score
- Top 10 bairros mais promissores com base no score
- Mapa Simplificado dos Bairros Promissores
- Melhores Bairros com Alta Disponibilidade de Transporte e no máximo 100 Empresas
- Distribuição de Bairros por Nível de Disponibilidade de Transporte e Ocupação

---

## Lógica do Score de Potencial:

O `potencial_score` dos bairros é calculado com base em:

- **Densidade de empresas por km²**
- **Densidade de pontos de ônibus por km²**

Utilizando padronização (z-score) e pesos:

```python
potencial_score = round(0.4 * z_empresas + 0.6 * z_transporte)
```

> **Alta infraestrutura de transporte** é valorizada mesmo em bairros ainda pouco ocupados economicamente.

---

## Próximos Passos (Escalabilidade em Produção):

O pipeline pode ser adaptado para execução automática e escalável utilizando arquitetura na **AWS**:

![Arquitetura Sugerida ](https://github.com/LLR798/Desafio-Place/blob/main/docs/arquitetura.png)

### Componentes Sugeridos:

| Componente              | Tecnologia Sugerida         |
|-------------------------|-----------------------------|
| Orquestração            | AWS EC2 com Airflow ou MWAA  |
| Ingestão de dados       | AWS Lambda                  |
| Processamento ETL       | AWS EMR ou Glue (PySpark)   |
| Armazenamento           | S3 (Bronze/Silver/Gold)     |
| Banco de Consulta       | AWS Athena ou Redshift      |
| Visualização            | Power BI, Tableau, Quicksight, etc |
| DataOps                 | GitLab e Terraform          |

---

## Contato:

Fique à vontade para entrar em contato para dúvidas ou contribuições:

🔗 [linkedin.com/in/lucas-lumertz](https://linkedin.com/in/lucas-lumertz)

---

## Resultado Final:

O pipeline entregue gera um conjunto de dados confiável que permite **identificar oportunidades reais de investimento**, cruzando dados de mobilidade urbana e densidade econômica.

Conseguindo identificar regiões promissoras para abertura de novos negócios em Belo Horizonte, considerando a densidade empresarial atual e infraestrutura de transporte (pontos de ônibus).

Esse processo mostra como a engenharia de dados pode ser aplicada de forma objetiva para apoiar decisões urbanas e econômicas baseadas em dados públicos abertos.