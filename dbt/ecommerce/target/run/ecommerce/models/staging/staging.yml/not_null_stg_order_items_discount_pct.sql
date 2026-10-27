
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select discount_pct
from "ecommerce"."analytics_staging"."stg_order_items"
where discount_pct is null



  
  
      
    ) dbt_internal_test