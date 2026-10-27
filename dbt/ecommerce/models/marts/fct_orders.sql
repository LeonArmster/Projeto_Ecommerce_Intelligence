{{
    config(
        materialized='incremental',
        unique_key='order_id',
        incremental_strategy='merge'
    )
}}

with orders as (

    select *
    from {{ ref('int_orders_enriched') }}

    {% if is_incremental() %}

        where order_at >= (
            select
                max(order_at) - interval '30 days'
            from {{ this }}
        )

    {% endif %}

),

final as (

    select
        order_id,
        customer_id,
        order_at,
        order_status,
        shipping_type,
        customer_state,
        customer_birth_date,
        customer_created_at,
        item_count,
        distinct_products,
        total_quantity,
        gross_amount,
        discount_amount,
        net_amount,
        total_weight_kg,
        payment_id,
        payment_method,
        payment_amount,
        installments,
        payment_status,
        paid_at,
        shipment_id,
        shipped_at,
        estimated_delivery_at,
        delivered_at,
        delivery_duration,
        is_delayed,
        review_id,
        rating,
        reviewed_at

    from orders

)

select *
from final