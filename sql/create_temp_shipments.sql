CREATE TEMP TABLE tmp_shipments
(LIKE raw.shipments)
ON COMMIT DROP;