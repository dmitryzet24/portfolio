from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'dmitrii',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'google_store_elt_pipeline',
    description = 'Full ELT pipeline: Python extract -> dbt transform',
    default_args = default_args,
    schedule_interval = '0 0 * * *',
    catchup = False
) as dag:

    extract_load_task = BashOperator(
        task_id='extract_load_task',
        bash_command="python /opt/airflow/extract_load/extract_data.py"
        )

    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command="""
            dbt run --project-dir /opt/airflow/dbt_project/dbt/my_transformer \
                    --profiles-dir /opt/airflow/.dbt \
                    --target dev
        """,
        # Добавляем переменные окружения явно, если Airflow их теряет
        env={
            'DBT_USER': 'dmitrii',
            'DBT_PASSWORD': 'pass',
            'DBT_DB': 'google_shop_data',
            'DBT_HOST': 'db',
            'DBT_PORT': '5432',
            **os.environ  # пробрасываем остальные системные переменные
        },
        dag=dag,
    )

    extract_load_task >> dbt_run_task