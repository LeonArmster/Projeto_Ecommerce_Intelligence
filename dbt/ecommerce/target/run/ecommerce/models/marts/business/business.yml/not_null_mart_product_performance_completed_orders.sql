
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select completed_orders
from "ecommerce"."analytics_marts"."mart_product_performance"
where completed_orders is null



  
  
      
    ) dbt_internal_test