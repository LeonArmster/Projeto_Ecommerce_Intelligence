
COPY tmp_orders (
    order_id,
    customer_id,
    order_date,
    order_status,
    shipping_type
)
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER '|',
    NULL ''
);
