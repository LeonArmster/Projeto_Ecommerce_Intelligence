# =====================================================
# Gerador de dados = Pagamentos
# =====================================================
# Bibliotecas
import numpy as np
import pandas as pd


def generate_payments(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Gera os pagamentos dos pedidos."""

    rng = np.random.default_rng(seed)

    # Valor líquido de cada item
    items = order_items.copy()

    items["net_amount"] = (
        items["quantity"]
        * items["unit_price"]
        * (1 - items["discount_pct"])
    )

    # Valor total de cada pedido
    order_totals = (
        items
        .groupby("order_id", as_index=False)["net_amount"]
        .sum()
        .rename(columns={"net_amount": "payment_amount"})
    )

    # Junta informações necessárias do pedido
    payments = order_totals.merge(
        orders[["order_id", "order_date", "order_status"]],
        on="order_id",
        how="left",
        validate="one_to_one",
    )

    # Meio de pagamento
    payments["payment_method"] = rng.choice(
        ["credit_card", "pix", "debit_card", "boleto"],
        size=len(payments),
        p=[0.50, 0.30, 0.10, 0.10],
    )

    # Parcelas
    installments = np.ones(
        len(payments),
        dtype=np.int8,
    )

    credit_mask = (
        payments["payment_method"] == "credit_card"
    )

    installments[credit_mask] = rng.choice(
        [1, 2, 3, 6, 10, 12],
        size=credit_mask.sum(),
        p=[0.25, 0.15, 0.20, 0.20, 0.12, 0.08],
    )

    payments["installments"] = installments

    # Status financeiro coerente com o pedido
    payments["payment_status"] = np.where(
        payments["order_status"] == "cancelled",
        "refunded",
        "approved",
    )

    # Data do pagamento
    payment_delay_hours = rng.integers(
        0,
        25,
        size=len(payments),
    )

    payments["paid_at"] = (
        pd.to_datetime(payments["order_date"])
        + pd.to_timedelta(payment_delay_hours, unit="h")
    )

    payments["payment_id"] = np.arange(
        1,
        len(payments) + 1,
    )

    payments["payment_amount"] = (
        payments["payment_amount"].round(2)
    )

    return payments[
        [
            "payment_id",
            "order_id",
            "payment_method",
            "payment_amount",
            "installments",
            "payment_status",
            "paid_at",
        ]
    ]