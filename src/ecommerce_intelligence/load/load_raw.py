# ============================================
# Orquestrador de Carga
# ============================================
# Bibliotecas
import logging
from time import perf_counter
from ecommerce_intelligence.load.load_database import truncate_table, copy_table
from ecommerce_intelligence.database.database_connection import db_connection


tables = [
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "reviews",
]


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
    )

    logging.info("Iniciando carga das tabelas RAW.")

    start_pipeline = perf_counter()

    conexao = db_connection()

    try:

        for table in tables:

            start_table = perf_counter()

            logging.info(
                "Iniciando carga da tabela raw.%s.",
                table,
            )

            truncate_table(
                conexao,
                table_name=table,
            )

            copy_table(
                conexao,
                table_name=table,
                file_path=f"/data/processed/{table}.csv",
            )

            # Confirma TRUNCATE + COPY da tabela
            conexao.commit()

            elapsed = perf_counter() - start_table

            logging.info(
                "Tabela raw.%s carregada em %.2f segundos.",
                table,
                elapsed,
            )

    except Exception:

        conexao.rollback()

        logging.exception(
            "Erro durante a carga das tabelas RAW."
        )

        raise

    finally:

        conexao.close()

        logging.info(
            "Conexão com PostgreSQL encerrada."
        )

    total_elapsed = (
        perf_counter() - start_pipeline
    )

    logging.info(
        "Carga RAW concluída em %.2f segundos.",
        total_elapsed,
    )


if __name__ == "__main__":
    main()
