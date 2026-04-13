# Crypto Data Ingestion (BTC + Solana)

Production-style data ingestion pipelines for blockchain analytics using **Bitcoin (S3)** and **Solana (API)**.

---

## Architecture
```text
Bitcoin (AWS S3)        Solana (API)
        │                    │
        └──── Airflow DAGs ─┘
                  │
        Python Ingestion Layer
                  │
              ClickHouse
                  │
                dbt
                  │
            Analytics / BI
```


---

##  Stack

- Python
- Airflow
- AWS S3 (BTC data)
- Solana JSON-RPC API
- ClickHouse
- dbt
- Telegram alerts
---

## Data Sources

### Bitcoin
- S3 public dataset
- blocks + transactions

### Solana
- JSON-RPC API
- blocks + performance (TPS)
---

##  Pipelines

### BTC (Batch)
- S3 → transform → ClickHouse

### Solana (API)
- RPC → extract block/slot → ClickHouse
---

##  Transformation (dbt)
- BTC: blocks, tx, network activity
- Solana: TPS, latency, throughput
---

##  Features
- Airflow orchestration
- Data quality checks
- Telegram alerting
- Hybrid ingestion (S3 + API)
---

## Key Concepts

- Batch + API ingestion
- Idempotent pipelines
- Partitioned modeling
- Observability

---

## Author

Darkhan