
{{ config(materialized='table') }}

with products as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from {{ ref('dim_products') }}

),

order_items as (

    select
        product_id,
        order_id,
        order_at,
        order_status,
        quantity,
        gross_amount,
        discount_amount,
        net_amount

    from {{ ref('fct_order_items') }}

),

product_metrics as (

    select
        product_id,

        count(distinct order_id) as total_orders,

        count(distinct order_id) filter (
            where order_status = 'completed'
        ) as completed_orders,

        coalesce(
            sum(quantity) filter (
                where order_status = 'completed'
            ), 0
        ) as units_sold,

        coalesce(
            sum(gross_amount) filter (
                where order_status = 'completed'
            ), 0
        ) as gross_revenue,

        coalesce(
            sum(discount_amount) filter (
                where order_status = 'completed'
            ), 0
        ) as discount_amount,

        coalesce(
            sum(net_amount) filter (
                where order_status = 'completed'
            ), 0
        ) as net_revenue,

        min(order_at) filter (
            where order_status = 'completed'
        ) as first_sale_at,

        max(order_at) filter (
            where order_status = 'completed'
        ) as last_sale_at

    from order_items
    group by product_id

),

final as (

    select
        p.product_id,
        p.category,
        p.brand,
        p.base_price,
        p.weight_kg,

        coalesce(m.total_orders, 0) as total_orders,
        coalesce(m.completed_orders, 0) as completed_orders,
        coalesce(m.units_sold, 0) as units_sold,

        coalesce(m.gross_revenue, 0) as gross_revenue,
        coalesce(m.discount_amount, 0) as discount_amount,
        coalesce(m.net_revenue, 0) as net_revenue,

        case
            when m.units_sold > 0
            then round(
                m.net_revenue / m.units_sold, 2
            )
            else 0
        end as average_selling_price,

        m.first_sale_at,
        m.last_sale_at

    from products p

    left join product_metrics m
        on p.product_id = m.product_id

)

select *
from final
