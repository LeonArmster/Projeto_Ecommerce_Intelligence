# =======================================
# Buscar último dia
# =======================================
# Bibliotecas
from ecommerce_intelligence.database.database_connection import db_connection, read_query
from ecommerce_intelligence.ai.business_rules import build_metric_signals


def get_business_context() -> dict:

    connection = db_connection()

    query = read_query("business_context.sql")

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

        # ---------------------------------------
        # Criando o contexto com os dados do SQL
        # ---------------------------------------
        context = dict(zip(columns, row))

        # ---------------------------------------
        # Metadados da análise
        # ---------------------------------------
        context["analysis_granularity"] = "daily"
        context["comparison_type"] = "previous_day"

        # ---------------------------------------
        # Sinais calculados pelas regras de negócio
        # ---------------------------------------
        context["metric_signals"] = build_metric_signals(context)

        return context

    finally:
        connection.close()


def main():

    context = get_business_context()

    print(context)


if __name__ == "__main__":
    main()