CREATE TEMP TABLE tmp_order_items
(LIKE raw.order_items)
ON COMMIT DROP;