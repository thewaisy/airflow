from airflow.models import Variable

class sparkSubmit:

    def __init__(self):
        pass

    def emr_spark_step(self, step_name, pyspark_script, num_executors=3, driver_memory='4g',
                       executor_cores=4, executor_memory='8g', dynamic=True, extra={}, extra_conf={}):

        extra_list = []
        extra_conf_list = []

        for k, v in extra.items():
            extra_list.extend([k, str(v)])

        for k, v in extra_conf.items():
            extra_conf_list.extend([k, v])


        SPARK_STEPS = [
            {
                'Name': step_name,
                'ActionOnFailure': 'CONTINUE',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'spark-submit',
                        '--deploy-mode', 'cluster',
                        '--master', 'yarn',
                        '--conf', 'spark.executorEnv.YARN_CONTAINER_RUNTIME_TYPE=docker',
                        '--conf',
                        f'spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE={Variable.get("spark_docker_image_name")}',
                        '--conf', 'spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_MOUNTS=/etc/passwd:/etc/passwd:ro',
                        '--conf', 'spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_TYPE=docker',
                        '--conf',
                        f'spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE={Variable.get("spark_docker_image_name")}',
                        '--conf', 'spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_MOUNTS=/etc/passwd:/etc/passwd:ro',
                        '--conf', f'spark.dynamicAllocation.enabled={"true" if dynamic else "false"}',
                        '--num-executors', f'{num_executors}',
                        '--driver-memory', driver_memory,
                        '--executor-cores', f'{executor_cores}',
                        '--executor-memory', executor_memory,
                        *extra_conf_list,
                        's3://idus-de-data/x_framework/emr/spark/ops/' + pyspark_script,
                        *extra_list,
                    ]
                }
            }
        ]

        return SPARK_STEPS
