
    
    

with all_values as (

    select
        order_status as value_field,
        count(*) as n_records

    from "ecommerce"."analytics_staging"."stg_orders"
    group by order_status

)

select *
from all_values
where value_field not in (
    'completed','processing','cancelled'
)


