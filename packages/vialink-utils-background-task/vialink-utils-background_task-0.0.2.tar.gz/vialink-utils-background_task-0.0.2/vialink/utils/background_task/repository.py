from typing import Dict, List, Callable
from abc import ABC, abstractmethod
from bson.objectid import ObjectId

from .abstract import (
    StatusStorageAbstract, ParameterStorageAbstract, TaskRepositoryAbstract, TaskAbstract, ClockAbstract,
)
from .clock import Clock


class TaskIdGeneratorAbstract(ABC):
    @abstractmethod
    def next_identity(self) -> str:
        pass


class TaskIdGeneratorObjectId(TaskIdGeneratorAbstract):
    def next_identity(self) -> str:
        return str(ObjectId())


class TaskRepository(TaskRepositoryAbstract):
    def __init__(self, parameter_storage: ParameterStorageAbstract, status_storage: StatusStorageAbstract,
                 create_task: Callable, clock: ClockAbstract = None,
                 launch_timeout: int = 300, execution_timeout: int = 1800,
                 id_generator: TaskIdGeneratorAbstract = None):
        self._parameter_storage: ParameterStorageAbstract = parameter_storage
        self._status_storage: StatusStorageAbstract = status_storage
        self._clock: ClockAbstract = clock or Clock()
        self._launch_timeout: int = launch_timeout
        self._execution_timeout: int = execution_timeout
        self._id_generator: TaskIdGeneratorAbstract = id_generator or TaskIdGeneratorObjectId()
        self._create_task: Callable = create_task

    def get_task(self, task_type: str, task_id: str) -> TaskAbstract:
        return self._create_task(task_type=task_type, task_id=task_id, repository=self)

    def submit(self, task_type: str, params: Dict) -> TaskAbstract:
        task_id = self._id_generator.next_identity()
        self._parameter_storage.upload(task_type, task_id, params)
        self._status_storage.update_status(task_type, task_id, 'PENDING')
        task: TaskAbstract = self._create_task(task_type=task_type, task_id=task_id, repository=self)
        return task

    def get_status(self, task_type: str, task_id: str) -> str:
        return self._status_storage.get_status(task_type, task_id)

    def fetch_parameters(self, task_type: str, task_id: str) -> Dict:
        return self._parameter_storage.fetch_parameters(task_type, task_id)

    def list_pending_tasks(self) -> List[TaskAbstract]:
        tasks = self._status_storage.list_tasks(status='PENDING')
        for task in tasks:
            task.attach_repository(self)
        return tasks

    def list_launch_timeout_tasks(self) -> List[TaskAbstract]:
        ts = self._clock.get_timestamp() - self._launch_timeout
        tasks = self._status_storage.list_tasks(status='LAUNCHED', launched_timestamp_lt=ts)
        for task in tasks:
            task.attach_repository(self)
        return tasks

    def list_execution_timeout_tasks(self) -> List[TaskAbstract]:
        ts = self._clock.get_timestamp() - self._execution_timeout
        tasks = self._status_storage.list_tasks(status='STARTED', started_timestamp_lt=ts)
        for task in tasks:
            task.attach_repository(self)
        return tasks

    def task_started(self, task_type: str, task_id: str):
        ts = self._clock.get_timestamp()
        self._status_storage.update_status(task_type, task_id, 'STARTED', started_timestamp=ts)

    def task_launched(self, task_type: str, task_id: str, metadata: Dict = None):
        ts = self._clock.get_timestamp()
        self._status_storage.update_status(task_type, task_id, 'LAUNCHED', launched_timestamp=ts, metadata=metadata)

    def task_done(self, task_type: str, task_id: str):
        self._status_storage.update_status(task_type, task_id, 'DONE')

    def task_failed(self, task_type: str, task_id: str):
        self._status_storage.update_status(task_type, task_id, 'FAILED')
