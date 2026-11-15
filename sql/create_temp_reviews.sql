CREATE TEMP TABLE tmp_reviews
(LIKE raw.reviews)
ON COMMIT DROP;