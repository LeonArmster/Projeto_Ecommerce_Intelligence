with orders as (

    select *
    from {{ ref('stg_orders') }}

),

customers as (

    select *
    from {{ ref('stg_customers') }}

),

order_items as (

    select *
    from {{ ref('int_order_items_aggregated') }}

),

payments as (

    select *
    from {{ ref('stg_payments') }}

),

shipments as (

    select *
    from {{ ref('int_shipments_enriched') }}

),

reviews as (

    select *
    from {{ ref('stg_reviews') }}

),

enriched as (

    select
        -- =====================================================
        -- Pedido
        -- =====================================================

        o.order_id,
        o.customer_id,
        o.order_at,
        o.order_status,
        o.shipping_type,

        -- =====================================================
        -- Cliente
        -- =====================================================

        c.state as customer_state,
        c.birth_date as customer_birth_date,
        c.created_at as customer_created_at,

        -- =====================================================
        -- Itens
        -- =====================================================

        oi.item_count,
        oi.distinct_products,
        oi.total_quantity,
        oi.gross_amount,
        oi.discount_amount,
        oi.net_amount,
        oi.total_weight_kg,

        -- =====================================================
        -- Pagamento
        -- =====================================================

        p.payment_id,
        p.payment_method,
        p.payment_amount,
        p.installments,
        p.payment_status,
        p.paid_at,

        -- =====================================================
        -- Logística
        -- =====================================================

        s.shipment_id,
        s.shipped_at,
        s.estimated_delivery_at,
        s.delivered_at,
        s.delivery_duration,
        s.is_delayed,

        -- =====================================================
        -- Avaliação
        -- =====================================================

        r.review_id,
        r.rating,
        r.reviewed_at

    from orders o

    left join customers c
        on o.customer_id = c.customer_id

    left join order_items oi
        on o.order_id = oi.order_id

    left join payments p
        on o.order_id = p.order_id

    left join shipments s
        on o.order_id = s.order_id

    left join reviews r
        on o.order_id = r.order_id

)

select *
from enriched