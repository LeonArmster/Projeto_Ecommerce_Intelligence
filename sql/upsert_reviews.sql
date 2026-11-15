INSERT INTO raw.reviews (
    review_id,
    order_id,
    rating,
    created_at
)
SELECT
    review_id,
    order_id,
    rating,
    created_at
FROM tmp_reviews
ON CONFLICT (review_id) DO NOTHING;