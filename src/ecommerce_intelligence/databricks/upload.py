import logging
from pathlib import Path

from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def upload_parquet(
    workspace: WorkspaceClient,
    file_path: Path,
    volume_path: str = "/Volumes/ecommerce/raw/landing",
    overwrite: bool = False
) -> str:
    """Upload a local Parquet file to a Databricks volume."""

    if not file_path.is_file():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.suffix.lower() != ".parquet":
        raise ValueError(
            f"Expected a Parquet file: {file_path}"
        )

    destination = f"{volume_path.rstrip('/')}/{file_path.name}"

    logger.info(
        "Uploading %s to %s",
        file_path.name,
        destination
    )

    with file_path.open("rb") as file:
        workspace.files.upload(
            destination,
            file,
            overwrite=overwrite
        )

    logger.info("Upload completed: %s", destination)

    return destination
