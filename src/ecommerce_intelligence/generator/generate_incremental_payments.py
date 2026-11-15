
# =====================================================
# Gerador incremental de dados = Pagamentos
# =====================================================
# Bibliotecas
import logging
import os

import pandas as pd

from ecommerce_intelligence.config.config import raw_dir

from ecommerce_intelligence.generator.payments import (
    generate_payments,
    calculate_scheduled_paid_at,
)


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Gera novos pagamentos e atualiza pagamentos pendentes."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # =================================================
    # 1. Carregar dados e definir data de referência
    # =================================================
    orders_path = raw_dir / "orders.parquet"
    items_path = raw_dir / "order_items.parquet"
    payments_path = raw_dir / "payments.parquet"

    orders = pd.read_parquet(orders_path)
    items = pd.read_parquet(items_path)
    payments = pd.read_parquet(payments_path)

    reference_date = (
        pd.Timestamp.today().normalize()
        - pd.Timedelta(days=1)
    )

    # =================================================
    # 2. Recuperar datas programadas de pagamento
    # =================================================
    if "scheduled_paid_at" not in payments.columns:

        payments["scheduled_paid_at"] = payments["paid_at"]

        pending_mask = payments["paid_at"].isna()

        if pending_mask.any():
            payments.loc[
                pending_mask, "scheduled_paid_at"
            ] = calculate_scheduled_paid_at(
                payments.loc[pending_mask],
                orders,
            )

    # =================================================
    # 3. Atualizar pagamentos pendentes
    # =================================================
    pending_mask = (
        payments["paid_at"].isna()
        & (
            pd.to_datetime(payments["scheduled_paid_at"])
            .dt.normalize()
            <= reference_date
        )
    )

    payments.loc[
        pending_mask, "paid_at"
    ] = payments.loc[
        pending_mask, "scheduled_paid_at"
    ]

    updated_pending = int(pending_mask.sum())

    # =================================================
    # 4. Identificar pedidos sem pagamento
    # =================================================
    new_orders = orders[
        ~orders["order_id"].isin(payments["order_id"])
    ].copy()

    new_payments = pd.DataFrame()

    # =================================================
    # 5. Gerar novos pagamentos
    # =================================================
    if not new_orders.empty:

        new_items = items[
            items["order_id"].isin(new_orders["order_id"])
        ].copy()

        new_payments = generate_payments(
            orders=new_orders,
            order_items=new_items,
        )

        # Continua a numeração após o último pagamento.
        next_payment_id = (
            int(payments["payment_id"].max()) + 1
            if not payments.empty
            else 1
        )

        new_payments["payment_id"] = range(
            next_payment_id,
            next_payment_id + len(new_payments),
        )

        # Preserva a data programada para atualização futura.
        new_payments["scheduled_paid_at"] = (
            new_payments["paid_at"]
        )

        # Pagamentos futuros permanecem pendentes.
        future_mask = (
            pd.to_datetime(new_payments["paid_at"])
            .dt.normalize()
            > reference_date
        )

        new_payments.loc[
            future_mask, "paid_at"
        ] = pd.NaT

    # =================================================
    # 6. Consolidar histórico e validar IDs
    # =================================================
    updated_payments = pd.concat(
        [payments, new_payments],
        ignore_index=True,
    )

    if updated_payments["payment_id"].duplicated().any():
        raise ValueError(
            "payment_id duplicado."
        )

    # =================================================
    # 7. Salvar Parquet com substituição segura
    # =================================================
    temp_path = payments_path.with_suffix(".tmp.parquet")

    # Evita substituir o histórico antes de concluir a gravação.
    try:
        updated_payments.to_parquet(
            temp_path,
            index=False,
        )

        os.replace(temp_path, payments_path)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    # =================================================
    # 8. Registrar resultados
    # =================================================
    LOGGER.info(
        "Novos pagamentos: %s",
        f"{len(new_payments):,}",
    )

    LOGGER.info(
        "Pagamentos pendentes atualizados: %s",
        f"{updated_pending:,}",
    )

    LOGGER.info(
        "Pagamentos ainda pendentes: %s",
        f"{updated_payments['paid_at'].isna().sum():,}",
    )

    LOGGER.info(
        "Total de pagamentos: %s",
        f"{len(updated_payments):,}",
    )


if __name__ == "__main__":
    main()
