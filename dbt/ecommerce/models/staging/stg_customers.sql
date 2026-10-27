with source as (

    select *
    from {{ source('ecommerce_raw', 'customers') }}

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