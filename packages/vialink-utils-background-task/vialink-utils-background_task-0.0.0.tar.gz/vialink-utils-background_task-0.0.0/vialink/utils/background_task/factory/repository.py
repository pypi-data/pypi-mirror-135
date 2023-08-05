from vialink.utils.background_task.repository import TaskRepository
from vialink.utils.background_task.task import Task

from .parameter_storage import get_parameter_storage
from .status_storage import get_status_storage


def get_task_repository():
    status_storage = get_status_storage()
    parameter_storage = get_parameter_storage()
    repository = TaskRepository(parameter_storage=parameter_storage, status_storage=status_storage, create_task=Task,
                                launch_timeout=300, execution_timeout=1800)
    return repository
