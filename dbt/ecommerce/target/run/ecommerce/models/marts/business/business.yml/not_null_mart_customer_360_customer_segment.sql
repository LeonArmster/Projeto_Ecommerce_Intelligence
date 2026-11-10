
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_segment
from "ecommerce"."analytics_marts"."mart_customer_360"
where customer_segment is null



  
  
      
    ) dbt_internal_test