
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    order_date,
    total_orders,
    valid_orders,
    cancelled_orders

from "ecommerce"."analytics_marts"."fct_daily_sales"

where
    total_orders <> valid_orders + cancelled_orders
  
  
      
    ) dbt_internal_test