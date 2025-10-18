# 📊 Ingestão de Dados em Batch com Airflow e Delta Lake

O objetivo deste projeto é **simular um pipeline de ingestão de dados transacionais em batch**, aplicando a arquitetura em camadas (medalhão): **source → bronze → silver**.  

Com isso, busca-se:  
- ✅ **Gerar dados mockados** de um sistema transacional para simular o fluxo real;  
- ✅ **Orquestrar a ingestão diária** desses arquivos utilizando o **Apache Airflow**;  
- ✅ **Processar os dados** em larga escala com **Apache Spark**;  
- ✅ **Armazenar em formato Delta Lake**, garantindo versionamento, consistência e eficiência;  
- ✅ **Fornecer um exemplo didático** de como funcionaria um fluxo de ingestão de dados em um ambiente de **engenharia de dados moderna**.  

Este projeto tem caráter **educacional e prático**, servindo como base para estudos em **engenharia de dados, processamento distribuído e orquestração de pipelines**. 

Todo o pipeline é executado **localmente**, orquestrado por uma instância do **Apache Airflow**, e utilizando **Apache Spark** com suporte ao **Delta Lake**.

⚠️ Obs: Foi utilizado **PySpark** por questões didáticas. Em um contexto real, a massa de dados precisaria ser maior para justificar essa tecnologia mas, para integração com o Delta o PySpark é a escolha mais prática.

---

## 🗂 Estrutura do Projeto

```
project-root/
│
├── mock_data/
│   └── MOCK_DATA.csv              # Base de dados completa usada como origem
│
├── datalake/                      # Pasta externa contendo os dados organizados por camadas. Você precisa criar essa pasta e apontar na variável "DATALAKE_PATH" dentro dos arquivos
│   ├── source/
│   │   └── transaction_system/    # Arquivos CSV diários de entrada
│   ├── bronze/
│   │   └── transaction_data/      # Dados no formato Delta Lake (raw zone)
│   └── silver/
│       └── transaction_data/      # Dados tratados e deduplicados no formato Delta Lake
│
├── dags/
│   └── ingest_transaction_data.py # DAG do Airflow responsável pela ingestão diária. Você pode utilizar o comando 'cp' para copiar essa DAG para sua pasta de DAGs do Airflow.
│
├── scripts/
│   ├── mock_data_spliter.py       # Divide o MOCK_DATA.csv em 10 partes com datas diferentes
│   ├── ingest_source_to_bronze.py # Realiza ingestão dos arquivos CSV para camada bronze
│   └── ingest_bronze_to_silver.py # Atualiza a camada silver com dados incrementais da bronze
│
├── requirements.txt               # Bibliotecas necessárias para execução
└── README.md                      # Este arquivo
```

⚠️ **Importante:**  
Crie manualmente a pasta `datalake/` na raiz do projeto antes da execução e ajuste o caminho absoluto na variável `DATALAKE_PATH` dentro dos scripts.

---

## ⚙️ Como Executar

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Gere os arquivos simulados
```bash
python scripts/mock_data_spliter.py
```

### 3. Inicie o Airflow standalone
```bash
airflow standalone
```

### 4. Ative a DAG no painel do Airflow
Acesse o Airflow em [http://localhost:8080](http://localhost:8080) e ative a DAG `INGEST_TRANSACTION_DATA`.

> A DAG está agendada para rodar todos os dias às 03:00 (`0 3 * * *`), com suporte a **catchup** de dias anteriores. A simulação inclui falhas nos dias em que não existem arquivos.

---


## 📦 Tecnologias Utilizadas

- **Apache Spark** (Standalone)
- **Delta Lake**
- **Apache Airflow** (Standalone)
- **Python 3.10+**
- **Pandas**
- **Linux**

---

## 📄 Licença
Este projeto é livre para reprodução e customização, sob licença MIT.

## 📬 Contato

- [LinkedIn](https://www.linkedin.com/in/thiago-cbferreira/)  
- [GitHub](https://github.com/ThiagoCBF) 
