from airflow.models import DAG
from airflow.utils.timezone import datetime as adt
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator


def random_subdag(parent_dag_name, child_dag_name, args):
    with DAG(
        # subdag의 id는 이와같은 컨벤션으로 쓴답니다.
        dag_id='%s.subdag_%s' % (parent_dag_name, child_dag_name),
        default_args=args,
        start_date=adt(2021, 8, 2, 3),
        # schedule_interval=None, # 값을 넣어주어야 합니다.
    ) as dag_subdag:

        union = DummyOperator(
            task_id='%s-union' % (child_dag_name),
            dag=dag_subdag
        )

        for i in range(2):
            process_a = DummyOperator(
                task_id='%s-task_A-%s' % (child_dag_name, i + 1),
                dag=dag_subdag,
            )
            # globals()['process_b'] = BashOperator(
            process_b = DummyOperator(
                task_id='%s-task_B-%s' % (child_dag_name, i + 1),
                dag=dag_subdag,
            )

            process_a >> process_b >> union

    return dag_subdag
