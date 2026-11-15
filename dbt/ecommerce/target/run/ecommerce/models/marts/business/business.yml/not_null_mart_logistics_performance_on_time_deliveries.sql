
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select on_time_deliveries
from "ecommerce"."analytics_marts"."mart_logistics_performance"
where on_time_deliveries is null



  
  
      
    ) dbt_internal_test