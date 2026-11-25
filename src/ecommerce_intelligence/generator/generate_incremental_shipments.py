
import logging
import os

import pandas as pd

from ecommerce_intelligence.config.config import raw_dir
from ecommerce_intelligence.generator.parquet_io import save_parquet

from ecommerce_intelligence.generator.shipments import (
    generate_shipments,
    apply_shipment_reference_date,
)

from ecommerce_intelligence.generator.generation_dates import (
    get_reference_date,
)


LOGGER = logging.getLogger(__name__)


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    orders_path = raw_dir / "orders.parquet"
    customers_path = raw_dir / "customers.parquet"
    shipments_path = raw_dir / "shipments.parquet"

    orders = pd.read_parquet(orders_path)
    customers = pd.read_parquet(customers_path)
    shipments = pd.read_parquet(shipments_path)

    reference_date = get_reference_date()

    # -----------------------------------------
    # 1. Identificar pedidos sem entrega
    # -----------------------------------------
    new_orders = orders[
        ~orders["order_id"].isin(shipments["order_id"])
        & (orders["order_status"] != "cancelled")
    ].copy()

    LOGGER.info(
        "Pedidos novos elegíveis para envio: %s",
        f"{len(new_orders):,}",
    )

    # -----------------------------------------
    # 2. Gerar entregas novas
    # -----------------------------------------
    if not new_orders.empty:

        new_shipments = generate_shipments(
            orders=new_orders,
            customers=customers,
        )

        next_shipment_id = (
            int(shipments["shipment_id"].max()) + 1
            if not shipments.empty
            else 1
        )

        new_shipments["shipment_id"] = range(
            next_shipment_id,
            next_shipment_id + len(new_shipments),
        )

        new_shipments = apply_shipment_reference_date(
            new_shipments,
            reference_date,
        )

    else:
        new_shipments = shipments.iloc[0:0].copy()

    # -----------------------------------------
    # 3. Atualizar entregas pendentes
    # -----------------------------------------
    if "scheduled_shipped_at" not in shipments.columns:
        shipments["scheduled_shipped_at"] = shipments["shipped_at"]

    if "scheduled_delivered_at" not in shipments.columns:
        shipments["scheduled_delivered_at"] = shipments["delivered_at"]

    pending_shipments = shipments["shipped_at"].isna()
    pending_deliveries = shipments["delivered_at"].isna()

    shipments = apply_shipment_reference_date(
        shipments,
        reference_date,
    )

    updated_shipments = int(
        (
            pending_shipments
            & shipments["shipped_at"].notna()
        ).sum()
    )

    updated_deliveries = int(
        (
            pending_deliveries
            & shipments["delivered_at"].notna()
        ).sum()
    )

    # -----------------------------------------
    # 4. Consolidar histórico
    # -----------------------------------------
    updated = pd.concat(
        [shipments, new_shipments],
        ignore_index=True,
    )

    if updated["shipment_id"].duplicated().any():
        raise ValueError(
            "shipment_id duplicado."
        )

    if updated["order_id"].duplicated().any():
        raise ValueError(
            "Pedido com mais de uma entrega."
        )

    # -----------------------------------------
    # 5. Salvar Parquet
    # -----------------------------------------
    temp_path = shipments_path.with_suffix(".tmp.parquet")

    try:
        save_parquet(
            updated,
            temp_path,
        )

        os.replace(temp_path, shipments_path)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    LOGGER.info(
        "Novas entregas: %s",
        f"{len(new_shipments):,}",
    )

    LOGGER.info(
        "Envios pendentes atualizados: %s",
        f"{updated_shipments:,}",
    )

    LOGGER.info(
        "Entregas pendentes atualizadas: %s",
        f"{updated_deliveries:,}",
    )

    LOGGER.info(
        "Entregas ainda pendentes: %s",
        f"{updated['delivered_at'].isna().sum():,}",
    )

    LOGGER.info(
        "Total de registros logísticos: %s",
        f"{len(updated):,}",
    )


if __name__ == "__main__":
    main()
