
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select shipping_type
from "ecommerce"."analytics_staging"."stg_orders"
where shipping_type is null



  
  
      
    ) dbt_internal_test