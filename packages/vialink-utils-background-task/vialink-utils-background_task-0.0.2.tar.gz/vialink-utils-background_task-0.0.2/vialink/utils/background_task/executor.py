from .abstract import TaskAbstract


class TaskExecutor:
    def __init__(self, execute):
        self._execute = execute

    def execute(self, task: TaskAbstract):
        params = task.get_parameters()
        task.started()
        try:
            self._execute(params)
        except BaseException as e:
            task.failed()
            raise e
        else:
            task.done()
