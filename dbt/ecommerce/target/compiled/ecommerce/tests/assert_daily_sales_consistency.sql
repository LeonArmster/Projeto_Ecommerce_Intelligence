select
    order_date,
    total_orders,
    valid_orders,
    cancelled_orders

from "ecommerce"."analytics_marts"."fct_daily_sales"

where
    total_orders <> valid_orders + cancelled_orders