# Design Decisions and Known Limitations

## Design Decisions

Several architectural decisions are intentional.

## Why PostgreSQL?

PostgreSQL provides a realistic relational analytical environment while remaining easy to run locally with Docker.

It also supports JSONB, which is useful for AI context and response persistence.

## Why Parquet and CSV?

Parquet is the persistent generated-data format.

CSV is used as an ingestion staging format. The initial loader uses PostgreSQL server-side `COPY`; the incremental loader streams CSV data through `COPY FROM STDIN` into temporary tables before applying table-specific conflict handling.

## Why dbt?

dbt separates analytical transformations from Python ingestion logic and provides:

- modular SQL transformations;
- lineage;
- tests;
- documentation;
- incremental models;
- snapshots.

## Why Airflow?

Airflow provides explicit dependency management, retries, execution history and observability for the complete pipeline.

## Why local AI?

The goal of V1 is to learn AI integration without requiring paid inference APIs.

Ollama allows local experimentation while preserving a provider-independent application architecture.

## Why not let the LLM calculate metrics?

LLMs are probabilistic systems.

Business metrics require deterministic and reproducible calculations.

Therefore:

```text
dbt / Python
     ↓
deterministic computation

LLM
     ↓
interpretation and communication
```

## Why no dedicated Quality TaskGroup?

Data-quality tests are already executed by `dbt build`.

Adding another TaskGroup that only repeated the same validations would add visual complexity without providing additional protection.

## Why no cloud yet?

Cloud infrastructure is intentionally postponed until the local architecture is stable.

This avoids introducing infrastructure cost and complexity before the analytical design is validated.

---

## Known Limitations and Technical Debt

The synthetic dataset intentionally remains an evolving component.

Known areas for future improvement include:

- customer creation dates should be fully consistent with order chronology;
- historical orders should have more realistic status behavior;
- duplicate products within the same order should be controlled;
- incremental RAW ingestion still scans the full historical CSV for each transactional table; delta-only CSV extraction is deferred as a performance optimization;
- AI severity thresholds are demonstration business rules rather than universal e-commerce standards;
- local Ollama inference depends on the host machine being available when the Airflow AI task executes.

These limitations are documented rather than hidden because identifying and managing technical debt is part of the project.

---
