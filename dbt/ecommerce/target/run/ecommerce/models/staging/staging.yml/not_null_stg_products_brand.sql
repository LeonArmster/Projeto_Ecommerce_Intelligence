
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select brand
from "ecommerce"."analytics_staging"."stg_products"
where brand is null



  
  
      
    ) dbt_internal_test