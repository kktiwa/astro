from airflow import DAG
from airflow.decorators import task

from datetime import datetime

with DAG('xcoms_dag',
         start_date=datetime(2023, 9, 16),
         schedule_interval='@daily',
         catchup=False
         ) as dag:
    @task
    def peter_task(ti=None):
        ti.xcom_push(key="mobile_phone", value="iPhone")


    @task
    def bryan_task(ti=None):
        phone = ti.xcom_pull(task_ids="peter_task", key="mobile_phone")
        print(phone)


    peter_task() >> bryan_task()
