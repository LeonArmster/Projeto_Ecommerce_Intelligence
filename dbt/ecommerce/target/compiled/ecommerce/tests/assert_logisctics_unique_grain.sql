select
    shipment_month,
    shipping_type,
    count(*) as total_rows

from "ecommerce"."analytics_marts"."mart_logistics_performance"

group by
    shipment_month,
    shipping_type

having count(*) > 1