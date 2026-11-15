COPY tmp_reviews (
    review_id,
    order_id,
    rating,
    created_at
)
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER '|'
);