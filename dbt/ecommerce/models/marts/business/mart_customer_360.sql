
{{ config(materialized='table') }}

with customers as (

    select
        customer_id,
        birth_date,
        state,
        created_at,
        registration_date

    from {{ ref('dim_customers') }}

),

orders as (

    select
        customer_id,
        order_id,
        order_at,
        order_status,
        net_amount

    from {{ ref('fct_orders') }}

),

ranked_completed_orders as (

    select
        customer_id,
        order_at,
        row_number() over (
            partition by customer_id
            order by order_at, order_id
        ) as purchase_number

    from orders
    where order_status = 'completed'

),

second_purchases as (

    select
        customer_id,
        max(order_at) filter (
            where purchase_number = 2
        ) as second_purchase_at

    from ranked_completed_orders
    where purchase_number <= 2
    group by customer_id

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

        (coalesce(m.completed_orders, 0) >= 2) as is_repeat_customer,

        case
            when sp.second_purchase_at is not null
            then sp.second_purchase_at::date - m.first_purchase_at::date
        end as days_to_second_purchase,

        case
            when m.completed_orders > 0
             and m.first_purchase_at::date <= '{{ var("customer_reference_date", run_started_at.strftime("%Y-%m-%d")) }}'::date
            then round(
                m.completed_orders::numeric * 30.0
                / greatest(
                    '{{ var("customer_reference_date", run_started_at.strftime("%Y-%m-%d")) }}'::date
                    - m.first_purchase_at::date + 1,
                    1
                ),
                2
            )
        end as purchase_frequency_per_month,

        case
            when m.last_purchase_at is not null
            then (
                '{{ var("customer_reference_date", run_started_at.strftime("%Y-%m-%d")) }}'::date
                - m.last_purchase_at::date
            )
        end as days_since_last_purchase

    from customers c

    left join customer_metrics m
        on c.customer_id = m.customer_id

    left join second_purchases sp
        on c.customer_id = sp.customer_id

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
