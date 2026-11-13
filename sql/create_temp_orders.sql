
CREATE TEMP TABLE tmp_orders
(LIKE raw.orders)
ON COMMIT DROP;
