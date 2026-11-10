select *
from "ecommerce"."analytics_marts"."mart_logistics_performance"

where
    total_shipments
        <> delivered_shipments + pending_shipments

    or delivered_shipments
        <> late_deliveries + on_time_deliveries

    or overdue_pending_shipments > pending_shipments

    or total_shipments < 0

    or (
        on_time_delivery_rate is not null
        and (
            on_time_delivery_rate < 0
            or on_time_delivery_rate > 100
        )
    )