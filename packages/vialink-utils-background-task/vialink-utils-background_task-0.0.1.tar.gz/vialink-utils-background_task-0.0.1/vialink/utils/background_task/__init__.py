from .factory.repository import get_task_repository
from .executor import TaskExecutor

task_repository = get_task_repository()
