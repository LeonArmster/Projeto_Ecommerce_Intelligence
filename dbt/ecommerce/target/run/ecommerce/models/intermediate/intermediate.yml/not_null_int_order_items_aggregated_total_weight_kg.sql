
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_weight_kg
from "ecommerce"."analytics_intermediate"."int_order_items_aggregated"
where total_weight_kg is null



  
  
      
    ) dbt_internal_test