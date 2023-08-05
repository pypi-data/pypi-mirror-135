from vialink.utils.background_task.abstract import TaskAbstract


class TaskLauncher:
    def __init__(self, launch):
        self._launch = launch

    def launch(self, task: TaskAbstract):
        self._launch(task.task_id, task.task_type)
        task.launched()
