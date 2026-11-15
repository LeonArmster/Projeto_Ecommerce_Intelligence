
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select late_deliveries
from "ecommerce"."analytics_marts"."mart_logistics_performance"
where late_deliveries is null



  
  
      
    ) dbt_internal_test