import logging
from airflow.utils.timezone import datetime as adt
from datetime import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from airflow.operators.subdag import SubDagOperator
from airflow.operators.dummy import DummyOperator
from subdag.sub_example import random_subdag

execution = '{{ execution_date.in_timezone("Asia/Seoul") }}'

default_args = {
    'owner': 'hanyoon',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),

}

with DAG(
    dag_id='import_sub_dag_example',
    concurrency=3,
    max_active_runs=1,
    catchup=False,
    schedule_interval=None,
    start_date=adt(2021, 12, 3, 9),
    # description='sub dag example',
    default_args=default_args,
    tags=['hanyoon', 'subdag', 'example'],
) as dag:

    start = DummyOperator(
        task_id="start",
        dag=dag,
    )

    end = DummyOperator(
        task_id="end",
        trigger_rule='all_success',
        dag=dag,
    )

    sub_list = []
    for i in range(4):
        load_subdag = SubDagOperator(
            # SubDagOperator의 task_id와 sub_dag의 child_dag_name가 동일해야한다
            task_id=f"subdag_{i}",
            subdag=random_subdag(
                parent_dag_name=dag.dag_id,
                child_dag_name=i,
                args=default_args
            ),
            dag=dag,
        )

        check_sub_dag = DummyOperator(
            task_id=f"subdag_{i}_check",
            dag=dag,
        )

        load_subdag >> check_sub_dag >> end
        sub_list.append(load_subdag)

    start >> sub_list
