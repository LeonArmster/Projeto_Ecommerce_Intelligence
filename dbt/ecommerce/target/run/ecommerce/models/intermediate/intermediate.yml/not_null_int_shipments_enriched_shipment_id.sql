
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select shipment_id
from "ecommerce"."analytics_intermediate"."int_shipments_enriched"
where shipment_id is null



  
  
      
    ) dbt_internal_test