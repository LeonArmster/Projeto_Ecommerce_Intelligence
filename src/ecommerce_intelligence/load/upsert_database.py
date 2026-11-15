
# =====================================================
# Carga incremental RAW - UPSERT
# =====================================================
# Bibliotecas
import logging
from pathlib import Path

from ecommerce_intelligence.database.database_connection import (
    execute_sql,
    read_query,
)


LOGGER = logging.getLogger(__name__)


def upsert_table(
    connection,
    table_name: str,
    file_path: Path,
) -> int:
    """
    Executa a carga incremental de uma tabela RAW.

    Parameters
    ----------
    connection:
        Conexão ativa com o PostgreSQL.

    table_name:
        Nome da tabela que será carregada.

    file_path:
        Caminho do arquivo CSV.

    Returns
    -------
    int
        Quantidade de registros inseridos ou atualizados.
    """

    # =================================================
    # 1. Validar arquivo de origem
    # =================================================
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}"
        )

    LOGGER.info(
        "Iniciando carga incremental de raw.%s.",
        table_name,
    )

    # =================================================
    # 2. Executar carga em transação
    # =================================================
    with connection.transaction():

        # Criar tabela temporária
        execute_sql(
            connection,
            f"create_temp_{table_name}.sql",
        )

        # Carregar CSV na tabela temporária
        copy_query = read_query(
            f"copy_temp_{table_name}.sql"
        )

        with connection.cursor() as cursor:

            with cursor.copy(copy_query) as copy:

                with path.open("rb") as file:

                    while chunk := file.read(1024 * 1024):
                        copy.write(chunk)

        # Inserir ou atualizar registros
        affected_rows = execute_sql(
            connection,
            f"upsert_{table_name}.sql",
        )

    # =================================================
    # 3. Registrar resultado
    # =================================================
    LOGGER.info(
        "Carga de raw.%s concluída. Linhas afetadas: %s",
        table_name,
        affected_rows,
    )

    return affected_rows
