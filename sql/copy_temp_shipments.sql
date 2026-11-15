COPY tmp_shipments (
    shipment_id,
    order_id,
    shipped_at,
    estimated_delivery_date,
    delivered_at
)
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER '|'
);