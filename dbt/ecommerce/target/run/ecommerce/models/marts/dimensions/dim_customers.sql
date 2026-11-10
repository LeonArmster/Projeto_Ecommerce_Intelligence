
  
    

  create  table "ecommerce"."analytics_marts"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    

with customers as (

    select
        customer_id,
        birth_date,
        state,
        created_at

    from "ecommerce"."analytics_staging"."stg_customers"

),

final as (

    select
        customer_id,
        birth_date,
        state,
        created_at,

        created_at::date as registration_date,

        extract(year from created_at)::int
            as registration_year,

        extract(month from created_at)::int
            as registration_month

    from customers

)

select *
from final
  );
  