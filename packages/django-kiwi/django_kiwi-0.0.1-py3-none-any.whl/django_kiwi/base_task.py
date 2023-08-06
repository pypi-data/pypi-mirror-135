import json

from django.apps import apps
from django.utils import timezone

from .consumer import Consumer
from .models import Task
from .producer import Producer
from .utils.packages import get_class_from_package


class BaseTask(Consumer):
    @property
    def name(self):
        raise NotImplementedError

    @property
    def queue(self):
        module_name = self.settings['module_name']
        queue_prefix = self.settings['queue_prefix']
        return f'{queue_prefix}-{module_name}'

    def get_task(self, task_name, raise_exception=True):
        for app in apps.get_app_configs():
            try:
                package_name = f'{app.module.__package__}.tasks'
                task_class = get_class_from_package(
                    package_name, lambda x: getattr(x, 'name', '') == task_name)

                if task_class:
                    return task_class

            except (ModuleNotFoundError, AttributeError):
                pass

        if raise_exception:
            raise ValueError('Task not found')

        return None

    def _run(self, payload):
        task_name = payload['task_name']
        data = payload['data']

        task = Task.objects.create(
            start_time=timezone.now(),
            name=task_name,
            data=json.dumps(data),
        )

        try:
            self.run(data, task)
            self.handle_success(data, task)
        except Exception:
            self.handle_error(data, task)

    def run(self, data, task):
        task_class = self.get_task(task.name)
        task_class().run(data, task)
