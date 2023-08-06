from typing import Dict
from .abstract import TaskRepositoryAbstract, TaskAbstract, ClockAbstract
from .clock import Clock


class Task(TaskAbstract):
    def __init__(self, task_type: str, task_id: str, repository: TaskRepositoryAbstract = None,
                 clock: ClockAbstract = None):
        self._task_type = task_type
        self._task_id = task_id
        self._repository = repository
        self._clock = clock or Clock()

    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def task_type(self) -> str:
        return self._task_type

    def get_status(self) -> str:
        return self._repository.get_status(task_type=self._task_type, task_id=self.task_id)

    def get_parameters(self) -> Dict:
        return self._repository.fetch_parameters(self.task_type, self.task_id)

    def launched(self, metadata: Dict = None):
        self._repository.task_launched(self.task_type, self.task_id, metadata=metadata)

    def started(self):
        self._repository.task_started(self.task_type, self.task_id)

    def done(self):
        self._repository.task_done(self.task_type, self.task_id)

    def failed(self):
        self._repository.task_done(self.task_type, self.task_id)

    def attach_repository(self, repository: TaskRepositoryAbstract):
        self._repository = repository
