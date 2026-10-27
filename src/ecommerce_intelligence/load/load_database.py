# ============================================
# Orquestrador de Carga
# ============================================
# Bibliotecas
import logging
from ecommerce_intelligence.database.database_connection import read_query


logger = logging.getLogger(__name__)


def truncate_table(
    connection,
    table_name: str,
) -> None:

    query = read_query("truncate_table.sql").format(table_name=table_name)

    logger.info("Executando TRUNCATE raw.%s",table_name)

    with connection.cursor() as cursor:
        cursor.execute(query)




def copy_table(
    connection,
    table_name: str,
    file_path: str,
) -> None:

    query = read_query("copy_data.sql").format(table_name=table_name, file_path=file_path)

    logger.info("Executando COPY %s -> raw.%s", file_path, table_name)

    with connection.cursor() as cursor:
        cursor.execute(query)