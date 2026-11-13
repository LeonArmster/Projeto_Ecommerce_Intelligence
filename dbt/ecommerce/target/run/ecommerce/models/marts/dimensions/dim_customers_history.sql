
  
    

  create  table "ecommerce"."analytics_marts"."dim_customers_history__dbt_tmp"
  
  
    as
  
  (
    

with snapshot_data as (

    select
        customer_id,
        birth_date,
        state,
        created_at,
        dbt_scd_id,
        dbt_valid_from,
        dbt_valid_to

    from "ecommerce"."snapshots"."snapshot_customers"

),

final as (

    select
        dbt_scd_id as customer_version_key,
        customer_id,
        birth_date,
        state,
        created_at,

        dbt_valid_from as valid_from,
        dbt_valid_to as valid_to,

        case
            when dbt_valid_to is null then true
            else false
        end as is_current

    from snapshot_data

)

select *
from final
  );
  