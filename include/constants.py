"Contains constants used in the DAGs"

from pathlib import Path
from cosmos import ExecutionConfig


dbt_executable = Path("/usr/local/airflow/dbt_venv/bin/activate")

venv_execution_config = ExecutionConfig(
    dbt_executable_path=str(dbt_executable)
)
