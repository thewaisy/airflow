from airflow.utils.timezone import datetime as adt
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'hanyoon',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'description': '조건 테스크 실행 예제',
}

dag = DAG(
    dag_id='condition_dag_example',
    default_args=default_args,
    catchup=True,
    schedule_interval=None,
    start_date=adt(2021, 8, 25),
    tags=['hanyoon', 'example', 'condition'],
)


def _check_condition():
    task_path = False
    if task_path:
        return 't1'
    return 't2'

check = BranchPythonOperator(
    task_id='condition_check',
    python_callable=_check_condition,
    dag=dag,
)

t1 = DummyOperator(
    task_id='t1',
    dag=dag,
)

t2 = DummyOperator(
    task_id='t2',
    dag=dag,
)

t3 = DummyOperator(
    task_id='t3',
    dag=dag,
)

finish = DummyOperator(
    task_id='finish',
    trigger_rule='one_success',
    dag=dag,
)

check >> [t1, t2]
t2 >> t3
[t1, t3] >>  finish