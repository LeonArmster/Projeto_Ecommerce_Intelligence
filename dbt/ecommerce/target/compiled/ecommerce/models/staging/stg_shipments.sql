with source as (

    select *
    from "ecommerce"."raw"."shipments"

),

renamed as (

    select
        shipment_id,
        order_id,
        shipped_at,
        estimated_delivery_date as estimated_delivery_at,
        delivered_at

    from source

)

select *
from renamed