import ast
import sys
import time
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union
from uuid import uuid4

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator, BaseOperatorLink, TaskInstance
from airflow.providers.amazon.aws.hooks.emr import EmrHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

class EmrAddStepsOperator(BaseOperator):
    """
    An operator that adds steps to an existing EMR job_flow.
    :param job_flow_id: id of the JobFlow to add steps to. (templated)
    :param job_flow_name: name of the JobFlow to add steps to. Use as an alternative to passing
        job_flow_id. will search for id of JobFlow with matching name in one of the states in
        param cluster_states. Exactly one cluster like this should exist or will fail. (templated)
    :param cluster_states: Acceptable cluster states when searching for JobFlow id by job_flow_name.
        (templated)
    :param aws_conn_id: aws connection to uses
    :param steps: boto3 style steps or reference to a steps file (must be '.json') to
        be added to the jobflow. (templated)
    :param target_states: the target states, sensor waits until
        step reaches any of these states
    :param failed_states: the failure states, sensor fails when
        step reaches any of these states
    :param do_xcom_push: if True, job_flow_id is pushed to XCom with key job_flow_id.
    """
    # ui render template
    template_fields: Sequence[str] = ('job_flow_id', 'job_flow_name', 'cluster_states',
                                      'step', 'target_states', 'failed_states')
    template_ext: Sequence[str] = ('.json',)
    template_fields_renderers = {"step": "json"}
    ui_color = '#33FFCC' # ui상의 아이콘 색
    ui_fgcolor = '#000000' # ui상의 폰트 색


    def __init__(
            self,
            job_flow_id: Optional[str] = None,
            job_flow_name: Optional[str] = None,
            cluster_states: Optional[List[str]] = None,
            aws_conn_id: str = 'aws_default',
            step: Optional[Union[List[dict], str]] = None,
            target_states: Optional[str] = None,
            failed_states: Optional[str] = None,
            **kwargs
    ) -> None:

        if kwargs.get('xcom_push') is not None:
            raise AirflowException("'xcom_push' was deprecated, use 'do_xcom_push' instead")
        # 둘 중 하나만 받을 수 있음
        if not (job_flow_id is None) ^ (job_flow_name is None):
            raise AirflowException('Exactly one of job_flow_id or job_flow_name must be specified.')

        super().__init__(**kwargs)
        self.aws_conn_id = aws_conn_id
        self.job_flow_id = job_flow_id
        self.job_flow_name = job_flow_name
        self.cluster_states = cluster_states or []
        self.step = step or []
        self.target_states = target_states or ['COMPLETED']
        self.failed_states = failed_states or ['CANCELLED', 'FAILED', 'INTERRUPTED']

    def execute(self, context: 'Context') -> List[str]:
        emr_hook = EmrHook(aws_conn_id=self.aws_conn_id)

        emr = emr_hook.get_conn()

        job_flow_id = self.job_flow_id or emr_hook.get_cluster_id_by_name(
            str(self.job_flow_name), self.cluster_states
        )

        if not job_flow_id:
            raise AirflowException(f'No cluster found for name: {self.job_flow_name}')

        if self.do_xcom_push:
            context['ti'].xcom_push(key='job_flow_id', value=job_flow_id)

        self.log.info('Adding steps to %s', job_flow_id)

        # steps may arrive as a string representing a list
        # e.g. if we used XCom or a file then: steps="[{ step1 }, { step2 }]"

        response = emr.add_job_flow_steps(JobFlowId=job_flow_id, Steps=self.step)

        if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
            raise AirflowException(f'Adding steps failed: {response}')
        else:
            step_id = response['StepIds'][0]
            self.log.info('Steps %s added to JobFlow', step_id)
          
        # sensor 
        self.log.info('Poking step %s on cluster %s', step_id, job_flow_id)
        
        while True:
            
            response = emr.describe_step(ClusterId=job_flow_id, StepId=step_id)
            
            if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
                self.log.info('Bad HTTP response: %s', response)        
            
            else:
                state = response['Step']['Status']['State']
                
                if state in self.target_states:
                    break
                
                if state in self.failed_states:
                    self.log.info('Bad HTTP response: %s', response)
                    final_message = 'EMR job failed'
                    failure_message = self.failure_message_from_response(response)
                    if failure_message:
                        final_message += ' ' + failure_message
                    raise AirflowException(final_message)
            time.sleep(10)
            
        return step_id
                
    @staticmethod
    def failure_message_from_response(response: Dict[str, Any]) -> Optional[str]:
        """
        Get failure message from response dictionary.
        :param response: response from AWS API
        :return: failure message
        :rtype: Optional[str]
        """
        fail_details = response['Step']['Status'].get('FailureDetails')
        if fail_details:
            return 'for reason {} with message {} and log file {}'.format(
                fail_details.get('Reason'), fail_details.get('Message'), fail_details.get('LogFile')
            )
        return None
        