



with shipments as (

    select
        shipment_id,
        order_id,
        shipped_at,
        estimated_delivery_at,
        delivered_at,
        delivery_duration,
        is_delayed

    from "ecommerce"."analytics_intermediate"."int_shipments_enriched"

),

orders as (

    select
        order_id,
        order_status,
        shipping_type

    from "ecommerce"."analytics_staging"."stg_orders"

),

shipment_base as (

    select
        s.shipment_id,
        s.order_id,
        o.shipping_type,

        date_trunc('month', s.shipped_at)::date
            as shipment_month,

        s.shipped_at,
        s.estimated_delivery_at,
        s.delivered_at,
        s.is_delayed,

        extract(epoch from s.delivery_duration)
            / 86400.0 as delivery_days,

        case
            when s.delivered_at > s.estimated_delivery_at
            then extract(
                epoch from (
                    s.delivered_at - s.estimated_delivery_at
                )
            ) / 86400.0
            else 0
        end as delay_days,

        case
            when s.delivered_at is null
             and s.estimated_delivery_at
                 < ('2026-11-09'::date + interval '1 day')
            then true
            else false
        end as is_overdue_pending

    from shipments s

    inner join orders o
        on s.order_id = o.order_id

    where o.order_status <> 'cancelled'
      and s.shipped_at is not null
      and s.shipped_at < ('2026-11-09'::date + interval '1 day')

),

monthly_metrics as (

    select
        shipment_month,
        shipping_type,

        count(*) as total_shipments,

        count(*) filter (
            where delivered_at is not null
        ) as delivered_shipments,

        count(*) filter (
            where delivered_at is null
        ) as pending_shipments,

        count(*) filter (
            where is_delayed = true
        ) as late_deliveries,

        count(*) filter (
            where is_delayed = false
        ) as on_time_deliveries,

        count(*) filter (
            where is_overdue_pending = true
        ) as overdue_pending_shipments,

        round(
            avg(delivery_days) filter (
                where delivered_at is not null
            )::numeric, 2
        ) as average_delivery_days,

        round(
            avg(delay_days) filter (
                where is_delayed = true
            )::numeric, 2
        ) as average_delay_days

    from shipment_base

    group by
        shipment_month,
        shipping_type

)

select
    *,

    round(
        100.0 * on_time_deliveries
        / nullif(delivered_shipments, 0),
        2
    ) as on_time_delivery_rate,

    round(
        100.0 * late_deliveries
        / nullif(delivered_shipments, 0),
        2
    ) as late_delivery_rate

from monthly_metrics