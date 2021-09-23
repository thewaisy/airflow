from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG(
    dag_id='fail_example',  # DAG id
    start_date=datetime(2021, 7, 25),  # 언제부터 DAG이 시작되는가
    schedule_interval='0 10 * * *',  # 매일 10시에 실행
    catchup=False,  # 과거데이터 처리를 설정
)

t1 = BashOperator(task_id='collect_wood', bash_command='echo collect wood', dag=dag)
t2 = BashOperator(task_id='start_fire', bash_command='echo start fire', dag=dag)
t3 = BashOperator(task_id='fish', bash_command='echo fish', dag=dag)
t4 = BashOperator(task_id='cook', bash_command='echo cook', dag=dag)

t1 >> t2 >> t4  # t1이 완료되면 t2 수행 가능; t2가 완료되면 t4 수행 가능
t3 >> t4  # t3가 완료되면 t4 수행 가능