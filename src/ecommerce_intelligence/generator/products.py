# =====================================================
# Gerador de dados = Produtos
# =====================================================
# Bibliotecas
import numpy as np
import pandas as pd


PRODUCT_CONFIG = {
    "electronics": {
        "brands": ["Samsung", "LG", "Sony", "Dell", "Lenovo"],
        "price_range": (200.0, 8000.0),
        "weight_range": (0.1, 15.0),
    },
    "home": {
        "brands": ["Tramontina", "Electrolux", "Brastemp", "Philco"],
        "price_range": (30.0, 5000.0),
        "weight_range": (0.2, 40.0),
    },
    "fashion": {
        "brands": ["Nike", "Adidas", "Puma", "Hering", "Renner"],
        "price_range": (20.0, 800.0),
        "weight_range": (0.05, 3.0),
    },
    "beauty": {
        "brands": ["Natura", "O Boticário", "L'Oréal", "Nivea"],
        "price_range": (15.0, 600.0),
        "weight_range": (0.05, 2.0),
    },
    "sports": {
        "brands": ["Nike", "Adidas", "Puma", "Wilson"],
        "price_range": (30.0, 3000.0),
        "weight_range": (0.1, 20.0),
    },
    "books": {
        "brands": ["Generic"],
        "price_range": (15.0, 250.0),
        "weight_range": (0.1, 2.0),
    },
}


def generate_products(
    number_products: int,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Gera o catálogo sintético de produtos.
    """

    rng = np.random.default_rng(seed)

    categories = list(PRODUCT_CONFIG.keys())

    category_probabilities = [
        0.20,
        0.20,
        0.20,
        0.15,
        0.15,
        0.10,
    ]

    records = []

    for product_id in range(1, number_products + 1):

        category = rng.choice(
            categories,
            p=category_probabilities,
        )

        config = PRODUCT_CONFIG[category]

        brand = rng.choice(config["brands"])

        price = rng.uniform(
            config["price_range"][0],
            config["price_range"][1],
        )

        weight = rng.uniform(
            config["weight_range"][0],
            config["weight_range"][1],
        )

        records.append(
            {
                "product_id": product_id,
                "category": category,
                "brand": brand,
                "base_price": round(price, 2),
                "weight_kg": round(weight, 3),
            }
        )

    return pd.DataFrame(records)