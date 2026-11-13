
# =====================================================
# Incremental RAW - UPSERT
# =====================================================

import logging
from pathlib import Path
from ecommerce_intelligence.database.database_connection import execute_sql, read_query


LOGGER = logging.getLogger(__name__)


def upsert_orders(
    connection,
    file_path: str = "/data/processed/orders.csv",
) -> int:
    """
    Realiza a ingestão incremental de pedidos.

    Etapas:
        1. Cria tabela temporária.
        2. Carrega CSV via COPY.
        3. Valida duplicidades.
        4. Executa UPSERT.
        5. Confirma a transação.

    Retorna o total de registros inseridos
    ou atualizados.
    """

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}"
        )

    LOGGER.info(
        "Iniciando UPSERT de raw.orders."
    )

    # A conexão deve estar em autocommit=False
    # e sem transação previamente aberta.
    with connection.transaction():

        # 1. Criação da tabela temporária
        execute_sql(
            connection,
            "create_temp_orders.sql",
        )

        # 2. Carregamento do CSV
        copy_query = read_query(
            "copy_temp_orders.sql"
        )

        with connection.cursor() as cursor:

            with cursor.copy(copy_query) as copy:

                with path.open("rb") as file:

                    while chunk := file.read(1024 * 1024):
                        copy.write(chunk)

        # 3. Validação de duplicidades
        duplicate = execute_sql(
            connection,
            "check_duplicate_orders.sql",
            fetch_one=True,
        )

        if duplicate is not None:
            raise ValueError(
                "Arquivo contém order_id duplicado: "
                f"{duplicate[0]}"
            )

        # 4. Inserção e atualização
        affected_rows = execute_sql(
            connection,
            "upsert_orders.sql",
        )

    LOGGER.info(
        "UPSERT concluído. "
        "Registros inseridos/atualizados: %s",
        affected_rows,
    )

    return affected_rows
