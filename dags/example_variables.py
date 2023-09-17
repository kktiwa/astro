from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from pendulum import datetime


def _ml_task(ml_parameter):
    print(ml_parameter)


with DAG(
        dag_id='example_variable',
        start_date=datetime(2023, 9, 17),
        schedule_interval='@daily',
        catchup=False
) as dag:
    ml_tasks = []

    for ml_parameter in Variable.get('ml_model_parameters', deserialize_json=True)["param"]:
        ml_tasks.append(
            PythonOperator(
                task_id=f'ml_task_{ml_parameter}',
                python_callable=_ml_task,
                op_kwargs={
                    'ml_parameter': ml_parameter
                }
            )
        )

        # Jinja notation: var.value.<var_key>
    report = BashOperator(
        task_id='report',
        bash_command='echo "report_{{ var.value.ml_report_name }}"'
    )

ml_tasks >> report
