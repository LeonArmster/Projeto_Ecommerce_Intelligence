with source as (

    select *
    from "ecommerce"."raw"."customers"

),

renamed as (

    select
        customer_id,
        birth_date,
        state,
        created_at

    from source

)

select *
from renamed