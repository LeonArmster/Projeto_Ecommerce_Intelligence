INSERT INTO raw.payments (
    payment_id,
    order_id,
    payment_method,
    payment_amount,
    installments,
    payment_status,
    paid_at
)
SELECT
    payment_id,
    order_id,
    payment_method,
    payment_amount,
    installments,
    payment_status,
    paid_at
FROM tmp_payments
ON CONFLICT (payment_id)
DO UPDATE SET
    order_id = EXCLUDED.order_id,
    payment_method = EXCLUDED.payment_method,
    payment_amount = EXCLUDED.payment_amount,
    installments = EXCLUDED.installments,
    payment_status = EXCLUDED.payment_status,
    paid_at = EXCLUDED.paid_at
WHERE (
    raw.payments.order_id,
    raw.payments.payment_method,
    raw.payments.payment_amount,
    raw.payments.installments,
    raw.payments.payment_status,
    raw.payments.paid_at
) IS DISTINCT FROM (
    EXCLUDED.order_id,
    EXCLUDED.payment_method,
    EXCLUDED.payment_amount,
    EXCLUDED.installments,
    EXCLUDED.payment_status,
    EXCLUDED.paid_at
);