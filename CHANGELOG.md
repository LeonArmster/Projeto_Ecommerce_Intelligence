# Changelog

Notable project changes are recorded here. This project uses versioned GitHub releases; entries describe features actually delivered, not future plans.

## [Unreleased]

### Added
- Lightweight repository documentation, quality tooling and pipeline baseline for the v1.1 development cycle.
- Python unit tests and GitHub Actions checks.
- Engineering conventions (`AGENTS.md`), Ruff and pre-commit guidance.
- Reproducible local pipeline baseline in `docs/baseline.md`.

## [v1.0.0] — 2026-11-21

First stable end-to-end E-Commerce Intelligence platform release.

### Added
- Synthetic e-commerce data generation across seven entities, with Parquet storage and CSV staging.
- Initial PostgreSQL bulk load and incremental, idempotent RAW ingestion using staging tables, `COPY` and `ON CONFLICT`.
- dbt staging, intermediate and marts layers, incremental order facts, daily sales metrics, snapshots and data-quality tests.
- Docker Compose environment and Airflow orchestration for ingestion, transformations, quality gates and AI reporting.
- Local Ollama / Qwen3 8B AI Business Briefs using deterministic KPIs, severity rules, JSON Schema validation and idempotent PostgreSQL persistence.

### Known limitations at release
- Incremental ingestion still processes historical CSV files.
- Synthetic-data integrity can be refined further.
- Local AI depends on host Ollama availability.
- Automated Python tests and CI were planned for subsequent development (and have since been introduced in the unreleased v1.1 cycle).

[v1.0.0]: https://github.com/LeonArmster/Projeto_Ecommerce_Intelligence/releases/tag/v1.0.0
