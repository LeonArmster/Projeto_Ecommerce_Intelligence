INSERT INTO raw.order_items (
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_pct
)
SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_pct
FROM tmp_order_items
ON CONFLICT (order_item_id) DO NOTHING;