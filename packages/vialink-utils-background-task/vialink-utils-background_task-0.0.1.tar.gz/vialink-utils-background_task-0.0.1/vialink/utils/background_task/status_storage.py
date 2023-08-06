from typing import List, Dict
from decimal import Decimal

from .abstract import StatusStorageAbstract, TaskAbstract
from .task import Task
from .infrastructure.dynamo import DynamoClient, Key


class DynamoStatusStorage(StatusStorageAbstract):
    def __init__(self, dynamo: DynamoClient):
        self._dynamo = dynamo

    def get_status(self, task_type: str, task_id: str) -> str:
        condition = Key('taskType').eq(task_type) & Key('taskId').eq(task_id)
        results = self._dynamo.query_with_key(condition, limit=1)
        if not results:
            return 'NOTFOUND'
        return results[0]['status']

    def list_tasks(self, status=None, started_timestamp_lt=None, launched_timestamp_lt=None) -> List[TaskAbstract]:
        condition = Key('status').eq(status)
        if started_timestamp_lt:
            condition &= Key('startedTs').lt(Decimal(started_timestamp_lt))
            index_name = 'startedTsIndex'
        elif launched_timestamp_lt:
            condition &= Key('launchedTs').lt(Decimal(launched_timestamp_lt))
            index_name = 'launchedTsIndex'
        else:
            condition &= Key('launchedTs').gte(Decimal(0))
            index_name = 'launchedTsIndex'

        items = self._dynamo.query_with_index(index_name, condition, limit=100)
        return [Task(item['taskType'], item['taskId'], None) for item in items]

    def update_status(self, task_type: str, task_id: str, status: str, *,
                      launched_timestamp: float = None, started_timestamp: float = None, metadata: Dict = None):
        item = {'taskType': task_type, 'taskId': task_id, 'status': status, 'metadata': metadata,
                'launchedTs': Decimal(launched_timestamp or 0), 'startedTs': Decimal(started_timestamp or 0)}

        self._dynamo.put_item(item)
