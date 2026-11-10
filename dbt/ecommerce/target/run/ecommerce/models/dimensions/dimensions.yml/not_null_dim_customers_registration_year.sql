
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select registration_year
from "ecommerce"."analytics"."dim_customers"
where registration_year is null



  
  
      
    ) dbt_internal_test