with items as (

    select
        order_id,
        sum(gross_amount) as gross_amount,
        sum(discount_amount) as discount_amount,
        sum(net_amount) as net_amount

    from "ecommerce"."analytics_marts"."fct_order_items"

    group by order_id

),

orders as (

    select
        order_id,
        gross_amount,
        discount_amount,
        net_amount

    from "ecommerce"."analytics_marts"."fct_orders"

),

reconciliation as (

    select
        coalesce(i.order_id, o.order_id) as order_id,

        i.net_amount as items_net_amount,
        o.net_amount as orders_net_amount

    from items i

    full outer join orders o
        on i.order_id = o.order_id

)

select *
from reconciliation

where
    items_net_amount is null
    or orders_net_amount is null
    or abs(
        items_net_amount - orders_net_amount
    ) > 0.01