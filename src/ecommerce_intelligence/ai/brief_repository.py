# ============================================================
# Salvando os dados no banco para avaliação
# ============================================================
import json
from datetime import date, datetime
from decimal import Decimal
from ecommerce_intelligence.database.database_connection import db_connection, read_query


def serialize_json(data: dict) -> str:

    def serializer(value):

        if isinstance(value, Decimal):
            return float(value)

        if isinstance(value, (date, datetime)):
            return value.isoformat()

        raise TypeError(
            f"Tipo não serializável: {type(value)}"
        )

    return json.dumps(
        data,
        default=serializer,
        ensure_ascii=False,
    )


def save_business_brief(
    reference_date: date,
    provider: str,
    model_name: str,
    context: dict,
    brief: dict,
    generation_duration_seconds: float,
) -> None:

    query = read_query("brief_repository.sql")

    connection = db_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    reference_date,
                    provider,
                    model_name,
                    serialize_json(context),
                    serialize_json(brief),
                    generation_duration_seconds,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()