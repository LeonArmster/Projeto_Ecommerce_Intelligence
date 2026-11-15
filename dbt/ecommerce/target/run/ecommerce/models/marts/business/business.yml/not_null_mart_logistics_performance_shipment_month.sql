
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select shipment_month
from "ecommerce"."analytics_marts"."mart_logistics_performance"
where shipment_month is null



  
  
      
    ) dbt_internal_test