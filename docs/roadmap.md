# Project Status and Roadmap

## V1 Status

Version 1 establishes the platform foundation.

Completed capabilities include:

- synthetic data generation, including incremental transactional updates;
- multi-million-row dataset;
- Parquet storage;
- PostgreSQL initial bulk ingestion and idempotent transactional RAW UPSERTs;
- dbt staging models;
- dbt intermediate models;
- analytical marts;
- dbt data-quality tests;
- incremental models;
- dbt snapshots;
- Docker environment;
- Apache Airflow orchestration with a validated incremental DAG and daily schedule configuration;
- local LLM integration;
- provider abstraction;
- deterministic AI business rules;
- structured AI output;
- PostgreSQL AI persistence;
- idempotent AI writes;
- Docker-to-host Ollama communication;
- successful end-to-end incremental pipeline execution;
- basic operational observability.

---

## Roadmap

The project is designed to evolve incrementally rather than adding technologies without a business purpose.

## V1 — Data Platform + AI Foundation

**Status: Complete**

Focus:

- Data Engineering;
- Analytics Engineering;
- orchestration;
- data quality;
- local Generative AI;
- structured business interpretation.

---

## V2 — Advanced Analytics Engineering

**Status: Core scope complete; release pending.** Customer 360, repeat purchase, cohort retention, product and logistics marts and Streamlit are delivered. The following original topics include optional enhancements not required for V2 closure:

- dimensional modeling;
- `dim_customers`;
- `dim_products`;
- `dim_date`;
- additional fact tables;
- customer behavior marts;
- product performance marts;
- logistics marts;
- advanced incremental strategies;
- SCD patterns;
- dbt macros;
- generic tests;
- singular tests;
- contracts;
- source freshness;
- exposures;
- improved synthetic-data integrity.

---

## Next phase — AI Engineering

Extend the existing Business Brief to customer, product and logistics contexts; validate structured outputs and factual grounding; then introduce controlled analytical tools for investigation. Keep the local provider and existing dbt metrics. Delivery-risk ML remains a future milestone.

## Future milestone — Machine Learning: Delivery Risk

Goal:

> Predict the probability that an order will be delivered late.

Planned components:

```text
dbt Feature Mart
      ↓
Training Dataset
      ↓
ML Training
      ↓
Experiment Tracking
      ↓
Model
      ↓
Predictions
      ↓
Explainability
```

Potential technologies:

- scikit-learn;
- XGBoost;
- CatBoost;
- MLflow;
- SHAP.

---

## V4 — Customer Intelligence

Potential capabilities:

- RFM analysis;
- customer segmentation;
- customer behavior features;
- repeat-purchase propensity;
- customer lifetime value;
- customer profiles.

---

## V5 — AI Data Analyst

The current Business Brief is intentionally limited to interpreting predefined metrics.

A future AI Analyst will be able to investigate analytical questions using controlled tools.

Example:

```text
User:
"Why did sales decrease?"

        ↓

AI Analyst

        ├── investigates categories
        ├── investigates regions
        ├── investigates customers
        ├── investigates logistics
        └── compares periods

        ↓

Evidence-based synthesis
```

Planned concepts:

- tool calling;
- semantic context;
- controlled analytical tools;
- context engineering;
- AI guardrails.

---

## V6 — Application Layer

Expose the platform through an application.

Potential architecture:

```text
Frontend
   │
   ▼
FastAPI
   │
   ├── Analytics
   ├── Machine Learning
   └── AI
          │
          ▼
      PostgreSQL
```

Potential deployment options include Supabase for lightweight public data access.

---

## V7 — Databricks / Lakehouse

The same project will later be adapted to a Lakehouse architecture.

Potential architecture:

```text
Object Storage
      ↓
Bronze
      ↓
Silver
      ↓
Gold
      ↓
Delta Lake
```

Planned technologies:

- PySpark;
- Delta Lake;
- Databricks;
- MLflow;
- Unity Catalog;
- Databricks Workflows;
- Model Serving.

The synthetic dataset can also be scaled from millions to tens or hundreds of millions of records to create a workload where distributed processing has a clear technical purpose.

---

## V8 — Azure Cloud Architecture

Final infrastructure evolution may include:

- Azure Data Lake Storage;
- Azure Databricks;
- secrets and identity management;
- cloud networking;
- deployment;
- monitoring;
- cost management;
- CI/CD.

Cloud resources will be introduced only when they provide a clear architectural learning objective.

---
