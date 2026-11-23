# Engineering Guidelines — E-Commerce Intelligence

This file documents conventions for contributors and coding assistants. Keep changes focused, reproducible, and appropriate for a public portfolio project.

## Project boundaries

- Use only synthetic or explicitly public data. Never commit company data, credentials, tokens, production exports, or local `.env` files.
- Preserve the existing Python 3.12 / uv, PostgreSQL, dbt, Airflow, Docker Compose, and Ollama architecture unless a change is explicitly scoped and justified.
- Prefer small PRs linked to an Issue. Avoid unrelated refactoring, mass formatting, and speculative infrastructure.
- Keep README concise; put detailed operational instructions in `docs/`. Update documentation when behavior changes.

## Python and dependencies

- Application code belongs in `src/ecommerce_intelligence/`; tests belong in `tests/`.
- Run modules using `uv run python -m ecommerce_intelligence.<module>` where practical.
- Use the existing `uv.lock` for reproducible dependencies; do not update dependencies incidentally.
- Use logging rather than printing for operational pipeline events. Handle failures explicitly.
- Run `uv run pytest tests/ -v` and `uv run ruff check src tests airflow/dags` before proposing Python changes.
- Do not introduce new lint rules that require rewriting unrelated files.

## PostgreSQL RAW and ingestion

- Initial bootstrap uses `load_raw.py` (TRUNCATE + COPY); recurring ingestion uses `load_upsert.py` (temporary tables, COPY, UPSERT).
- Keep table-specific SQL in `sql/`: `create_temp_<table>.sql`, `copy_temp_<table>.sql`, `upsert_<table>.sql`.
- Respect primary keys, dependencies, and table order: orders → order_items → payments → shipments → reviews.
- Preserve idempotency: repeated loads of unchanged records should not duplicate rows or produce unnecessary updates.
- Keep writes transactional. Do not introduce destructive schema or data operations into recurring jobs.
- Note that current incremental loading still scans full historical CSV files; do not describe it as delta-only extraction.

## dbt models and data quality

- Use `staging` for source standardization, `intermediate` for reusable business logic, and `marts` for analytical consumption.
- State and preserve the grain of every model. For example, `int_orders_enriched` and `fct_orders` are one row per order; daily marts use an explicit date grain.
- Avoid accidental fanout when joining order items, payments, shipments, reviews, or customer history.
- Add or adjust dbt tests when changing keys, relationships, arithmetic, grains, or business rules. Prefer existing macros and patterns.
- Snapshots track historical changes; do not overwrite their meaning or invalidate historical keys casually.
- Run `dbt build` with the project and profiles directories documented in `docs/setup.md`.
- Metric suffixes are semantic contracts: `_amount` = monetary amount; `_orders` = count; `_rate` = decimal rate; `_change_pct` = relative percentage change; `_change_pp` = percentage-point change; `_change` = absolute difference. Do not mix units.

## AI and business briefs

- PostgreSQL/dbt calculate validated KPIs; Python applies deterministic metric direction and severity; the LLM interprets the supplied evidence.
- Do not let the LLM recalculate KPIs, invent values, infer unsupported causality, or confuse percentages with percentage points.
- Preserve the structured JSON Schema output contract, validation, and traceable persistence of context, provider, model, and result.
- Treat proposed causes as hypotheses requiring investigation, not established facts.
- Keep the LLM provider abstraction; Ollama currently runs locally with Qwen3 8B.

## Airflow and Docker

- The DAG `ecommerce_intelligence_pipeline` has three dependent TaskGroups: ingestion → transformation → ai.
- Within ingestion: incremental generation → CSV staging → RAW UPSERT. Within transformation: dbt snapshot → dbt build (including configured tests).
- AI must run only after successful transformations and data-quality checks. Preserve retries, task IDs, and execution timeouts unless the change requires otherwise.
- The DAG uses the America/Sao_Paulo timezone and a daily 06:00 schedule. Verify scheduling changes before enabling automatic runs.
- Airflow runs in Docker; host Ollama is accessed through `host.docker.internal:11434`, not the container's `localhost`.

## Validation and security

- Never commit real credentials, personal data, proprietary datasets, database dumps, or generated dbt artifacts.
- Keep `.env.example` illustrative; use environment variables for secrets.
- Before merging, verify the affected layer (Python tests, dbt build, DAG parse, or documentation links as appropriate).
- Record actual measured results; do not fabricate performance baselines or claim CI validates behavior it does not exercise.
