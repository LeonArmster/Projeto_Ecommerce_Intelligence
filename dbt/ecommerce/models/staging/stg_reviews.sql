with source as (

    select *
    from {{ source('ecommerce_raw', 'reviews') }}

),

renamed as (

    select
        review_id,
        order_id,
        rating,
        created_at as reviewed_at

    from source

)

select *
from renamed