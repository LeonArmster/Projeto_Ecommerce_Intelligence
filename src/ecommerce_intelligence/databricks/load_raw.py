import logging
from time import perf_counter

import pyarrow.parquet as pq

from databricks.sdk import WorkspaceClient

from ecommerce_intelligence.config.config import raw_dir
from ecommerce_intelligence.databricks.connection import connect_databricks
from ecommerce_intelligence.databricks.sql_executor import execute_sql
from ecommerce_intelligence.databricks.ingestion import (
    ENTITIES,
    VOLUME_PATH,
)


logger = logging.getLogger(__name__)

CATALOG = "ecommerce"
SCHEMA = "raw"

PRIMARY_KEYS = {
    "customers": "customer_id",
    "products": "product_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "payments": "payment_id",
    "shipments": "shipment_id",
    "reviews": "review_id",
}


def validate_source(
    workspace: WorkspaceClient,
    entity: str,
) -> int:
    """Validate the source Parquet before loading."""

    file_path = raw_dir / f"{entity}.parquet"
    expected_rows = pq.read_metadata(file_path).num_rows

    source_path = f"{VOLUME_PATH}/{entity}.parquet"
    primary_key = PRIMARY_KEYS[entity]

    statement = f"""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT {primary_key}) AS unique_keys,
            COUNT_IF(_rescued_data IS NOT NULL) AS rescued_rows
        FROM read_files(
            '{source_path}',
            format => 'parquet'
        )
    """

    response = execute_sql(workspace, statement)

    total_rows, unique_keys, rescued_rows = map(
        int,
        response.result.data_array[0]
    )

    if total_rows != expected_rows:
        raise ValueError(
            f"{entity}: local and remote row counts differ"
        )

    if total_rows != unique_keys:
        raise ValueError(
            f"{entity}: duplicate or null primary keys"
        )

    if rescued_rows != 0:
        raise ValueError(
            f"{entity}: {rescued_rows} rescued records"
        )

    logger.info(
        "Source validated: %s | %s rows",
        entity,
        f"{total_rows:,}"
    )

    return total_rows


def create_raw_table(
    workspace: WorkspaceClient,
    entity: str,
) -> None:
    """Create a managed Delta table from a Parquet file."""

    table_name = f"{CATALOG}.{SCHEMA}.{entity}"
    source_path = f"{VOLUME_PATH}/{entity}.parquet"

    statement = f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        USING DELTA AS
        SELECT * EXCEPT (_rescued_data)
        FROM read_files(
            '{source_path}',
            format => 'parquet'
        )
    """

    execute_sql(workspace, statement)

    logger.info("Table available: %s", table_name)


def validate_raw_table(
    workspace: WorkspaceClient,
    entity: str,
    expected_rows: int,
) -> None:
    """Validate the loaded Delta table."""

    table_name = f"{CATALOG}.{SCHEMA}.{entity}"
    primary_key = PRIMARY_KEYS[entity]

    statement = f"""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT {primary_key}) AS unique_keys
        FROM {table_name}
    """

    response = execute_sql(workspace, statement)

    total_rows, unique_keys = map(
        int,
        response.result.data_array[0]
    )

    if total_rows != expected_rows:
        raise ValueError(
            f"{table_name}: expected {expected_rows} rows, "
            f"found {total_rows}"
        )

    if total_rows != unique_keys:
        raise ValueError(
            f"{table_name}: duplicate or null primary keys"
        )

    logger.info(
        "Table validated: %s | %s rows",
        table_name,
        f"{total_rows:,}"
    )


def main() -> None:
    """Create and validate all RAW Delta tables."""

    start_time = perf_counter()

    workspace = connect_databricks()

    logger.info("Starting Databricks RAW load")

    for entity in ENTITIES:

        expected_rows = validate_source(
            workspace,
            entity
        )

        create_raw_table(
            workspace,
            entity
        )

        validate_raw_table(
            workspace,
            entity,
            expected_rows
        )

    logger.info(
        "Databricks RAW load completed in %.2f seconds",
        perf_counter() - start_time
    )


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    main()
