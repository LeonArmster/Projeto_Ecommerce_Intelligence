import os
import logging
from time import sleep, monotonic

from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import (
    StatementResponse,
    StatementState,
)

load_dotenv()

logger = logging.getLogger(__name__)


def execute_sql(
    workspace: WorkspaceClient,
    statement: str,
    warehouse_id: str | None = None,
    timeout: int = 600,
    poll_interval: int = 2,
) -> StatementResponse:
    """Execute a SQL statement and wait for its completion."""

    warehouse_id = warehouse_id or os.getenv(
        "DATABRICKS_WAREHOUSE_ID"
    )

    if not warehouse_id:
        raise ValueError(
            "DATABRICKS_WAREHOUSE_ID is not configured"
        )

    start_time = monotonic()

    logger.info("Submitting SQL statement")

    response = workspace.statement_execution.execute_statement(
        warehouse_id=warehouse_id,
        statement=statement,
        wait_timeout="10s",
    )

    statement_id = response.statement_id

    while response.status.state in (
        StatementState.PENDING,
        StatementState.RUNNING,
    ):

        if monotonic() - start_time >= timeout:
            workspace.statement_execution.cancel_execution(
                statement_id=statement_id
            )

            raise TimeoutError(
                f"SQL execution exceeded {timeout} seconds"
            )

        sleep(poll_interval)

        response = workspace.statement_execution.get_statement(
            statement_id=statement_id
        )

    if response.status.state != StatementState.SUCCEEDED:
        error = response.status.error

        raise RuntimeError(
            f"SQL execution failed: "
            f"{error.message if error else response.status.state}"
        )

    logger.info(
        "SQL statement completed in %.2f seconds",
        monotonic() - start_time
    )

    return response
