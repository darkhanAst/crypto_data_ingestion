# 🚀 Crypto Data Platform (BTC + Solana)

A production-style end-to-end data engineering platform for ingesting, processing, and analyzing blockchain data from Bitcoin and Solana networks.

The system demonstrates modern Data Engineering practices including **ETL orchestration, cloud storage ingestion, data warehousing, dbt modeling, and real-time alerting via Telegram**.

---

## 🧠 Architecture Overview
S3 (BTC), Solana API (Solana)
↓
Airflow DAGs (Orchestration)
↓
Python Ingestion Layer
↓
ClickHouse (Data Warehouse)
↓
dbt (Analytics & Marts)
↓
BI / Dashboards

---

## ⚙️ Tech Stack

- 🐍 Python (ETL / ingestion)
- 🌬 Apache Airflow (workflow orchestration)
- ☁️ AWS S3 (public blockchain datasets)
- 🗄 ClickHouse (OLAP database)
- 🧱 dbt (data modeling)
- 📩 Telegram API (alerting system)

---

## 📊 Data Sources

### Bitcoin
- AWS Public Dataset:
  - `s3://aws-public-blockchain/v1.0/btc/blocks/`
  - `s3://aws-public-blockchain/v1.0/btc/transactions/`

### Solana
- Blockchain performance & block data
- Slots, TPS, transaction throughput

---

## 🔄 Pipeline Overview

### 1. Extraction
- Reads parquet files from AWS S3
- Handles schema inconsistencies (string vs dictionary encoding)
- Partition-based loading by `date`

### 2. Transformation
- Type normalization (timestamps, numeric fields)
- Deduplication and schema alignment
- Data quality validation

### 3. Loading
- Inserts optimized batches into ClickHouse
- Partitioned by `date`
- Ordered for query performance

---

## 📦 Key Features

### ✅ Production-style Airflow DAGs
- Daily scheduled ingestion
- Retry logic
- Task dependencies (blocks → transactions)

### 📩 Telegram Alerting System
- Failure notifications via callbacks
- Includes error details and Airflow logs
- Real-time incident visibility

### 🧠 Data Quality Layer
- dbt-style checks:
  - uniqueness constraints
  - null validation
  - anomaly detection (audit layer)

### 📊 Analytics Ready Models
- BTC:
  - daily blocks metrics
  - transaction throughput
  - network efficiency (WAP-like metrics)

- Solana:
  - TPS calculation
  - block production latency
  - network load analysis

---

## 🧱 Data Models

### BTC Tables
- `btc_blocks`
- `btc_transactions`

### Solana Tables
- `solana_blocks`
- `solana_performance`

---

## 📈 Example Metrics

### Bitcoin
- Blocks per day
- Transactions per block
- Average block size
- Network difficulty trends

### Solana
- TPS (Transactions Per Second)
- Peak throughput (p95 / p99)
- Block latency
- Network efficiency

---

## 🚨 Observability

- Airflow task failure alerts → Telegram
- Logging for ingestion steps
- Error context propagation (task_id, DAG, logs)

---

## 🧪 Data Quality Strategy

- Schema enforcement during ingestion
- dbt-style tests:
  - NOT NULL constraints
  - uniqueness checks
  - anomaly detection models
- Audit layer for validation metrics

---

## 🧠 Key Engineering Concepts Demonstrated

- ETL / ELT pipeline design
- Idempotent data ingestion
- Partitioned data modeling
- Schema drift handling (S3 parquet inconsistency)
- Distributed data warehousing with ClickHouse
- Observability in data pipelines
- Event-driven alerting system

---

## 📌 Future Improvements

- Incremental ingestion (CDC-style)
- Kafka-based streaming ingestion
- dbt CI/CD with GitHub Actions
- AI agent for pipeline debugging
- Data lineage tracking

---

## 👨‍💻 Author

Darkhan  
Data Engineering / Analytics Engineering Project

---

## ⭐ Why this project matters

This project simulates a **real-world production data platform** used in fintech and blockchain analytics environments, demonstrating:

- scalability thinking
- production-grade pipeline design
- analytics engineering practices
- observability & reliability patterns