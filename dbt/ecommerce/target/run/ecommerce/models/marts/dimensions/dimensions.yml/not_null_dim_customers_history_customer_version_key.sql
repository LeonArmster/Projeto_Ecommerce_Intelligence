
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_version_key
from "ecommerce"."analytics_marts"."dim_customers_history"
where customer_version_key is null



  
  
      
    ) dbt_internal_test