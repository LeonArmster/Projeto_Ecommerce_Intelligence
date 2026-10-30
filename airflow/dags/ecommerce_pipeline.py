# =====================================================
# DAG do Airflow
# =====================================================
from datetime import datetime, timedelta
from airflow.sdk import DAG, TaskGroup
from airflow.providers.standard.operators.bash import BashOperator


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="ecommerce_intelligence_pipeline",
    description="Pipeline end-to-end da plataforma E-commerce Intelligence",
    start_date=datetime(2026, 10, 29),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["ecommerce", "analytics-engineering", "dbt"],
) as dag:

    # =================================================
    # 1. Ingestion
    # =================================================
    with TaskGroup(group_id="ingestion") as ingestion:

        generate_data = BashOperator(
            task_id="generate_data",
            bash_command=(
                "python -m "
                "ecommerce_intelligence.generator.generate"
            ),
        )

        prepare_staging = BashOperator(
            task_id="prepare_staging",
            bash_command=(
                "python -m "
                "ecommerce_intelligence.transform.prepare_staging"
            ),
        )

        load_raw = BashOperator(
            task_id="load_raw",
            bash_command=(
                "python -m "
                "ecommerce_intelligence.load.load_raw"
            ),
        )

        generate_data >> prepare_staging >> load_raw

    # =================================================
    # 2. Transformation
    # =================================================
    with TaskGroup(group_id="transformation") as transformation:

        dbt_snapshot = BashOperator(
            task_id="dbt_snapshot",
            bash_command=(
                "dbt snapshot "
                "--project-dir /opt/airflow/dbt/ecommerce "
                "--profiles-dir /opt/airflow/dbt/profiles"
            ),
        )

        dbt_build = BashOperator(
            task_id="dbt_build",
            bash_command=(
                "dbt build "
                "--project-dir /opt/airflow/dbt/ecommerce "
                "--profiles-dir /opt/airflow/dbt/profiles"
            ),
            execution_timeout=timedelta(minutes=30),
        )

        dbt_snapshot >> dbt_build

    # =================================================
    # Pipeline
    # =================================================
    ingestion >> transformation