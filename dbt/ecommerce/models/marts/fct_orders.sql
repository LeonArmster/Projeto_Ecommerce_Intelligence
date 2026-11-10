{{
    config(
        materialized='incremental',
        unique_key='order_id',
        incremental_strategy='merge',
        on_schema_change='append_new_columns'
    )
}}

with orders as (

    select *
    from {{ ref('int_orders_enriched') }}

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

    {% if is_incremental() %}

    left join {{ this }} existing
        on h.order_id = existing.order_id

    where
        existing.order_id is null
        or existing.record_hash is distinct from h.record_hash

    {% endif %}

)

select *
from changed_orders
