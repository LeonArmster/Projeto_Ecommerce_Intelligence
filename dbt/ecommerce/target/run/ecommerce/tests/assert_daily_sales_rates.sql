
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    order_date,
    cancellation_rate,
    delay_rate,
    review_rate

from "ecommerce"."analytics_marts"."fct_daily_sales"

where
       cancellation_rate not between 0 and 1

    or delay_rate not between 0 and 1

    or review_rate not between 0 and 1
  
  
      
    ) dbt_internal_test