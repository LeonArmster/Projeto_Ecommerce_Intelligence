# =====================================================
# Gerador incremental de dados = Itens dos pedidos
# =====================================================
# Bibliotecas
import logging
import os

import pandas as pd

from ecommerce_intelligence.config.config import raw_dir
from ecommerce_intelligence.generator.order_items import (
    generate_order_items,
)


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Gera itens para pedidos que ainda não possuem registros de itens."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # =================================================
    # 1. Carregar arquivos Parquet
    # =================================================
    orders_path = raw_dir / "orders.parquet"
    products_path = raw_dir / "products.parquet"
    items_path = raw_dir / "order_items.parquet"

    orders = pd.read_parquet(orders_path)
    products = pd.read_parquet(products_path)
    items = pd.read_parquet(items_path)

    # =================================================
    # 2. Identificar pedidos sem itens
    # =================================================
    existing_order_ids = items["order_id"].unique()

    new_orders = orders[
        ~orders["order_id"].isin(existing_order_ids)
    ].copy()

    if new_orders.empty:
        LOGGER.info(
            "Nenhum pedido novo para gerar itens."
        )
        return

    LOGGER.info(
        "Pedidos sem itens: %s",
        f"{len(new_orders):,}",
    )

    # =================================================
    # 3. Gerar itens e continuar sequência de IDs
    # =================================================
    new_items = generate_order_items(
        orders=new_orders,
        products=products,
    )

    # A função original reinicia os IDs; continuamos após o último existente.
    next_item_id = int(items["order_item_id"].max()) + 1

    new_items["order_item_id"] = range(
        next_item_id,
        next_item_id + len(new_items),
    )

    # =================================================
    # 4. Consolidar histórico e validar IDs
    # =================================================
    updated_items = pd.concat(
        [items, new_items],
        ignore_index=True,
    )

    # Impede duplicações antes de persistir os registros.
    if updated_items["order_item_id"].duplicated().any():
        raise ValueError(
            "Foram encontrados order_item_id duplicados."
        )

    # =================================================
    # 5. Salvar Parquet com substituição segura
    # =================================================
    temp_path = items_path.with_suffix(".tmp.parquet")

    # O arquivo temporário evita substituir o histórico antes da gravação.
    try:
        updated_items.to_parquet(
            temp_path,
            index=False,
        )

        os.replace(temp_path, items_path)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    # =================================================
    # 6. Registrar resultados
    # =================================================
    LOGGER.info(
        "Novos itens gerados: %s",
        f"{len(new_items):,}",
    )

    LOGGER.info(
        "Total de itens: %s",
        f"{len(updated_items):,}",
    )

    LOGGER.info(
        "Geração incremental de itens concluída."
    )


if __name__ == "__main__":
    main()
