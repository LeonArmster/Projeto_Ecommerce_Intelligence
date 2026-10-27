with source as (

    select *
    from "ecommerce"."raw"."payments"

),

renamed as (

    select
        payment_id,
        order_id,
        payment_method,
        payment_amount,
        installments,
        payment_status,
        paid_at

    from source

)

select *
from renamed