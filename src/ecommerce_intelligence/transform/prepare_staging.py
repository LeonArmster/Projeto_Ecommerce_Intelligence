# ============================================
# Orquestrador de conversão do parquet para csv
# ============================================
# Bibliotecas
from ecommerce_intelligence.config.config import raw_dir, processed_dir
from ecommerce_intelligence.transform.parquet_csv import parquet_to_csv


TABLES = [
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "reviews",
]


def main() -> None:

    for table in TABLES:

        print(f"Preparando {table}...")

        parquet_to_csv(
            source=raw_dir / f"{table}.parquet",
            destination=processed_dir / f"{table}.csv",
        )

        print(f"{table} preparado.")


if __name__ == "__main__":
    main()