
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        shipping_type as value_field,
        count(*) as n_records

    from "ecommerce"."analytics_staging"."stg_orders"
    group by shipping_type

)

select *
from all_values
where value_field not in (
    'economy','standard','express'
)



  
  
      
    ) dbt_internal_test