{{ config(materialized='table') }}

{% set reference_date = var('customer_reference_date', run_started_at.strftime('%Y-%m-%d')) %}

with completed_orders as (

    select
        customer_id,
        order_at::date as order_date,
        date_trunc('month', order_at)::date as order_month

    from {{ ref('fct_orders') }}
    where order_status = 'completed'
      and order_at::date <= '{{ reference_date }}'::date

),

first_purchases as (

    select
        customer_id,
        min(order_month) as cohort_month

    from completed_orders
    group by customer_id

),

cohort_sizes as (

    select
        cohort_month,
        count(*) as cohort_customers

    from first_purchases
    group by cohort_month

),

monthly_activity as (

    select distinct
        f.cohort_month,
        o.order_month as activity_month,
        o.customer_id

    from completed_orders o
    inner join first_purchases f
        on o.customer_id = f.customer_id

),

retained_customers as (

    select
        cohort_month,
        activity_month,
        count(*) as active_customers

    from monthly_activity
    group by cohort_month, activity_month

),

cohort_months as (

    select
        c.cohort_month,
        gs.activity_month::date as activity_month,
        c.cohort_customers

    from cohort_sizes c
    cross join lateral generate_series(
        c.cohort_month,
        date_trunc('month', '{{ reference_date }}'::date)::date,
        interval '1 month'
    ) as gs(activity_month)

)

select
    cm.cohort_month,
    cm.activity_month,
    (
        (extract(year from cm.activity_month) - extract(year from cm.cohort_month)) * 12
        + extract(month from cm.activity_month) - extract(month from cm.cohort_month)
    )::integer as months_since_first_purchase,
    cm.cohort_customers,
    coalesce(r.active_customers, 0) as active_customers,
    round(
        100.0 * coalesce(r.active_customers, 0)
        / nullif(cm.cohort_customers, 0),
        2
    ) as retention_rate_pct

from cohort_months cm
left join retained_customers r
    on cm.cohort_month = r.cohort_month
   and cm.activity_month = r.activity_month
