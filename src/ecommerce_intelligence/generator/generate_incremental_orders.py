# =====================================================
# Gerador incremental de dados = Pedidos
# =====================================================
# Bibliotecas
# =====================================================
# Geração incremental de pedidos
# =====================================================

import logging
import os

import pandas as pd

from ecommerce_intelligence.config.config import raw_dir

from ecommerce_intelligence.generator.generation_dates import (
    get_reference_date,
    get_missing_dates,
)

from ecommerce_intelligence.generator.orders import (
    generate_daily_orders,
)


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Gera pedidos para as datas ainda não processadas, preservando o histórico."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # =================================================
    # 1. Localizar e validar os arquivos Parquet
    # =================================================
    customers_path = raw_dir / "customers.parquet"
    orders_path = raw_dir / "orders.parquet"

    if not customers_path.exists():
        raise FileNotFoundError(customers_path)

    if not orders_path.exists():
        raise FileNotFoundError(
            "Base inicial de pedidos não encontrada. "
            "Execute a geração inicial primeiro."
        )

    # =================================================
    # 2. Carregar dados e identificar datas pendentes
    # =================================================
    customers = pd.read_parquet(customers_path)
    orders = pd.read_parquet(orders_path)

    reference_date = get_reference_date()

    last_generated_date = (
        pd.to_datetime(orders["order_date"])
        .max()
        .date()
    )

    missing_dates = get_missing_dates(
        last_generated_date=last_generated_date,
        reference_date=reference_date,
    )

    LOGGER.info(
        "Última data existente: %s",
        last_generated_date,
    )

    LOGGER.info(
        "Data de referência: %s",
        reference_date,
    )

    if not missing_dates:
        LOGGER.info(
            "Nenhuma nova data para processar."
        )
        return

    # =================================================
    # 3. Gerar pedidos com IDs sequenciais
    # =================================================
    next_order_id = int(orders["order_id"].max()) + 1

    new_batches = []

    for generation_date in missing_dates:

        daily_orders = generate_daily_orders(
            customers=customers,
            generation_date=generation_date,
            start_order_id=next_order_id,
            number_orders=1_000,
        )

        new_batches.append(daily_orders)

        next_order_id += len(daily_orders)

    new_orders = pd.concat(
        new_batches,
        ignore_index=True,
    )


    # =================================================
    # Padronizar resolução temporal
    # =================================================

    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    ).astype("datetime64[ns]")

    new_orders["order_date"] = pd.to_datetime(
        new_orders["order_date"]
    ).astype("datetime64[ns]")

    LOGGER.info(
        "Dtype histórico: %s | Dtype incremental: %s",
        orders["order_date"].dtype,
        new_orders["order_date"].dtype,
    )


    # =================================================
    # 4. Consolidar histórico e validar IDs
    # =================================================
    LOGGER.info(
        "Dtype histórico: %s",
        orders["order_date"].dtype,
    )

    LOGGER.info(
        "Dtype incremental: %s",
        new_orders["order_date"].dtype,
    )

    LOGGER.info(
        "Shape histórico: %s",
        orders.shape,
    )

    LOGGER.info(
        "Shape incremental: %s",
        new_orders.shape,
    )


    updated_orders = pd.concat(
        [orders, new_orders],
        ignore_index=True,
    )

    # Impede duplicações antes de persistir os registros.
    if updated_orders["order_id"].duplicated().any():
        raise ValueError(
            "Foram encontrados order_id duplicados."
        )

    # =================================================
    # 5. Salvar Parquet com substituição segura
    # =================================================
    temp_path = orders_path.with_suffix(".tmp.parquet")

    # O arquivo temporário evita substituir o histórico antes da gravação.
    try:
        updated_orders.to_parquet(
            temp_path,
            index=False,
        )

        os.replace(temp_path, orders_path)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    # =================================================
    # 6. Registrar resultados
    # =================================================
    LOGGER.info(
        "Novos pedidos: %s",
        f"{len(new_orders):,}",
    )

    LOGGER.info(
        "Total de pedidos: %s",
        f"{len(updated_orders):,}",
    )

    LOGGER.info(
        "Geração incremental concluída."
    )


if __name__ == "__main__":
    main()
