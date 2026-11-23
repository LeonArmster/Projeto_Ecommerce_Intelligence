# Business performance dashboard

Run from the repository root after PostgreSQL and dbt marts are available.

```bash
uv run --with streamlit --with matplotlib streamlit run dashboard/app.py
```

Set POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD and POSTGRES_PORT in the local .env or environment. DASHBOARD_DB_HOST defaults to localhost; use the published PostgreSQL host and port. Never commit credentials. Open http://localhost:8501.

The dashboard reads existing marts only, caches queries for five minutes, and uses a read-only transaction setting. Net sales use fct_daily_sales (non-cancelled orders); customer metrics use mart_customer_360 (completed orders); weighted retention and the heatmap use mart_customer_cohort_retention. Run dbt with its default reference date before viewing. The current calendar month is excluded from retention, not sales. Synthetic data is not a market benchmark.
