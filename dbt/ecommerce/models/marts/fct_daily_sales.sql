with orders as (

    select *
    from {{ ref('int_orders_enriched') }}

),

daily as (

    select
        order_at::date as order_date,

        -- =====================================================
        -- Volume
        -- =====================================================

        count(*) as total_orders,

        count(*) filter (
            where order_status <> 'cancelled'
        ) as valid_orders,

        count(*) filter (
            where order_status = 'cancelled'
        ) as cancelled_orders,

        count(distinct customer_id) as total_customers,

        sum(
            case
                when order_status <> 'cancelled'
                    then total_quantity
                else 0
            end
        ) as total_units,

        -- =====================================================
        -- Financeiro
        -- =====================================================

        sum(
            case
                when order_status <> 'cancelled'
                    then gross_amount
                else 0
            end
        ) as gross_amount,

        sum(
            case
                when order_status <> 'cancelled'
                    then discount_amount
                else 0
            end
        ) as discount_amount,

        sum(
            case
                when order_status <> 'cancelled'
                    then net_amount
                else 0
            end
        ) as net_amount,

        -- =====================================================
        -- Experiência / Operação
        -- =====================================================

        count(*) filter (
            where is_delayed = true
        ) as delayed_orders,

        count(*) filter (
            where delivered_at is not null
        ) as delivered_orders,

        count(rating) as reviewed_orders,

        avg(rating) as avg_rating

    from orders

    group by 1

),

final as (

    select
        *,

        {{ safe_divide('net_amount', 'valid_orders') }}
            as avg_order_value,

        {{ safe_divide('cancelled_orders', 'total_orders') }}
            as cancellation_rate,

        {{ safe_divide('delayed_orders', 'delivered_orders') }}
            as delay_rate,

        {{ safe_divide('reviewed_orders', 'total_orders') }}
            as review_rate

    from daily

)

select *
from final