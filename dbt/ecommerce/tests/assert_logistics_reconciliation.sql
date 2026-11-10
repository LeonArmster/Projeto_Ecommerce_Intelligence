
{% set reference_date = var('logistics_reference_date', '2026-11-09') %}

with source_metrics as (

    select
        date_trunc('month', s.shipped_at)::date
            as shipment_month,

        o.shipping_type,

        count(*) as total_shipments,

        count(*) filter (
            where s.delivered_at is not null
        ) as delivered_shipments,

        count(*) filter (
            where s.delivered_at is null
        ) as pending_shipments,

        count(*) filter (
            where s.is_delayed = true
        ) as late_deliveries,

        count(*) filter (
            where s.is_delayed = false
        ) as on_time_deliveries,

        count(*) filter (
            where s.delivered_at is null
              and s.estimated_delivery_at
                  < ('{{ reference_date }}'::date + interval '1 day')
        ) as overdue_pending_shipments

    from {{ ref('int_shipments_enriched') }} s

    inner join {{ ref('stg_orders') }} o
        on s.order_id = o.order_id

    where o.order_status <> 'cancelled'
      and s.shipped_at is not null
      and s.shipped_at < ('{{ reference_date }}'::date + interval '1 day')

    group by 1, 2

),

mart_metrics as (

    select
        shipment_month,
        shipping_type,
        total_shipments,
        delivered_shipments,
        pending_shipments,
        late_deliveries,
        on_time_deliveries,
        overdue_pending_shipments

    from {{ ref('mart_logistics_performance') }}

),

reconciliation as (

    select
        coalesce(s.shipment_month, m.shipment_month)
            as shipment_month,

        coalesce(s.shipping_type, m.shipping_type)
            as shipping_type,

        s.shipment_month is null as missing_in_source,
        m.shipment_month is null as missing_in_mart,

        s.total_shipments as source_total,
        m.total_shipments as mart_total,

        s.delivered_shipments as source_delivered,
        m.delivered_shipments as mart_delivered,

        s.pending_shipments as source_pending,
        m.pending_shipments as mart_pending,

        s.late_deliveries as source_late,
        m.late_deliveries as mart_late,

        s.on_time_deliveries as source_on_time,
        m.on_time_deliveries as mart_on_time,

        s.overdue_pending_shipments as source_overdue,
        m.overdue_pending_shipments as mart_overdue

    from source_metrics s

    full outer join mart_metrics m
        on s.shipment_month = m.shipment_month
       and s.shipping_type = m.shipping_type

)

select *
from reconciliation

where
    missing_in_source
    or missing_in_mart

    or source_total is distinct from mart_total
    or source_delivered is distinct from mart_delivered
    or source_pending is distinct from mart_pending
    or source_late is distinct from mart_late
    or source_on_time is distinct from mart_on_time
    or source_overdue is distinct from mart_overdue
