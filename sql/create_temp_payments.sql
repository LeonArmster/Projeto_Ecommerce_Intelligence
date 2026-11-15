CREATE TEMP TABLE tmp_payments
(LIKE raw.payments)
ON COMMIT DROP;