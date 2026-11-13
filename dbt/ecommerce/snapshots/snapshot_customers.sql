
{% snapshot snapshot_customers %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['birth_date', 'state'],
        invalidate_hard_deletes=True
    )
}}

select
    customer_id,
    birth_date,
    state,
    created_at

from {{ source('ecommerce_raw', 'customers') }}

{% endsnapshot %}
