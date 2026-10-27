
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select valid_orders
from "ecommerce"."analytics_marts"."fct_daily_sales"
where valid_orders is null



  
  
      
    ) dbt_internal_test