
{{ config(
    materialized='table'
) }}

with order_items as (

    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_pct,
        gross_amount,
        discount_amount,
        net_amount

    from {{ ref('int_order_items_enriched') }}

),

orders as (

    select
        order_id,
        customer_id,
        order_at,
        order_status,
        shipping_type

    from {{ ref('stg_orders') }}

),

final as (

    select
        oi.order_item_id,
        oi.order_id,
        oi.product_id,

        o.customer_id,

        o.order_at,
        to_char(o.order_at, 'YYYYMMDD')::integer
            as order_date_key,

        o.order_status,
        o.shipping_type,

        oi.quantity,
        oi.unit_price,
        oi.discount_pct,

        oi.gross_amount,
        oi.discount_amount,
        oi.net_amount

    from order_items oi

    inner join orders o
        on oi.order_id = o.order_id

)

select *
from final
