from airflow.utils.timezone import datetime as adt
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
# import operator
from airflow.operators.python import PythonOperator
# import hook
from airflow.hooks.base import BaseHook
# import utils


def print_note(note):
    print("+" * 10)
    print(note)
    print("+" * 10)


def dummy_sub(parent_dag_name, child_dag_name, args):
    with DAG(
        dag_id=f'{parent_dag_name}.{child_dag_name}',
        start_date=adt(2021, 10, 1),
        tags=['hanyoon', 'subdag', child_dag_name],
        default_args=args,
    ) as subdag:

        start = PythonOperator(
            task_id=f'{child_dag_name}.start',
            python_callable=print_note,
            op_kwargs={
                "note": "start"
            },
            dag=subdag,
        )

        mid = PythonOperator(
            task_id=f'{child_dag_name}.mid',
            python_callable=print_note,
            op_kwargs={
                "note": "mid"
            },
            dag=subdag,
        )

        end = PythonOperator(
            task_id=f'{child_dag_name}.end',
            python_callable=print_note,
            op_kwargs={
                "note": "end"
            },
            dag=subdag,
        )

        start >> mid >> end
    return subdag
