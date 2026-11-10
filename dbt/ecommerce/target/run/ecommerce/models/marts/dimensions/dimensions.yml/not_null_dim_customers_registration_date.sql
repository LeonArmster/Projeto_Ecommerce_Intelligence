
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select registration_date
from "ecommerce"."analytics_marts"."dim_customers"
where registration_date is null



  
  
      
    ) dbt_internal_test