# Synthetic Dataset and Data Ingestion

## Synthetic Dataset

The platform uses a synthetic e-commerce dataset so the entire project can be publicly reproduced without exposing proprietary or sensitive information.

The dataset contains seven main entities:

| Entity | Approximate Volume |
|---|---:|
| Customers | 100,000 |
| Products | 20,000 |
| Orders | 1,000,000 |
| Order Items | ~2,750,000 |
| Payments | 1,000,000 |
| Shipments | ~960,000 |
| Reviews | ~576,000 |

The initial dataset contains approximately **6.4 million records**. Volumes grow as the incremental generator creates additional transactional records; the figures above are baseline estimates, not fixed current counts.

The generator includes intentional relationships between variables to create realistic analytical patterns.

Examples include:

- demand seasonality;
- different customer purchasing profiles;
- shipping method impact on delivery performance;
- regional logistical complexity;
- delivery delays affecting customer ratings;
- discount effects on demand;
- category-specific price behavior.

The goal is not to perfectly reproduce a real e-commerce company, but to create a sufficiently complex environment for practicing Data Engineering, Analytics Engineering, Machine Learning and AI.

---

## Data Ingestion

The platform supports **two ingestion modes**: an initial full load and a recurring incremental workflow. Both use Parquet as the persistent synthetic-data format and pipe-delimited CSV files as PostgreSQL ingestion staging.

```text
                     INITIAL LOAD                      INCREMENTAL RUN
                  (bootstrap / reset)                  (daily workflow)
                          │                                   │
                 Full data generation                Incremental generation
                          │                                   │
                          └───────────┬───────────────────────┘
                                      ▼
                                 Parquet files
                                      │
                                      ▼
                               CSV staging files
                                      │
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
                TRUNCATE + COPY              Temporary tables +
                 (load_raw.py)                COPY FROM STDIN +
                                             INSERT / UPSERT
                                             (load_upsert.py)
                       │                             │
                       └──────────────┬──────────────┘
                                      ▼
                              PostgreSQL RAW
                                      │
                                      ▼
                               dbt + AI layer
```

## Initial Full Load

`ecommerce_intelligence.load.load_raw` is retained for initial database population or deliberate reloads. It uses `TRUNCATE` and PostgreSQL `COPY` to load the seven RAW entities: `customers`, `products`, `orders`, `order_items`, `payments`, `shipments`, and `reviews`.

## Incremental Synthetic Data Generation

`ecommerce_intelligence.generator.generate_incremental` updates the existing synthetic datasets without recreating the complete history. `customers` and `products` remain static reference datasets; the five transactional datasets are maintained incrementally:

- **Orders:** generate new orders for dates not yet processed.
- **Order items:** generate items for newly created orders.
- **Payments:** generate payments for new orders and update pending payment outcomes.
- **Shipments:** create eligible shipment records and update pending shipping/delivery events.
- **Reviews:** generate eligible reviews for delivered orders.

The generator uses existing Parquet data to determine what needs to be created or updated. Re-running it without new eligible data should not create duplicate business records.

## CSV Staging

`ecommerce_intelligence.transform.prepare_staging` converts the seven Parquet datasets to pipe-delimited CSV files. Generator-only scheduling columns (such as `scheduled_paid_at`, `scheduled_shipped_at`, and `scheduled_delivered_at`) are excluded from the corresponding CSV exports because they are not part of the RAW table schemas.

## Incremental PostgreSQL RAW Loading

`ecommerce_intelligence.load.load_upsert` orchestrates the five transactional RAW tables in dependency order:

```text
orders → order_items → payments → shipments → reviews
```

A reusable `upsert_table()` function in `load/upsert_database.py` performs each table load within a database transaction:

1. Create a temporary table using a table-specific SQL file.
2. Stream the CSV into the temporary table using PostgreSQL `COPY FROM STDIN`.
3. Execute the table-specific `INSERT ... ON CONFLICT` statement.
4. Commit on success or roll back the table transaction on failure.

SQL is kept in separate files under `sql/`, following the naming convention `create_temp_<table>.sql`, `copy_temp_<table>.sql`, and `upsert_<table>.sql`.

| RAW table | Conflict strategy |
|---|---|
| `orders` | Update existing orders only when values differ |
| `order_items` | Insert missing items; ignore existing IDs |
| `payments` | Update payment status and other changed fields |
| `shipments` | Update shipping and delivery fields when changed |
| `reviews` | Insert missing reviews; ignore existing IDs |

This design avoids duplicate records and unnecessary updates during repeated loads. The loader still reads the **full historical CSV** for each transactional table; incremental behavior currently applies to the database changes, not to the volume of CSV data scanned. Delta-only CSV extraction is a potential future optimization, not part of the current implementation.

**Validation:** A completed incremental RAW run processed all five tables with **zero affected rows in 10.75 seconds** when the destination was already synchronized. The complete Airflow workflow was also executed successfully after the integration changes.

---
