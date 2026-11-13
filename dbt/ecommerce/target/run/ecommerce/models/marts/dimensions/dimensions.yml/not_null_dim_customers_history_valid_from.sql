
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select valid_from
from "ecommerce"."analytics_marts"."dim_customers_history"
where valid_from is null



  
  
      
    ) dbt_internal_test