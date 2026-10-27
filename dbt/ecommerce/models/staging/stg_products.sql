with source as (

    select *
    from {{ source('ecommerce_raw', 'products') }}

),

renamed as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from source

)

select *
from renamed