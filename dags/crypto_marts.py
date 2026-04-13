
from cosmos import DbtDag, ProjectConfig
from include.profiles import clickhouse_db
from include.constants import venv_execution_config

import pytz
from datetime import datetime

local_tz = pytz.timezone('Asia/Almaty')

crypt_marts = DbtDag(
    project_config=ProjectConfig('/usr/local/airflow/dbt/dbt_crypto_analytics'),
    profile_config=clickhouse_db,
    execution_config=venv_execution_config,
    default_args={
        "retries": 1,
    },
    schedule="@daily",  
    start_date=datetime(2026, 1, 1, tzinfo=local_tz),
    catchup=False,
    dag_id="crypt_marts",
    tags=["marts", "bi"]
)
