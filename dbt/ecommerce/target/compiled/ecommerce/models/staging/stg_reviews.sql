with source as (

    select *
    from "ecommerce"."raw"."reviews"

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