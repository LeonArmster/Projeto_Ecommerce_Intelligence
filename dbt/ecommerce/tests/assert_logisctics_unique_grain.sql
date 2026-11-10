
select
    shipment_month,
    shipping_type,
    count(*) as total_rows

from {{ ref('mart_logistics_performance') }}

group by
    shipment_month,
    shipping_type

having count(*) > 1
