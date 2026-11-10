
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select gross_revenue
from "ecommerce"."analytics_marts"."mart_product_performance"
where gross_revenue is null



  
  
      
    ) dbt_internal_test