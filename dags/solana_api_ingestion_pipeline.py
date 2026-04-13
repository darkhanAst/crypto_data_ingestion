from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from include.solana_api import get_current_slot, get_block, get_performance_samples
from include.clickhouse import insert_block, insert_performance
from include.alerts.telegram import send_telegram_message


def task_failure_alert(context):
    dag_id = context.get("dag").dag_id
    task_id = context.get("task_instance").task_id
    execution_date = context.get("logical_date")

    error = context.get("exception")

    message = f"""
        DAG FAILED
        DAG: {dag_id}
        Task: {task_id}
        Date: {execution_date}
        Error:{error}
    """
    send_telegram_message(message)



def get_slot(**context):
    slot = get_current_slot() - 1  
    print(f"Slot: {slot}")

    context["ti"].xcom_push(key="slot", value=slot)


def fetch_block(**context):
    slot = context["ti"].xcom_pull(key="slot", task_ids="get_slot")

    block = get_block(slot)

    if block is None:
        print("Block not ready")
        return

    insert_block(block, slot)



def fetch_performance(**context):
    samples = get_performance_samples()
    insert_performance(samples)


with DAG(
    dag_id="solana_api_clickhouse_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["solana", "pipeline"],
    default_args={
        "retries": 0,
        "on_failure_callback": task_failure_alert
    }
) as dag:

    task_get_slot = PythonOperator(
        task_id="get_slot",
        python_callable=get_slot
    )

    task_block = PythonOperator(
        task_id="fetch_block",
        python_callable=fetch_block
    )

    task_perf = PythonOperator(
        task_id="fetch_performance",
        python_callable=fetch_performance
    )

    task_get_slot >> [task_block, task_perf]