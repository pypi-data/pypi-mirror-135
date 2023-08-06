from typing import Dict

from vialink.utils.background_task.infrastructure.s3 import S3Client
from vialink.utils.background_task.abstract import ParameterStorageAbstract
from vialink.utils.background_task.parameter_storage import S3ParameterStorage
from vialink.utils.background_task.settings import settings


def _get_parameter_storage_on_aws():
    bucket_name = f'{settings.VIALINK_TASK_BUCKET_NAME_PREFIX}-{settings.ENVIRONMENT}'
    s3 = S3Client(bucket_name, settings.AWS_REGION)
    return S3ParameterStorage(s3)


def _get_parameter_storage_on_local():
    return DummyParameterStorage()


def get_parameter_storage():
    if settings.ENVIRONMENT == 'local':
        return _get_parameter_storage_on_local()
    return _get_parameter_storage_on_aws()


class DummyParameterStorage(ParameterStorageAbstract):
    def __init__(self, dummy_params: Dict = None):
        self._dummy_params = dummy_params or {}

    def upload(self, task_type: str, task_id: str, params: Dict):
        print(f'DummyParameterStorage: parameter uploaded {params} for {task_type}.{task_id}')

    def fetch_parameters(self, task_type: str, task_id: str) -> Dict:
        print(f'DummyParameterStorage: parameter fetched for {task_type}.{task_id}')
        return self._dummy_params
