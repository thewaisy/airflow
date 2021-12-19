from airflow.utils.timezone import datetime as adt
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
# import operator
from airflow.operators.dummy import DummyOperator
# import hook
from airflow.hooks.base import BaseHook
# import utils


def dummy_sub(parent_dag_name, child_dag_name, args):
    with DAG(
        dag_id=f'{parent_dag_name}.{child_dag_name}',
        start_date=adt(2021, 10, 1),
        tags=['hanyoon', 'subdag', child_dag_name],
        default_args=args,
    ) as subdag:
        
        start = DummyOperator(
            task_id=f'{child_dag_name}.start',
            dag=subdag,
        )

        mid = DummyOperator(
            task_id=f'{child_dag_name}.mid',
            dag=subdag,
        )

        end = DummyOperator(
            task_id=f'{child_dag_name}.end',
            dag=subdag,
        )

        start >> mid >> end
    return subdag
