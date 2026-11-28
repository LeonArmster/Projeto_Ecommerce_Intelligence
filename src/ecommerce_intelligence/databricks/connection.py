import os
import logging

from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def connect_databricks(
    profile: str | None = None
) -> WorkspaceClient:
    """Create an authenticated Databricks workspace client."""

    profile = profile or os.getenv(
        "DATABRICKS_PROFILE",
        "ecommerce"
    )

    logger.info(
        "Initializing Databricks client with profile: %s",
        profile
    )

    return WorkspaceClient(profile=profile)
