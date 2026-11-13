
SELECT
    order_id,
    COUNT(*) AS total
FROM tmp_orders
GROUP BY order_id
HAVING COUNT(*) > 1
LIMIT 1;
