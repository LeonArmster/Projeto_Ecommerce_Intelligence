
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pending_shipments
from "ecommerce"."analytics_marts"."mart_logistics_performance"
where pending_shipments is null



  
  
      
    ) dbt_internal_test