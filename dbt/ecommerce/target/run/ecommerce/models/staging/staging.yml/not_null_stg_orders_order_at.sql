
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select order_at
from "ecommerce"."analytics_staging"."stg_orders"
where order_at is null



  
  
      
    ) dbt_internal_test