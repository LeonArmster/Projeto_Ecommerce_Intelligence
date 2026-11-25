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

**Status: Core scope released in v2.0.0.** Customer 360, repeat purchase, cohort retention, product and logistics marts and Streamlit are delivered. The following original topics include optional enhancements not required for V2 closure:

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

## V2.1 — CI/CD and documentation

Partially delivered. Review remaining CI, portability, contracts, freshness and documentation gaps as needed for cloud migration; avoid unrelated expansion.

## V3.0 — Multi-warehouse Analytics Engineering

Databricks first, BigQuery second; retain PostgreSQL as the local baseline.

- Databricks: workspace, Unity Catalog, schemas, Parquet ingestion into RAW Delta tables, dbt-databricks target, incremental merge and tests.
- BigQuery: budget controls, dbt-bigquery target, load jobs, partitioning and clustering.
- Audit warehouse-specific SQL and use adapter-aware macros where necessary.
- Compare metric results, test coverage, build times and costs across targets.
- Document portability and publish v3.0.0 after successful builds on PostgreSQL and both cloud targets. Genie is optional, subject to availability.

## V3.1 — Consumption layer

Streamlit MVP delivered early in v2.0.0. No further dashboard development required unless a concrete gap emerges.

## V4.0 — AI Analyst and evaluation

Preserve the existing local Business Brief. Extend semantic context using dbt manifest metadata, controlled analytical tools, read-only SQL guardrails, Python agent loop, traces and a 30-question evaluation dataset. Compare accuracy, refusal behavior, latency and cost. Frameworks and MCP are optional.

## Future backlog

Delivery-risk ML, advanced customer intelligence, FastAPI, Azure and full lakehouse expansion are deferred until after V4 and require a clear learning objective.
