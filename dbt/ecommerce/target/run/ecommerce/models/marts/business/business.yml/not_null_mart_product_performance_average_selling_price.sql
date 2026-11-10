
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select average_selling_price
from "ecommerce"."analytics_marts"."mart_product_performance"
where average_selling_price is null



  
  
      
    ) dbt_internal_test