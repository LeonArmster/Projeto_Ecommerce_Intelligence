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





def generate_daily_reviews(
    shipments: pd.DataFrame,
    reference_date,
) -> pd.DataFrame:
    """
    Gera avaliações determinísticas para entregas concluídas.

    Cada order_id possui uma decisão fixa:
    - Se receberá avaliação.
    - Qual será sua nota.
    - Quantos dias após a entrega será avaliado.
    """

    columns = [
        "order_id",
        "rating",
        "created_at",
    ]

    if shipments.empty:
        return pd.DataFrame(columns=columns)

    reference_date = pd.Timestamp(reference_date).normalize()

    shipments = shipments.copy()

    # Somente entregas efetivamente concluídas.
    shipments = shipments[
        shipments["delivered_at"].notna()
    ].copy()

    if shipments.empty:
        return pd.DataFrame(columns=columns)

    reviews = []

    for row in shipments.itertuples(index=False):

        # Semente fixa por pedido.
        rng = np.random.default_rng(int(row.order_id))

        # Probabilidade de avaliação: 60%.
        if rng.random() >= 0.60:
            continue

        delivered_at = pd.Timestamp(row.delivered_at)

        # Avaliação entre 0 e 7 dias após a entrega.
        delay_days = int(rng.integers(0, 8))

        created_at = (
            delivered_at + pd.Timedelta(days=delay_days)
        )

        # Não criar avaliações futuras.
        if created_at.normalize() > reference_date:
            continue

        estimated_date = pd.Timestamp(
            row.estimated_delivery_date
        )

        # Entregas atrasadas tendem a receber notas menores.
        delayed = delivered_at > estimated_date

        if delayed:
            rating = int(
                rng.choice(
                    [1, 2, 3, 4, 5],
                    p=[0.20, 0.25, 0.30, 0.15, 0.10],
                )
            )
        else:
            rating = int(
                rng.choice(
                    [1, 2, 3, 4, 5],
                    p=[0.05, 0.05, 0.15, 0.30, 0.45],
                )
            )

        reviews.append(
            {
                "order_id": row.order_id,
                "rating": rating,
                "created_at": created_at,
            }
        )

    return pd.DataFrame(reviews, columns=columns)
