
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select order_status
from "ecommerce"."analytics_intermediate"."int_orders_enriched"
where order_status is null



  
  
      
    ) dbt_internal_test