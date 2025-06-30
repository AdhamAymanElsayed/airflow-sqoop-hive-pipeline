# 🔁 Airflow Sqoop-Hive ETL Pipeline

A lightweight ETL pipeline that extracts data from a local **MySQL** database, transfers it to **HDFS** using **Sqoop**, loads it into **Hive**, and validates the data — all orchestrated using **Apache Airflow**.

---
<div align="center">
    <img src="https://github.com/AdhamAymanElsayed/airflow-sqoop-hive-pipeline/blob/main/pipeline.png?raw=true" alt="Airflow Sqoop Hive Pipeline" width="700"/>
</div>
---

## ⚙️ Stack

- 🐬 **MySQL** – Source database (host machine)
- 🔄 **Sqoop** – Data import into HDFS
- 🐘 **HDFS** & 🐝 **Hive** – Storage & querying (Hortonworks VM)
- 🧩 **Apache Airflow** – DAG orchestration (Docker)

---

## 🧭 Workflow Steps

1. **Sqoop Import** – Extract MySQL data to HDFS  
2. **Create Hive Table** – Define table schema  
3. **Load into Hive** – Move data from HDFS  
4. **Validate** – Count records in Hive

---

## 🗺️ DAG Structure

```mermaid
graph TD
    Start([🚀 Start]) --> Sqoop([🔄 Sqoop Import])
    Sqoop --> Create([📊 Create Hive Table])
    Create --> Load([📥 Load Data to Hive])
    Load --> Validate([🔎 Validate Data])
    Validate --> End([✅ End])
