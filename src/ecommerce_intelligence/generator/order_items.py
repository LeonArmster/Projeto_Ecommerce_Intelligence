# =====================================================
# Gerador de dados = Items por Ordem
# =====================================================
# Bibliotecas
import numpy as np
import pandas as pd


def generate_order_items(
    orders: pd.DataFrame,
    products: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Gera os itens associados aos pedidos.

    Cada linha representa um produto dentro de um pedido.
    """

    rng = np.random.default_rng(seed)

    # -----------------------------------------
    # Quantidade de itens diferentes por pedido
    # -----------------------------------------
    number_items_per_order = rng.choice(
        [1, 2, 3, 4, 5, 6],
        size=len(orders),
        p=[0.25, 0.25, 0.20, 0.15, 0.10, 0.05],
    )

    total_items = number_items_per_order.sum()

    # -----------------------------------------
    # Repete cada order_id conforme
    # sua quantidade de itens
    # -----------------------------------------
    order_ids = np.repeat(
        orders["order_id"].to_numpy(),
        number_items_per_order,
    )

    # -----------------------------------------
    # Produtos
    # -----------------------------------------
    product_ids = rng.choice(
        products["product_id"].to_numpy(),
        size=total_items,
    )

    # -----------------------------------------
    # Quantidade do mesmo produto
    # -----------------------------------------
    quantities = rng.choice(
        [1, 2, 3, 4],
        size=total_items,
        p=[0.78, 0.15, 0.05, 0.02],
    )

    # -----------------------------------------
    # Recupera preço base
    # -----------------------------------------
    product_price_map = (
        products
        .set_index("product_id")["base_price"]
    )

    base_prices = product_price_map.loc[
        product_ids
    ].to_numpy()

    # -----------------------------------------
    # Pequena variação de preço
    # -----------------------------------------
    price_factor = rng.normal(
        loc=1.0,
        scale=0.05,
        size=total_items,
    )

    unit_prices = np.maximum(
        base_prices * price_factor,
        1.0,
    )

    # -----------------------------------------
    # Descontos
    # -----------------------------------------
    discounts = rng.choice(
        [0.00, 0.05, 0.10, 0.15, 0.20, 0.30],
        size=total_items,
        p=[0.50, 0.15, 0.15, 0.10, 0.07, 0.03],
    )

    # -----------------------------------------
    # DataFrame
    # -----------------------------------------
    order_items = pd.DataFrame(
        {
            "order_item_id": np.arange(
                1,
                total_items + 1,
            ),
            "order_id": order_ids,
            "product_id": product_ids,
            "quantity": quantities,
            "unit_price": np.round(
                unit_prices,
                2,
            ),
            "discount_pct": discounts,
        }
    )

    return order_items