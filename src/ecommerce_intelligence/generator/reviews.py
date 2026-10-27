# =====================================================
# Gerador de dados = Reviews de experiência do cliente
# =====================================================
# Bibliotecas
import numpy as np
import pandas as pd


def generate_reviews(
    shipments: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Gera avaliações associadas às entregas."""

    rng = np.random.default_rng(seed)

    reviews = shipments.copy()

    # Nem todo cliente avalia
    review_mask = (
        rng.random(len(reviews)) < 0.60
    )

    reviews = reviews[
        review_mask
    ].copy()

    delayed = (
        reviews["delivered_at"]
        > reviews["estimated_delivery_date"]
    )

    ratings = np.empty(
        len(reviews),
        dtype=np.int8,
    )

    on_time_count = (~delayed).sum()
    delayed_count = delayed.sum()

    ratings[~delayed] = rng.choice(
        [1, 2, 3, 4, 5],
        size=on_time_count,
        p=[0.02, 0.03, 0.10, 0.30, 0.55],
    )

    ratings[delayed] = rng.choice(
        [1, 2, 3, 4, 5],
        size=delayed_count,
        p=[0.30, 0.30, 0.20, 0.15, 0.05],
    )

    reviews["rating"] = ratings

    reviews["review_id"] = np.arange(
        1,
        len(reviews) + 1,
    )

    reviews["created_at"] = (
        reviews["delivered_at"]
        + pd.to_timedelta(
            rng.integers(
                0,
                8,
                size=len(reviews),
            ),
            unit="D",
        )
    )

    return reviews[
        [
            "review_id",
            "order_id",
            "rating",
            "created_at",
        ]
    ]