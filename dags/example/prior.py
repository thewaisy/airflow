import logging
from airflow.utils.timezone import datetime as adt
from datetime import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'hanyoon',
    # 'max_active_tasks': 4,
    'max_active_runs': 1,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='prior_weight_example',
    concurrency=2,
    schedule_interval=None,
    start_date=adt(2021, 8, 1, 22),
    default_args=default_args,
    description='sub dag example',
    tags=['hanyoon', 'prior', 'example'],
) as dag:
    start = DummyOperator(
        task_id="start_test",
        dag=dag,
    )

    end = DummyOperator(
        task_id="end_test",
        dag=dag,
    )

    task_list = []
    weight = 2
    for i in range(6):

        task_1 = BashOperator(
            task_id=f'task_1_{i}',
            bash_command='sleep 5',
            weight_rule='downstream',
            priority_weight=weight,
            dag=dag
        )
        task_2 = BashOperator(
            task_id=f'task_2_{i}',
            bash_command='sleep 5',
            priority_weight=weight-1,
            dag=dag
        )

        task_1 >> task_2 >> end
        task_list.append(task_1)
        weight += 2

    start >> task_list
