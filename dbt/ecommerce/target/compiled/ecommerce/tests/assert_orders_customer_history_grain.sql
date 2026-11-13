select
    order_id,
    count(*) as total_rows

from "ecommerce"."analytics_intermediate"."int_orders_customer_history"

group by order_id

having count(*) <> 1