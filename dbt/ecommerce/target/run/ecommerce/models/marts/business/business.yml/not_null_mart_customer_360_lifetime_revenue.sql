
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select lifetime_revenue
from "ecommerce"."analytics_marts"."mart_customer_360"
where lifetime_revenue is null



  
  
      
    ) dbt_internal_test