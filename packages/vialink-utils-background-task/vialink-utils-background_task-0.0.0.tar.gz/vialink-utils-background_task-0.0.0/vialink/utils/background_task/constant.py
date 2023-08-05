from enum import Enum


class TaskStatusEnum(str, Enum):
    PENDING: str = 'PENDING'
    STARTED: str = 'STARTED'
    DONE: str = 'DONE'
