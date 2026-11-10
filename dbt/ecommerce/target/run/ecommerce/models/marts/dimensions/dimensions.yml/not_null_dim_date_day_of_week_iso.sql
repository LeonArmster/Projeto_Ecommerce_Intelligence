
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select day_of_week_iso
from "ecommerce"."analytics_marts"."dim_date"
where day_of_week_iso is null



  
  
      
    ) dbt_internal_test