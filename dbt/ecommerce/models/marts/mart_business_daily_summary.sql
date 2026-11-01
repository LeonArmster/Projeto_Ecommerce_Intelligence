with daily as (

    select *
    from {{ ref('fct_daily_sales') }}

),

comparison as (

    select
        order_date,

        net_amount,
        valid_orders,
        avg_order_value,

        cancellation_rate,
        delay_rate,
        avg_rating,

        lag(net_amount) over (
            order by order_date
        ) as previous_net_amount,

        lag(valid_orders) over (
            order by order_date
        ) as previous_valid_orders,

        lag(avg_order_value) over (
            order by order_date
        ) as previous_avg_order_value,

        lag(cancellation_rate) over (
            order by order_date
        ) as previous_cancellation_rate,

        lag(delay_rate) over (
            order by order_date
        ) as previous_delay_rate,

        lag(avg_rating) over (
            order by order_date
        ) as previous_avg_rating

    from daily

),

final as (

    select
        *,

        {{ safe_divide(
            'net_amount - previous_net_amount',
            'previous_net_amount'
        ) }} as net_sales_change_pct,

        {{ safe_divide(
            'valid_orders - previous_valid_orders',
            'previous_valid_orders'
        ) }} as orders_change_pct,

        {{ safe_divide(
            'avg_order_value - previous_avg_order_value',
            'previous_avg_order_value'
        ) }} as avg_order_value_change_pct,

        (cancellation_rate - previous_cancellation_rate) * 100
            as cancellation_rate_change_pp,

        (delay_rate - previous_delay_rate) * 100
            as delay_rate_change_pp,

        avg_rating - previous_avg_rating
            as avg_rating_change

    from comparison

)

select *
from final