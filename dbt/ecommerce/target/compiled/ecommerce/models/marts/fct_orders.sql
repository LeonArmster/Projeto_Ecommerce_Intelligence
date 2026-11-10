

with orders as (

    select *
    from "ecommerce"."analytics_intermediate"."int_orders_enriched"

),

hashed_orders as (

    select
        orders.*,

        md5(
            to_jsonb(orders)::text
        ) as record_hash

    from orders

),

changed_orders as (

    select h.*

    from hashed_orders h

    

    left join "ecommerce"."analytics_marts"."fct_orders" existing
        on h.order_id = existing.order_id

    where
        existing.order_id is null
        or existing.record_hash is distinct from h.record_hash

    

)

select *
from changed_orders