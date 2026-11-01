select
    order_date,
    net_amount,
    previous_net_amount,
    net_sales_change_pct,
    valid_orders,
    previous_valid_orders,
    orders_change_pct,
    avg_order_value,
    previous_avg_order_value,
    avg_order_value_change_pct,
    cancellation_rate,
    previous_cancellation_rate,
    cancellation_rate_change_pp,
    delay_rate,
    previous_delay_rate,
    delay_rate_change_pp,
    avg_rating,
    previous_avg_rating,
    avg_rating_change
from 
    analytics_marts.mart_business_daily_summary
where 
    previous_net_amount is not null

order by 
    order_date desc

limit 1;