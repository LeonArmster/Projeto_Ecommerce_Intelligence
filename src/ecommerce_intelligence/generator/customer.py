# =====================================================
# Gerador de dados = Clientes
# =====================================================
# Bibliotecas
from datetime import date
import numpy as np
import pandas as pd
from faker import Faker


fake = Faker("pt_BR")


def generate_customers(
    number_customers: int,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Gera dados sintéticos de clientes.

    Parameters
    ----------
    number_customers:
        Quantidade de clientes que serão gerados.

    seed:
        Semente utilizada para tornar a geração reproduzível.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo os clientes gerados.
    """

    Faker.seed(seed)
    rng = np.random.default_rng(seed)

    states = [
        "SP",
        "RJ",
        "MG",
        "PR",
        "RS",
        "SC",
        "BA",
        "PE",
        "GO",
        "DF",
    ]

    state_probabilities = [
        0.30,
        0.13,
        0.13,
        0.09,
        0.08,
        0.06,
        0.07,
        0.05,
        0.05,
        0.04,
    ]

    customer_ids = np.arange(1, number_customers + 1)

    birth_dates = [
        fake.date_between(
            start_date=date(1955, 1, 1),
            end_date=date(2007, 12, 31),
        )
        for _ in range(number_customers)
    ]

    created_dates = pd.to_datetime(
        rng.integers(
            pd.Timestamp("2022-01-01").value // 10**9,
            pd.Timestamp("2026-01-01").value // 10**9,
            size=number_customers,
        ),
        unit="s",
    ).normalize()

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "birth_date": birth_dates,
            "state": rng.choice(
                states,
                size=number_customers,
                p=state_probabilities,
            ),
            "created_at": created_dates,
        }
    )

    return df