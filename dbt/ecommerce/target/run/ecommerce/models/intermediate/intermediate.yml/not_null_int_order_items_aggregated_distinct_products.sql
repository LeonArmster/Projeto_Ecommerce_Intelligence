
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select distinct_products
from "ecommerce"."analytics_intermediate"."int_order_items_aggregated"
where distinct_products is null



  
  
      
    ) dbt_internal_test