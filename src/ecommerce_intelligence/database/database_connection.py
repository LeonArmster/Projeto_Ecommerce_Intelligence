# ===============================================
# Conexao com o banco
# ===============================================
# Bibliotecas
import os
import psycopg
from ecommerce_intelligence.config.config import pg_host, pg_port, pg_user, pg_password, pg_dbname
from ecommerce_intelligence.config.config import sql_dir


def db_connection() -> psycopg.Connection:
    """
    Carrega a conexão do banco de dados
    """
    return psycopg.connect(
        host=pg_host,
        port=pg_port,
        dbname=pg_dbname,
        user=pg_user,
        password=pg_password
    )


def read_query(file_name:str) -> str:
    """
    Carrega uma query SQL armazenada em arquivo.
    """
    with open(sql_dir/file_name, mode='r', encoding='utf-8') as file:
        query = file.read()

    return query