from django_kiwi.base_task import BaseTask


class SampleTask(BaseTask):
    name = 'sample-task'

    def run(self, data, task):
        print(f'Task Name: {task.name}')
        print(f'Task Data: {data}')
