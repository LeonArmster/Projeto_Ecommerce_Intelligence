with source as (

    select *
    from {{ source('ecommerce_raw', 'orders') }}

),

renamed as (

    select
        order_id,
        customer_id,
        order_date as order_at,
        order_status,
        shipping_type

    from source

)

select *
from renamed