
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select shipped_at
from "ecommerce"."analytics_intermediate"."int_shipments_enriched"
where shipped_at is null



  
  
      
    ) dbt_internal_test