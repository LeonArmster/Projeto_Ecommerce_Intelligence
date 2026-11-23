with validated as (
    select
        *,
        count(*) over (
            partition by cohort_month, activity_month
        ) as rows_per_grain
    from {{ ref('mart_customer_cohort_retention') }}
)
select *
from validated
where rows_per_grain <> 1
   or cohort_month > activity_month
   or months_since_first_purchase < 0
   or cohort_customers <= 0
   or active_customers < 0
   or active_customers > cohort_customers
   or retention_rate_pct < 0
   or retention_rate_pct > 100
   or (months_since_first_purchase = 0
       and (active_customers <> cohort_customers or retention_rate_pct <> 100))
   or months_since_first_purchase is distinct from (
       (extract(year from activity_month) - extract(year from cohort_month)) * 12
       + extract(month from activity_month) - extract(month from cohort_month)
   )::integer
