
# =====================================================
# Orquestrador de carga incremental RAW
# =====================================================
# Bibliotecas
import logging
from time import perf_counter

from ecommerce_intelligence.config.config import processed_dir
from ecommerce_intelligence.database.database_connection import db_connection
from ecommerce_intelligence.load.upsert_database import upsert_table


LOGGER = logging.getLogger(__name__)


TABLES = [
    "orders",
    "order_items",
    "payments",
    "shipments",
    "reviews",
]


def main() -> None:
    """Executa a carga incremental das tabelas RAW."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # =================================================
    # 1. Iniciar processamento
    # =================================================
    start_pipeline = perf_counter()

    LOGGER.info("Iniciando carga incremental RAW.")

    # =================================================
    # 2. Conectar ao PostgreSQL
    # =================================================
    connection = db_connection()

    try:

        # =================================================
        # 3. Executar UPSERT das tabelas
        # =================================================
        for table in TABLES:

            start_table = perf_counter()

            affected_rows = upsert_table(
                connection=connection,
                table_name=table,
                file_path=processed_dir / f"{table}.csv",
            )

            LOGGER.info(
                "Tabela raw.%s: %s linhas afetadas | %.2f segundos",
                table,
                affected_rows,
                perf_counter() - start_table,
            )

    except Exception:

        LOGGER.exception(
            "Erro durante a carga incremental RAW."
        )
        raise

    finally:

        connection.close()

    # =================================================
    # 4. Finalizar processamento
    # =================================================
    LOGGER.info(
        "Carga incremental RAW concluída em %.2f segundos.",
        perf_counter() - start_pipeline,
    )


if __name__ == "__main__":
    main()
