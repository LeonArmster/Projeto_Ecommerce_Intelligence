# =====================================================
# Gerador de dados = Ordens
# =====================================================
# Bibliotecas
import numpy as np
import pandas as pd


def generate_orders(
    customers: pd.DataFrame,
    number_orders: int,
    seed: int = 42,
) -> pd.DataFrame:

    rng = np.random.default_rng(seed)

    customer_ids = customers["customer_id"].to_numpy()

    # -------------------------------------------------
    # Perfil latente de frequência dos clientes
    # -------------------------------------------------
    customer_profiles = rng.choice(
        ["low", "regular", "high"],
        size=len(customer_ids),
        p=[0.50, 0.40, 0.10],
    )

    customer_weights = np.where(
        customer_profiles == "low",
        0.5,
        np.where(
            customer_profiles == "regular",
            1.0,
            3.0,
        ),
    )

    customer_probabilities = (
        customer_weights / customer_weights.sum()
    )

    # -------------------------------------------------
    # Cliente responsável pelo pedido
    # -------------------------------------------------
    selected_customers = rng.choice(
        customer_ids,
        size=number_orders,
        p=customer_probabilities,
    )

    # -------------------------------------------------
    # Datas
    # -------------------------------------------------
    date_range = pd.date_range(
        start="2024-01-01",
        end="2026-10-24",
        freq="D",
    )

    month_weights = {
        1: 0.80,
        2: 0.75,
        3: 0.85,
        4: 0.90,
        5: 0.95,
        6: 0.95,
        7: 1.00,
        8: 1.00,
        9: 1.05,
        10: 1.10,
        11: 1.60,
        12: 1.40,
    }

    date_weights = np.array(
        [
            month_weights[date.month]
            for date in date_range
        ],
        dtype=float,
    )

    date_probabilities = (
        date_weights / date_weights.sum()
    )

    order_dates = rng.choice(
        date_range,
        size=number_orders,
        p=date_probabilities,
    )

    # -------------------------------------------------
    # Frete
    # -------------------------------------------------
    shipping_types = rng.choice(
        ["standard", "express", "economy"],
        size=number_orders,
        p=[0.60, 0.20, 0.20],
    )

    # -------------------------------------------------
    # Status
    # -------------------------------------------------
    order_status = rng.choice(
        [
            "completed",
            "cancelled",
            "processing",
        ],
        size=number_orders,
        p=[0.94, 0.04, 0.02],
    )

    # -------------------------------------------------
    # DataFrame
    # -------------------------------------------------
    orders = pd.DataFrame(
        {
            "order_id": np.arange(
                1,
                number_orders + 1,
            ),
            "customer_id": selected_customers,
            "order_date": order_dates,
            "order_status": order_status,
            "shipping_type": shipping_types,
        }
    )

    orders = orders.sort_values(
        "order_date"
    ).reset_index(drop=True)

    return orders