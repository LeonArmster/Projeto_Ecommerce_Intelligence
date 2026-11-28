import os
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from ecommerce_intelligence.config.config import raw_dir


ENTITIES = (
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "reviews",
)


def migrate_parquet(file_path: Path) -> None:
    """Convert nanosecond timestamps to microseconds."""

    schema = pq.read_schema(file_path)

    timestamp_columns = [
        field.name
        for field in schema
        if pa.types.is_timestamp(field.type)
        and field.type.unit == "ns"
    ]

    if not timestamp_columns:
        print(f"[SKIPPED] {file_path.name}: already compatible")
        return

    print(f"[MIGRATING] {file_path.name}")
    print(f"Columns: {timestamp_columns}")

    original_table = pq.read_table(file_path)

    temp_path = file_path.with_suffix(".tmp.parquet")

    try:
        pq.write_table(
            original_table,
            temp_path,
            coerce_timestamps="us",
            allow_truncated_timestamps=False
        )

        converted_table = pq.read_table(temp_path)

        if original_table.num_rows != converted_table.num_rows:
            raise ValueError("Row count mismatch")

        if original_table.column_names != converted_table.column_names:
            raise ValueError("Column mismatch")

        restored_table = converted_table.cast(
            original_table.schema,
            safe=True
        )

        if not original_table.equals(restored_table):
            raise ValueError("Data mismatch after conversion")

        os.replace(temp_path, file_path)

        print(
            f"[SUCCESS] {file_path.name}: "
            f"{original_table.num_rows:,} rows preserved"
        )

    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> None:

    for entity in ENTITIES:
        file_path = raw_dir / f"{entity}.parquet"

        migrate_parquet(file_path)


if __name__ == "__main__":
    main()
