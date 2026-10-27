with shipments as (

    select *
    from "ecommerce"."analytics_staging"."stg_shipments"

),

enriched as (

    select
        shipment_id,
        order_id,
        shipped_at,
        estimated_delivery_at,
        delivered_at,

        delivered_at - shipped_at
            as delivery_duration,

        case
            when delivered_at is null then null

            when delivered_at > estimated_delivery_at
                then true

            else false
        end as is_delayed

    from shipments

)

select *
from enriched