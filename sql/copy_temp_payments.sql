COPY tmp_payments (
    payment_id,
    order_id,
    payment_method,
    payment_amount,
    installments,
    payment_status,
    paid_at
)
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER '|'
);