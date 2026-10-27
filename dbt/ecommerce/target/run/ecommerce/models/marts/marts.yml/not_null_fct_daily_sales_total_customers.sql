
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_customers
from "ecommerce"."analytics_marts"."fct_daily_sales"
where total_customers is null



  
  
      
    ) dbt_internal_test