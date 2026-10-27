
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select category
from "ecommerce"."analytics_intermediate"."int_order_items_enriched"
where category is null



  
  
      
    ) dbt_internal_test