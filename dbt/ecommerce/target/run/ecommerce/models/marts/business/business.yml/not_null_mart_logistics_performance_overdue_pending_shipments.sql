
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select overdue_pending_shipments
from "ecommerce"."analytics_marts"."mart_logistics_performance"
where overdue_pending_shipments is null



  
  
      
    ) dbt_internal_test