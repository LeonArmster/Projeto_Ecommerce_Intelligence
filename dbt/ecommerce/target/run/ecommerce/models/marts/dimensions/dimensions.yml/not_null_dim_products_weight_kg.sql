
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select weight_kg
from "ecommerce"."analytics_marts"."dim_products"
where weight_kg is null



  
  
      
    ) dbt_internal_test