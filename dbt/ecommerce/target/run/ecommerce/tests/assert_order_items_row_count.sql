
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  with source_count as (

    select count(*) as total
    from "ecommerce"."analytics_staging"."stg_order_items"

),

fact_count as (

    select count(*) as total
    from "ecommerce"."analytics_marts"."fct_order_items"

)

select
    source_count.total as source_rows,
    fact_count.total as fact_rows

from source_count
cross join fact_count

where source_count.total <> fact_count.total
  
  
      
    ) dbt_internal_test