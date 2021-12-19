# from airflow.utils.timezone import datetime as adt
# from datetime import timedelta
# from airflow import DAG
# from airflow.models import Variable
# # import operator
# from airflow.providers.amazon.aws.operators.athena import AWSAthenaOperator
# from airflow.operators.python import PythonOperator
# from airflow.operators.dummy import DummyOperator
# # import utils
# from utils.slack_noti import SlackAlert
# import json
# import boto3

# alert = SlackAlert()
# today = '{{ next_execution_date.in_timezone("Asia/Seoul").strftime("%Y%m%d") }}'
# topic_dict = json.loads(Variable.get('topic_list'))
# s3 = boto3.resource('s3')

# default_args = {
#     'owner': 'hanyoon',
#     'depends_on_past': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1),
#     'description': 'server_log json_table add partition',
# }


# def print_info(**kwargs):
#     print("execution_date")
#     print(kwargs['execution_date'])
#     print("execution_date to kst")
#     print(kwargs['execution_date'].in_timezone('Asia/Seoul'))
#     print("next_execution_date to kst")
#     print(kwargs['next_execution_date'].in_timezone('Asia/Seoul'))
#     return

# def add_folder(s3_folder, p_ymd):
#     s3.Object('idus-de-data', f"bronze/server_log/{s3_folder}/json/p_ymd={p_ymd}/").put()
#     return

# def topic_info(topic, topic_info):
#     print("topic", topic)
#     print("table_json", topic_info['table_json'])
#     print("s3_folder", topic_info['s3_folder'])
#     print("="*10)


# with DAG(
#         dag_id='server_log_json_add_partition',
#         default_args=default_args,
#         schedule_interval='10 0 * * *',
#         start_date=adt(2021, 11, 10),
#         catchup=True,
#         concurrency=3,
#         on_failure_callback=alert.slack_webhook_fail_alert,
#         tags=['hanyoon', 'server_log', 'json', 'add_partition'],
# ) as dag:
#     print_info = PythonOperator(
#         task_id='print_execution_info',
#         python_callable=print_info,
#         dag=dag,
#     )

#     task_end = DummyOperator(
#         task_id='task_finish',
#         trigger_rule='none_failed_or_skipped',
#         dag=dag,
#     )

#     topic_tasks = []
#     for topic, topic_info in topic_dict.items():

#         add_query = f"""
#             ALTER TABLE b_server_log.{topic_info['table_json']} ADD IF NOT EXISTS PARTITION (p_ymd = '{today}') 
#             LOCATION 's3://idus-de-data/bronze/server_log/{topic_info['s3_folder']}/json/p_ymd={today}/'
#         """
#         # add s3 folder
#         add_folder = PythonOperator(
#             task_id=f'{topic}_add_folder',
#             python_callable=topic_info,
#             op_kwargs={
#                 "s3_folder": topic_info['s3_folder'],
#                 "p_ymd": today,
#             },
#             dag=dag,
#         )

#         # athena add partititon
#         add_partition = AWSAthenaOperator(
#             task_id=f'{topic}_json_add_partition',
#             query=add_query,
#             output_location='s3://idus-de-data/x_framework/athena/primary/',
#             database="b_server_log",
#             workgroup='primary',
#             max_tries=3,
#             aws_conn_id="aws_conn",
#             dag=dag,
#         )

#         add_folder >> add_partition >> task_end
#         topic_tasks.append(add_folder)

#     print_info >> topic_tasks
