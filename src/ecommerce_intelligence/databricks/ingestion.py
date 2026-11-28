import logging
from time import perf_counter

from ecommerce_intelligence.config.config import raw_dir
from ecommerce_intelligence.databricks.connection import connect_databricks
from ecommerce_intelligence.databricks.upload import upload_parquet


logger = logging.getLogger(__name__)


ENTITIES = (
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "reviews",
)

VOLUME_PATH = "/Volumes/ecommerce/raw/landing"


def main() -> None:
    """Upload source Parquet files to Databricks."""

    start_time = perf_counter()

    logger.info("Starting Databricks ingestion")

    file_paths = [
        raw_dir / f"{entity}.parquet"
        for entity in ENTITIES
    ]

    # Validate all source files before uploading
    for file_path in file_paths:
        if not file_path.is_file():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

    workspace = connect_databricks()

    for file_path in file_paths:

        file_start_time = perf_counter()

        destination = upload_parquet(
            workspace=workspace,
            file_path=file_path,
            volume_path=VOLUME_PATH,
            overwrite=True
        )

        logger.info(
            "Uploaded %s in %.2f seconds",
            destination,
            perf_counter() - file_start_time
        )

    logger.info(
        "Databricks ingestion completed in %.2f seconds",
        perf_counter() - start_time
    )


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    main()
