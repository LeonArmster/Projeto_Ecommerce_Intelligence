
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    customer_id,
    count(*) as current_versions

from "ecommerce"."analytics_marts"."dim_customers_history"

where is_current = true

group by customer_id

having count(*) > 1
  
  
      
    ) dbt_internal_test