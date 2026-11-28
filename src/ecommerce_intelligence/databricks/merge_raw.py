import logging
from time import perf_counter

import pyarrow.parquet as pq

from databricks.sdk import WorkspaceClient

from ecommerce_intelligence.config.config import raw_dir
from ecommerce_intelligence.databricks.connection import connect_databricks
from ecommerce_intelligence.databricks.sql_executor import execute_sql
from ecommerce_intelligence.databricks.ingestion import VOLUME_PATH

from ecommerce_intelligence.databricks.load_raw import (
    CATALOG,
    SCHEMA,
    PRIMARY_KEYS,
    validate_source,
    validate_raw_table,
)


logger = logging.getLogger(__name__)


INCREMENTAL_ENTITIES = (
    "orders",
    "order_items",
    "payments",
    "shipments",
    "reviews",
)


def build_merge_statement(entity: str) -> str:
    """Build a Delta MERGE statement from Parquet metadata."""

    primary_key = PRIMARY_KEYS[entity]

    file_path = raw_dir / f"{entity}.parquet"

    columns = pq.read_schema(file_path).names

    if primary_key not in columns:
        raise ValueError(
            f"{entity}: primary key {primary_key} not found"
        )

    comparison_columns = [
        column
        for column in columns
        if column != primary_key
    ]

    if not comparison_columns:
        raise ValueError(
            f"{entity}: no columns available for comparison"
        )

    selected_columns = ", ".join(
        f"`{column}`" for column in columns
    )

    comparison = "\n        AND ".join(
        f"target.`{column}` <=> source.`{column}`"
        for column in comparison_columns
    )

    table_name = f"{CATALOG}.{SCHEMA}.{entity}"
    source_path = f"{VOLUME_PATH}/{entity}.parquet"

    return f"""
        MERGE INTO {table_name} AS target

        USING (
            SELECT {selected_columns}
            FROM read_files(
                '{source_path}',
                format => 'parquet'
            )
        ) AS source

        ON target.`{primary_key}` = source.`{primary_key}`

        WHEN MATCHED AND NOT (
            {comparison}
        )
        THEN UPDATE SET *

        WHEN NOT MATCHED
        THEN INSERT *
    """


def merge_raw_table(
    workspace: WorkspaceClient,
    entity: str,
) -> None:
    """Insert new records and update modified records."""

    start_time = perf_counter()

    statement = build_merge_statement(entity)

    logger.info("Merging entity: %s", entity)

    response = execute_sql(workspace, statement)

    if response.result and response.result.data_array:
        logger.info(
            "MERGE result: %s",
            response.result.data_array
        )

    logger.info(
        "MERGE completed: %s | %.2f seconds",
        entity,
        perf_counter() - start_time
    )


def main() -> None:
    """Execute incremental RAW loads."""

    start_time = perf_counter()

    workspace = connect_databricks()

    logger.info("Starting Databricks incremental RAW load")

    for entity in INCREMENTAL_ENTITIES:

        expected_rows = validate_source(
            workspace,
            entity
        )

        merge_raw_table(
            workspace,
            entity
        )

        validate_raw_table(
            workspace,
            entity,
            expected_rows
        )

    logger.info(
        "Incremental RAW load completed in %.2f seconds",
        perf_counter() - start_time
    )


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    main()
