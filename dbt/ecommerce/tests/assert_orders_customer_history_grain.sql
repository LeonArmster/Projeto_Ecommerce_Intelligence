
select
    order_id,
    count(*) as total_rows

from {{ ref('int_orders_customer_history') }}

group by order_id

having count(*) <> 1
