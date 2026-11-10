
{{ config(
    materialized='table'
) }}

with products as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from {{ ref('stg_products') }}

),

final as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from products

)

select *
from final
