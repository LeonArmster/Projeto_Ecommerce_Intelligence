# =====================================================
# Gerador de dados = Entregas
# =====================================================
# Bibliotecas
import numpy as np
import pandas as pd


def generate_shipments(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Gera informações logísticas dos pedidos."""

    rng = np.random.default_rng(seed)

    shipments = orders.merge(
        customers[["customer_id", "state"]],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    # Pedidos cancelados não são enviados
    shipments = shipments[
        shipments["order_status"] != "cancelled"
    ].copy()

    # Prazo base de acordo com modalidade
    base_delivery_days = shipments[
        "shipping_type"
    ].map(
        {
            "express": 2,
            "standard": 5,
            "economy": 8,
        }
    ).to_numpy()

    # Algumas regiões têm maior complexidade logística
    regional_extra_days = (
        shipments["state"]
        .map(
            {
                "SP": 0,
                "RJ": 1,
                "MG": 1,
                "PR": 1,
                "SC": 1,
                "RS": 2,
                "GO": 2,
                "DF": 1,
                "BA": 3,
                "PE": 3,
            }
        )
        .fillna(2)
        .to_numpy()
    )

    # Data de envio: 1 a 3 dias após o pedido
    handling_days = rng.choice(
        [1, 2, 3],
        size=len(shipments),
        p=[0.55, 0.35, 0.10],
    )

    shipments["shipped_at"] = (
        pd.to_datetime(shipments["order_date"])
        + pd.to_timedelta(handling_days, unit="D")
    )

    promised_days = (
        base_delivery_days
        + regional_extra_days
    )

    shipments["estimated_delivery_date"] = (
        shipments["shipped_at"]
        + pd.to_timedelta(promised_days, unit="D")
    )

    # -----------------------------------------
    # Probabilidade de atraso
    # -----------------------------------------

    delay_probability = np.full(
        len(shipments),
        0.05,
    )

    delay_probability += np.where(
        shipments["shipping_type"] == "economy",
        0.08,
        0,
    )

    delay_probability += np.where(
        shipments["state"].isin(["BA", "PE"]),
        0.06,
        0,
    )

    order_month = pd.to_datetime(
        shipments["order_date"]
    ).dt.month

    delay_probability += np.where(
        order_month.isin([11, 12]),
        0.10,
        0,
    )

    delay_probability = np.clip(
        delay_probability,
        0,
        0.60,
    )

    delayed = (
        rng.random(len(shipments))
        < delay_probability
    )

    # Pedidos no prazo podem chegar um pouco antes
    normal_variation = rng.choice(
        [-2, -1, 0],
        size=len(shipments),
        p=[0.15, 0.25, 0.60],
    )

    # Atrasados chegam 1 a 8 dias depois
    delay_days = rng.integers(
        1,
        9,
        size=len(shipments),
    )

    delivery_variation = np.where(
        delayed,
        delay_days,
        normal_variation,
    )

    shipments["delivered_at"] = (
        shipments["estimated_delivery_date"]
        + pd.to_timedelta(
            delivery_variation,
            unit="D",
        )
    )

    shipments["shipment_id"] = np.arange(
        1,
        len(shipments) + 1,
    )

    return shipments[
        [
            "shipment_id",
            "order_id",
            "shipped_at",
            "estimated_delivery_date",
            "delivered_at",
        ]
    ]