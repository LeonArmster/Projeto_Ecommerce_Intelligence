
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select discount_amount
from "ecommerce"."analytics_marts"."mart_product_performance"
where discount_amount is null



  
  
      
    ) dbt_internal_test