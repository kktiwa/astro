from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(dag_id='check_dag',
         description='DAG to check data',
         tags=['data_engineering_team'],
         schedule='@daily',
         start_date=datetime(2023, 1, 1),
         catchup=False
         ):
    create_file = BashOperator(task_id='create_file', bash_command="echo 'Hi there!' > /tmp/dummy")

    check_file_exists = BashOperator(task_id='check_file_exists', bash_command="test -f /tmp/dummy")

    read_file = PythonOperator(task_id='read_file', python_callable=lambda: print(open('/tmp/dummy', 'rb').read()))

    create_file >> check_file_exists >> read_file
