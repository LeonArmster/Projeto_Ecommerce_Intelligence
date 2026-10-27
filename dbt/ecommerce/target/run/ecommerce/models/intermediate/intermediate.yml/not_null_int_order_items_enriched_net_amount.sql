
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select net_amount
from "ecommerce"."analytics_intermediate"."int_order_items_enriched"
where net_amount is null



  
  
      
    ) dbt_internal_test