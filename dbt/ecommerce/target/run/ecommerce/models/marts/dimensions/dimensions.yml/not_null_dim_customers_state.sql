
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select state
from "ecommerce"."analytics_marts"."dim_customers"
where state is null



  
  
      
    ) dbt_internal_test