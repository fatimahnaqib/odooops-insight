# airflow_dags/odoo_etl_dags.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'fatimah',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='odoo_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 6, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["odoo", "etl", "analytics"]
) as dag:

    extract_transform = BashOperator(
        task_id='extract_transform',
        bash_command='cd /opt/airflow && python3 -m etl.run_extracts',
    )
    load_to_postgres = BashOperator(
        task_id='load_to_postgres',
        bash_command='cd /opt/airflow && python3 -m etl.load_to_postgres',
    )

    extract_transform >> load_to_postgres
