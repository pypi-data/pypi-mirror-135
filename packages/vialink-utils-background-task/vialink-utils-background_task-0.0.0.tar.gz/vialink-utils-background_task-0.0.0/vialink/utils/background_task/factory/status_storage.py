from typing import Dict, List

from vialink.utils.background_task.infrastructure.dynamo import DynamoClient
from vialink.utils.background_task.abstract import StatusStorageAbstract, TaskAbstract
from vialink.utils.background_task.status_storage import DynamoStatusStorage
from vialink.utils.background_task.settings import settings


def _get_status_storage_on_aws():
    table_name = f'{settings.VIALINK_TASK_TABLE_NAME_PREFIX}-{settings.ENVIRONMENT}'
    field_types = {'taskType': 'S', 'taskId': 'S', 'status': 'S', 'startedTs': 'N', 'launchedTs': 'N'}
    global_second_indexes = {'startedTsIndex': ('status', 'startedTs'),
                             'launchedTsIndex': ('status', 'launchedTs')}
    dynamo = DynamoClient(table_name, 'taskType', field_types, ['taskId'], global_second_indexes)
    return DynamoStatusStorage(dynamo)


def _get_status_storage_on_local():
    return DummyStatusStorage()


def get_status_storage():
    if settings.ENVIRONMENT == 'local':
        return _get_status_storage_on_local()
    return _get_status_storage_on_aws()


class DummyStatusStorage(StatusStorageAbstract):
    def get_status(self, task_type: str, task_id: str) -> str:
        print(f'DummyStatusStorage: fetched status for {task_type}.{task_id}')
        return 'PENDING'

    def list_tasks(self, status=None, started_timestamp_lt=None, launched_timestamp_lt=None) -> List[TaskAbstract]:
        print(f'DummyStatusStorage: fetched tasks with condition '
              f'status={status} started_timestamp_lt={started_timestamp_lt} '
              f'launched_timestamp_lt={launched_timestamp_lt}')
        return []

    def update_status(self, task_type: str, task_id: str, status: str, *, launched_timestamp: float = None,
                      started_timestamp: float = None, metadata: Dict = None):
        print(f'DummyStatusStorage: update status for {task_type}.{task_id} '
              f'status={status} started_timestamp={started_timestamp} '
              f'launched_timestamp={launched_timestamp} metadata={metadata}')
