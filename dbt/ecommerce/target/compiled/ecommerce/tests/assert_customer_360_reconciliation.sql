with orders_metrics as (

    select
        customer_id,
        count(*) as total_orders,

        count(*) filter (
            where order_status = 'completed'
        ) as completed_orders,

        count(*) filter (
            where order_status = 'processing'
        ) as processing_orders,

        count(*) filter (
            where order_status = 'cancelled'
        ) as cancelled_orders,

        coalesce(
            sum(net_amount) filter (
                where order_status = 'completed'
            ), 0
        ) as lifetime_revenue

    from "ecommerce"."analytics_marts"."fct_orders"
    group by customer_id

),

customer_360 as (

    select
        customer_id,
        total_orders,
        completed_orders,
        processing_orders,
        cancelled_orders,
        lifetime_revenue

    from "ecommerce"."analytics_marts"."mart_customer_360"

)

select
    coalesce(o.customer_id, c.customer_id) as customer_id,

    o.total_orders as expected_orders,
    c.total_orders as actual_orders,

    o.lifetime_revenue as expected_revenue,
    c.lifetime_revenue as actual_revenue

from orders_metrics o

full outer join customer_360 c
    on o.customer_id = c.customer_id

where
    c.customer_id is null

    or coalesce(o.total_orders, 0)
        <> coalesce(c.total_orders, 0)

    or coalesce(o.completed_orders, 0)
        <> coalesce(c.completed_orders, 0)

    or coalesce(o.processing_orders, 0)
        <> coalesce(c.processing_orders, 0)

    or coalesce(o.cancelled_orders, 0)
        <> coalesce(c.cancelled_orders, 0)

    or abs(
        coalesce(o.lifetime_revenue, 0)
        - coalesce(c.lifetime_revenue, 0)
    ) > 0.01