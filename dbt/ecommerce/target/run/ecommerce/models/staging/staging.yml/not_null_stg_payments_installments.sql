
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select installments
from "ecommerce"."analytics_staging"."stg_payments"
where installments is null



  
  
      
    ) dbt_internal_test