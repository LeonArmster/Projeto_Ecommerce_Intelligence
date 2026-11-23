# Analytics Engineering, Marts and Data Quality

## Analytics Engineering with dbt

dbt is responsible for transforming RAW data into reliable analytical models.

The transformation architecture follows three primary layers.

## Staging

The staging layer standardizes the source data.

Responsibilities include:

- column naming;
- data types;
- boolean normalization;
- timestamp normalization;
- basic validation;
- source tests.

Example models:

```text
stg_customers
stg_products
stg_orders
stg_order_items
stg_payments
stg_shipments
stg_reviews
```

---

## Intermediate

The intermediate layer contains reusable business transformations.

Examples:

### `int_order_items_enriched`

Enriches order items with product information and calculates:

- gross amount;
- discount amount;
- net amount.

### `int_order_items_aggregated`

Aggregates item-level information to one row per order.

### `int_shipments_enriched`

Calculates logistics metrics such as:

- delivery duration;
- delivery status;
- delay indicator.

### `int_orders_enriched`

Creates the central analytical order dataset by combining:

- customer;
- items;
- payments;
- shipments;
- reviews.

The model maintains a **one-row-per-order grain**.

---

## Analytical Marts

The marts layer contains datasets designed for analytical consumption.

## `fct_orders`

Incremental order fact table.

Main characteristics:

- unique `order_id`;
- incremental materialization;
- merge strategy;
- rolling lookback window to capture recent changes.

---

## `fct_daily_sales`

Daily business performance fact table.

Example metrics:

- total orders;
- valid orders;
- cancelled orders;
- customers;
- units sold;
- gross sales;
- discounts;
- net sales;
- delivered orders;
- delayed orders;
- reviewed orders;
- average rating;
- average order value;
- cancellation rate;
- delay rate;
- review rate.

Ratios are calculated using a reusable `safe_divide` dbt macro.

---

## Business Daily Summary

A dedicated analytical mart prepares metrics used by the AI layer.

It calculates comparisons such as:

```text
net_sales_change_pct
orders_change_pct
avg_order_value_change_pct

cancellation_rate_change_pp
delay_rate_change_pp

avg_rating_change
```

Metric naming follows a semantic contract:

| Suffix | Meaning |
|---|---|
| `_amount` | Monetary value |
| `_orders` | Count |
| `_rate` | Decimal rate |
| `_change_pct` | Relative percentage change |
| `_change_pp` | Percentage-point change |
| `_change` | Absolute change |

This semantic convention reduces ambiguity between the analytical and AI layers.

---

## Data Quality

Data quality is integrated directly into the dbt workflow.

The project uses tests such as:

- `not_null`;
- `unique`;
- relationships;
- accepted values;
- grain validation;
- arithmetic validation;
- business-rule validation.

Because `dbt build` executes models and their associated tests, the pipeline does not require a redundant standalone quality TaskGroup in V1.

Conceptually:

```text
Transformation
      │
      ▼
dbt build
      │
      ├── models
      └── tests
             │
             ▼
        tests passed?
          │      │
         YES     NO
          │      │
          ▼      ▼
         AI    Pipeline fails
```

The AI layer therefore only executes after the analytical models have successfully passed the configured data-quality checks.

---

## dbt Snapshots

Snapshots are used to preserve historical changes in mutable business entities.

The V1 implementation tracks changes in order status.

This introduces Slowly Changing Dimension concepts and allows historical analysis even when source records change over time.

---

## V2 Customer Analytics

`mart_customer_360` has one row per current customer. Repeat customers have at least two completed orders; days to second purchase measures calendar days between the first two completed purchases; monthly frequency is completed orders per 30 days of inclusive exposure since first purchase. `mart_customer_cohort_retention` has one row per first-purchase month and activity month, including zero-activity months. M0 is 100%; monthly retention is active customers divided by cohort size, not cumulative retention. Aggregate retention is weighted by eligible cohort size. Both models exclude orders after `customer_reference_date` (default dbt invocation date). Current order statuses and customer dimension are retained, so this is not a historical snapshot. The current month may be incomplete. Streamlit excludes the current calendar month from retention and uses non-cancelled net sales from `fct_daily_sales`.
