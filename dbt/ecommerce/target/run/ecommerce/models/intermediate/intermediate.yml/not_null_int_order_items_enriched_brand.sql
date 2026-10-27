
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select brand
from "ecommerce"."analytics_intermediate"."int_order_items_enriched"
where brand is null



  
  
      
    ) dbt_internal_test