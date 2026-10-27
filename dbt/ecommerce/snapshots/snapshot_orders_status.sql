{% snapshot snapshot_orders_status %}

{{
    config(
        target_schema='snapshots',
        unique_key='order_id',
        strategy='check',
        check_cols=[
            'order_status',
            'shipping_type'
        ]
    )
}}

select
    order_id,
    order_status,
    shipping_type

from {{ ref('stg_orders') }}

{% endsnapshot %}