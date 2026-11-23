# Pipeline performance and quality baseline (v1.1)

## Scope and provenance

Measurements captured on **2026-11-22 (America/Sao_Paulo)** from a local Windows 11 / Git Bash / Docker Desktop environment running Linux containers, PostgreSQL 17 and Airflow. The Airflow run ID is `manual_2026-11-23T01:09:02+00:00` (UTC). These are **observed local measurements on the project's synthetic e-commerce dataset**, not production benchmarks or cold-start measurements. Times vary with machine, data volume, cache and container load.

## dbt inventory and isolated build

- dbt Core **1.12.6**, postgres adapter **1.11.0**, target `dev`, **4 threads**.
- Discovered: **23 models** (12 views, 10 tables, 1 incremental), **2 snapshots**, **196 data tests**, **7 sources**.
- Isolated `dbt build`: **32.96 seconds**, **PASS=221, WARN=0, ERROR=0, SKIP=0, NO-OP=0, REUSED=0**.
- Example model timings: `fct_order_items` created **2,829,252 rows in 4.81s**; incremental `fct_orders` reported **MERGE 0 in 15.12s**.
- Both snapshots succeeded and reported `INSERT 0 0` in this run.

Commands run from Git Bash (path conversion disabled for Linux container paths):

```bash
MSYS_NO_PATHCONV=1 docker compose exec airflow-scheduler dbt ls --project-dir /opt/airflow/dbt/ecommerce --profiles-dir /opt/airflow/dbt/profiles --resource-type model
MSYS_NO_PATHCONV=1 docker compose exec airflow-scheduler dbt ls --project-dir /opt/airflow/dbt/ecommerce --profiles-dir /opt/airflow/dbt/profiles --resource-type snapshot
MSYS_NO_PATHCONV=1 docker compose exec airflow-scheduler dbt ls --project-dir /opt/airflow/dbt/ecommerce --profiles-dir /opt/airflow/dbt/profiles --resource-type test
MSYS_NO_PATHCONV=1 docker compose exec airflow-scheduler dbt build --project-dir /opt/airflow/dbt/ecommerce --profiles-dir /opt/airflow/dbt/profiles
```

Note: the isolated `dbt ls --resource-type snapshot` request encountered a transient Docker Engine HTTP 500; the other successful dbt commands independently reported **2 snapshots**, and the build executed both.

## End-to-end Airflow run

- DAG: `ecommerce_intelligence_pipeline`
- Run: `manual_2026-11-23T01:09:02+00:00`
- Trigger: manual, observed in the Airflow UI.
- UI start: **2026-11-22 22:09:04**; end: **22:11:04** (local UI time).
- UI duration: **00:02:00**; DAG state: **success**.
- Task groups: ingestion, transformation, ai — **all succeeded**.
- Task instances: **6/6 succeeded**, one attempt each:
  - `ingestion.generate_data`
  - `ingestion.prepare_staging`
  - `ingestion.load_raw`
  - `transformation.dbt_snapshot`
  - `transformation.dbt_build`
  - `ai.generate_business_brief`

Reproduction: start the Docker Compose services, open Airflow at `http://localhost:8080`, manually trigger `ecommerce_intelligence_pipeline`, and inspect the DAG run details for its duration, state and task instance outcomes. **The isolated dbt build duration is not the same measurement as the full DAG duration.** This DAG run includes synthetic-data generation, staging, RAW loading, snapshots, transformations and AI report generation.

## Existing RAW UPSERT reference

A previously observed RAW synchronization baseline reported **0 affected rows across five synchronized tables in 10.75 seconds**. This is a **separate prior measurement**, not a timing extracted from the Airflow run or the dbt build above. Its original command output and precise measurement date were not provided with the present evidence; treat it as a historical reference, not a newly reproduced result.

## Interpretation and limits

These observations establish a reproducible local quality/performance reference for the current synthetic dataset and warm environment. They do **not** establish cold-start performance, throughput at other dataset sizes, or production SLAs. To compare future changes fairly, retain the dataset size, environment, thread count and run mode alongside the timing.
