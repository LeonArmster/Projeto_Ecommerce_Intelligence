
from ecommerce_intelligence.database.database_connection import (
    db_connection,
)


def test_upsert_idempotency():
    connection = db_connection()

    try:
        with connection.cursor() as cursor:
            # Tabela temporária exclusiva desta conexão
            cursor.execute("""
                CREATE TEMP TABLE test_orders (
                    order_id INTEGER PRIMARY KEY,
                    order_status TEXT NOT NULL
                ) ON COMMIT DROP;
            """)

            upsert_sql = """
                INSERT INTO test_orders (
                    order_id,
                    order_status
                )
                VALUES
                    (1, 'pending'),
                    (2, 'completed')
                ON CONFLICT (order_id)
                DO UPDATE SET
                    order_status = EXCLUDED.order_status
                WHERE
                    test_orders.order_status
                    IS DISTINCT FROM
                    EXCLUDED.order_status;
            """

            # Primeira execução
            cursor.execute(upsert_sql)
            assert cursor.rowcount == 2

            # Segunda execução: dados idênticos
            cursor.execute(upsert_sql)
            assert cursor.rowcount == 0

            # Terceira execução: alterar uma ordem
            cursor.execute("""
                INSERT INTO test_orders (
                    order_id,
                    order_status
                )
                VALUES (1, 'completed')
                ON CONFLICT (order_id)
                DO UPDATE SET
                    order_status = EXCLUDED.order_status
                WHERE
                    test_orders.order_status
                    IS DISTINCT FROM
                    EXCLUDED.order_status;
            """)

            assert cursor.rowcount == 1

            # Verificar ausência de duplicidade
            cursor.execute(
                "SELECT COUNT(*) FROM test_orders;"
            )
            assert cursor.fetchone()[0] == 2

            # Verificar atualização
            cursor.execute("""
                SELECT order_status
                FROM test_orders
                WHERE order_id = 1;
            """)
            assert cursor.fetchone()[0] == "completed"

    finally:
        connection.rollback()
        connection.close()
