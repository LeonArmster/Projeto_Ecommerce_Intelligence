# =======================================
# Buscar último dia
# =======================================
# Bibliotecas
from ecommerce_intelligence.database.database_connection import db_connection, read_query



def get_business_context() -> dict:

    connection = db_connection()

    query = read_query('business_context.sql')

    try:

        with connection.cursor() as cursor:

            cursor.execute(query)

            columns = [
                description.name
                for description in cursor.description
            ]

            row = cursor.fetchone()

        if row is None:
            raise ValueError(
                "Nenhum dado disponível para gerar o Business Brief."
            )

        return dict(zip(columns, row))

    finally:
        connection.close()


def main():

    context = get_business_context()

    print(context)


if __name__ == "__main__":
    main()