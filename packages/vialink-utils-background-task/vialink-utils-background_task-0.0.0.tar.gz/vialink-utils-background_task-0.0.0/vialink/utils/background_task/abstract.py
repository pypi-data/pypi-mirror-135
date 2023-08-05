from abc import ABC, abstractmethod
from typing import Dict, List


class TaskAbstract(ABC):
    @property
    @abstractmethod
    def task_id(self) -> str:
        pass

    @property
    @abstractmethod
    def task_type(self) -> str:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

    @abstractmethod
    def get_parameters(self) -> Dict:
        pass

    @abstractmethod
    def launched(self, metadata: Dict = None):
        pass

    @abstractmethod
    def started(self):
        pass

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def failed(self):
        pass

    @abstractmethod
    def attach_repository(self, repository: 'TaskRepositoryAbstract'):
        pass


class ParameterStorageAbstract(ABC):
    @abstractmethod
    def upload(self, task_type: str, task_id: str, params: Dict):
        pass

    @abstractmethod
    def fetch_parameters(self, task_type: str, task_id: str) -> Dict:
        pass


class StatusStorageAbstract(ABC):
    @abstractmethod
    def get_status(self, task_type: str, task_id: str) -> str:
        pass

    @abstractmethod
    def list_tasks(self, status=None, started_timestamp_lt=None, launched_timestamp_lt=None) -> List[TaskAbstract]:
        pass

    @abstractmethod
    def update_status(self, task_type: str, task_id: str, status: str, *,
                      launched_timestamp: float = None, started_timestamp: float = None, metadata: Dict = None):
        pass


class TaskRepositoryAbstract(ABC):
    @abstractmethod
    def get_task(self, task_type: str, task_id: str) -> TaskAbstract:
        pass

    @abstractmethod
    def get_status(self, task_type: str, task_id: str) -> str:
        pass

    @abstractmethod
    def fetch_parameters(self, task_type: str, task_id: str) -> Dict:
        pass

    @abstractmethod
    def task_started(self, task_type: str, task_id: str):
        pass

    @abstractmethod
    def task_launched(self, task_type: str, task_id: str, metadata: Dict = None):
        pass

    @abstractmethod
    def task_done(self, task_type: str, task_id: str):
        pass

    @abstractmethod
    def task_failed(self, task_type: str, task_id: str):
        pass


class ClockAbstract(ABC):
    @abstractmethod
    def get_timestamp(self) -> float:
        pass
