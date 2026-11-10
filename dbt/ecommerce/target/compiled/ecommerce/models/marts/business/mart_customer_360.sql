

with customers as (

    select
        customer_id,
        birth_date,
        state,
        created_at,
        registration_date

    from "ecommerce"."analytics_marts"."dim_customers"

),

orders as (

    select
        customer_id,
        order_id,
        order_at,
        order_status,
        net_amount

    from "ecommerce"."analytics_marts"."fct_orders"

),

customer_metrics as (

    select
        customer_id,

        count(*) as total_orders,

        count(*) filter (
            where order_status = 'completed'
        ) as completed_orders,

        count(*) filter (
            where order_status = 'cancelled'
        ) as cancelled_orders,

        count(*) filter (
            where order_status = 'processing'
        ) as processing_orders,

        coalesce(
            sum(net_amount) filter (
                where order_status = 'completed'
            ), 0
        ) as lifetime_revenue,

        min(order_at) filter (
            where order_status = 'completed'
        ) as first_purchase_at,

        max(order_at) filter (
            where order_status = 'completed'
        ) as last_purchase_at

    from orders
    group by customer_id

),

final as (

    select
        c.customer_id,
        c.birth_date,
        c.state,
        c.created_at,
        c.registration_date,

        coalesce(m.total_orders, 0) as total_orders,
        coalesce(m.completed_orders, 0) as completed_orders,
        coalesce(m.cancelled_orders, 0) as cancelled_orders,
        coalesce(m.processing_orders, 0) as processing_orders,

        coalesce(m.lifetime_revenue, 0) as lifetime_revenue,

        case
            when m.completed_orders > 0
            then round(
                m.lifetime_revenue
                / m.completed_orders, 2
            )
            else 0
        end as average_order_value,

        m.first_purchase_at,
        m.last_purchase_at,

        case
            when m.last_purchase_at is not null
            then (
                '2026-11-09'::date
                - m.last_purchase_at::date
            )
        end as days_since_last_purchase

    from customers c

    left join customer_metrics m
        on c.customer_id = m.customer_id

)

select
    *,

    case
        when completed_orders = 0
            then 'no_purchase'

        when days_since_last_purchase < 0
            then 'future_purchase'

        when completed_orders = 1
            and days_since_last_purchase <= 90
            then 'new_customer'

        when completed_orders >= 2
            and days_since_last_purchase <= 90
            then 'active_repeat'

        when days_since_last_purchase <= 180
            then 'at_risk'

        else 'inactive'

    end as customer_segment

from final