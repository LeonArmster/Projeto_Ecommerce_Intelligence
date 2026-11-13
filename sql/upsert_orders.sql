
INSERT INTO raw.orders AS target (
    order_id,
    customer_id,
    order_date,
    order_status,
    shipping_type
)
SELECT
    order_id,
    customer_id,
    order_date,
    order_status,
    shipping_type
FROM tmp_orders
WHERE TRUE

ON CONFLICT (order_id)

DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    order_date = EXCLUDED.order_date,
    order_status = EXCLUDED.order_status,
    shipping_type = EXCLUDED.shipping_type

WHERE
    (
        target.customer_id,
        target.order_date,
        target.order_status,
        target.shipping_type
    )
    IS DISTINCT FROM
    (
        EXCLUDED.customer_id,
        EXCLUDED.order_date,
        EXCLUDED.order_status,
        EXCLUDED.shipping_type
    );
