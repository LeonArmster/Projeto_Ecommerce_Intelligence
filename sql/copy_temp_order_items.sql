COPY tmp_order_items (
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_pct
)
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER '|'
);