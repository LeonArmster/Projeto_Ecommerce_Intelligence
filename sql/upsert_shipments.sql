INSERT INTO raw.shipments (
    shipment_id,
    order_id,
    shipped_at,
    estimated_delivery_date,
    delivered_at
)
SELECT
    shipment_id,
    order_id,
    shipped_at,
    estimated_delivery_date,
    delivered_at
FROM tmp_shipments
ON CONFLICT (shipment_id)
DO UPDATE SET
    order_id = EXCLUDED.order_id,
    shipped_at = EXCLUDED.shipped_at,
    estimated_delivery_date = EXCLUDED.estimated_delivery_date,
    delivered_at = EXCLUDED.delivered_at
WHERE (
    raw.shipments.order_id,
    raw.shipments.shipped_at,
    raw.shipments.estimated_delivery_date,
    raw.shipments.delivered_at
) IS DISTINCT FROM (
    EXCLUDED.order_id,
    EXCLUDED.shipped_at,
    EXCLUDED.estimated_delivery_date,
    EXCLUDED.delivered_at
);