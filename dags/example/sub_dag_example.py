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

execution = '{{ execution_date.in_timezone("Asia/Seoul") }}'

default_args = {
    'owner': 'hanyoon',
    'depends_on_past': True,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),

}

dag = DAG(
    dag_id='sub_dag_example',
    default_args=default_args,
    catchup=True,
    schedule_interval="0 * * * *",
    start_date=adt(2021, 8, 1, 22),
    description='sub dag example',
    tags=['hanyoon', 'subdag', 'example'],
)

def print_info(note):
    print(note)

def load_subdag(parent_dag_name, child_dag_name, args):
    dag_subdag = DAG(
        dag_id='{0}.{1}'.format(parent_dag_name, child_dag_name),
        default_args=args,
        # start_date가 없다면 에러가 발생한다.
        start_date=adt(2021, 8, 2), # sub dag의 start_date 설정해도 적용된다.
        # schedule_interval="*/20 * * * *", # sub dag의 schedule_interval을 설정해도 적용되지 않는거 같다
    )
    with dag_subdag:
        for i in range(5):
            t = PythonOperator(
                task_id='load_subdag_{0}'.format(i),
                python_callable=print_info,
                op_kwargs={
                    "note": f"python operator num {i}"
                },
                dag=dag_subdag,
            )

    return dag_subdag

load_tasks = SubDagOperator(
    task_id="load_tasks", # sub task name
    subdag=load_subdag(
        parent_dag_name="sub_dag_example",
        child_dag_name="load_tasks",
        args=default_args
    ),
    default_args=default_args,
    dag=dag,
)

load_tasks