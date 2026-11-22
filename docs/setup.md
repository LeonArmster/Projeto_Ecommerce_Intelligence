# Local Development Setup and Execution

## Environment Configuration

Create a `.env` file based on `.env.example`.

Example:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce
POSTGRES_PASSWORD=ecommerce

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin

LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:8b
OLLAMA_BASE_URL=http://localhost:11434
```

Inside Docker, the Ollama endpoint must point to the host:

```text
http://host.docker.internal:11434
```

Never commit real credentials or secrets to Git.

---

## Local Development Setup

## Requirements

Recommended environment:

- Python 3.12
- uv
- Docker Desktop
- Docker Compose
- Ollama
- Git

For GPU-accelerated local inference, a compatible NVIDIA GPU is recommended but not required for understanding the architecture.

---

## Python Environment

Create the environment:

```bash
uv sync
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## Ollama Setup

Install Ollama and download the model:

```bash
ollama pull qwen3:8b
```

Verify the model:

```bash
ollama list
```

The local API should be available at:

```text
http://localhost:11434
```

---

## Start the Platform

Start the Docker services:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

The environment includes services for:

- PostgreSQL;
- pgAdmin;
- Airflow metadata database;
- Airflow scheduler;
- Airflow API/web services.

---

## Running dbt

Validate the dbt connection:

```bash
uv run dbt debug \
  --project-dir dbt/ecommerce \
  --profiles-dir dbt/profiles
```

Build analytical models and run tests:

```bash
uv run dbt build \
  --project-dir dbt/ecommerce \
  --profiles-dir dbt/profiles
```

Run snapshots:

```bash
uv run dbt snapshot \
  --project-dir dbt/ecommerce \
  --profiles-dir dbt/profiles
```

---

## Running the AI Business Brief Locally

The Business Brief can be executed independently:

```bash
uv run python -m ecommerce_intelligence.ai.business_brief
```

This process:

1. reads validated analytical metrics;
2. builds the business context;
3. applies deterministic business rules;
4. calls the configured LLM provider;
5. validates the structured output;
6. persists the result in PostgreSQL.

---

## Running through Airflow

The main DAG is `ecommerce_intelligence_pipeline`, defined in `airflow/dags/ecommerce_pipeline.py`.

After starting Docker Compose, check DAG discovery and the configured executor:

```powershell
docker compose exec airflow-scheduler airflow dags list
docker compose exec airflow-scheduler airflow config get-value core executor
```

The validated development setup uses `LocalExecutor`; no dedicated Celery worker is required. The DAG can be triggered manually through the Airflow UI at `http://localhost:8080`.

The incremental ingestion modules can also be run locally, independently of Airflow:

```powershell
uv run python -m ecommerce_intelligence.generator.generate_incremental
uv run python -m ecommerce_intelligence.transform.prepare_staging
uv run python -m ecommerce_intelligence.load.load_upsert
```

For a fresh database, use the existing initial-generation and `ecommerce_intelligence.load.load_raw` bootstrap path first. Do not substitute the incremental generator for the initial dataset creation process.

The DAG is configured for daily scheduling (`0 6 * * *`). Confirm the intended timezone and unpause the DAG only when automatic execution is desired. Successful manual runs validate the workflow but do not, by themselves, confirm that a scheduled run has occurred.

---
