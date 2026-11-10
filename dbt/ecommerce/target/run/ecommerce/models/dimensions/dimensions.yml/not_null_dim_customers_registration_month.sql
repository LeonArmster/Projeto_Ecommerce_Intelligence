
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select registration_month
from "ecommerce"."analytics"."dim_customers"
where registration_month is null



  
  
      
    ) dbt_internal_test