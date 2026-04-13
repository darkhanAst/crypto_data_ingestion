from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta

from include.bitcoin_s3 import read_blocks, read_transactions
from include.clickhouse import insert_btc_blocks, insert_btc_transactions
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



def load_blocks():
    date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    df = read_blocks(date)
    if len(df) == 0:
        print("No blocks found")
        return

    insert_btc_blocks(df, date)


def load_transactions():
    date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    df = read_transactions(date)
    if len(df) == 0:
        print("No transactions found")
        return

    insert_btc_transactions(df, date)


with DAG(
    dag_id="btc_s3_to_clickhouse_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["btc", "s3"],
    default_args={
        "retries": 0,
        "on_failure_callback": task_failure_alert
    }
        
) as dag:

    t1 = PythonOperator(
        task_id="load_blocks",
        python_callable=load_blocks
    )

    t2 = PythonOperator(
        task_id="load_transactions",
        python_callable=load_transactions
    )

    t1 >> t2