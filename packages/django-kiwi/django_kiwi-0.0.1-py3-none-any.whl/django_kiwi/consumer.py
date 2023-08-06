import json
import traceback

import pika
from django.utils import timezone

from .models import Task
from .settings import get_settings


class Consumer:
    start_message = 'Django Kiwi worker running...'

    def __init__(self):
        self.settings = get_settings()

    def _run(self, data):
        task = Task.objects.create(
            start_time=timezone.now(),
            data=json.dumps(data),
        )
        try:
            self.run(data, task)
            self.handle_success(data, task)
        except Exception:
            self.handle_error(data, task)

    def run(self, data, task):
        raise NotImplementedError

    def handle_error(self, data, task):
        task.end_time = timezone.now()
        task.traceback = traceback.format_exc()
        task.success = False
        task.save()

    def handle_success(self, data, task):
        task.end_time = timezone.now()
        task.success = True
        task.save()

    def callback(self, ch, method, properties, body):
        self._run(self.parser_message(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def parser_message(self, message):
        return json.loads(message.decode('utf-8'))

    def start(self):
        connection = pika.BlockingConnection(
            pika.URLParameters(self.settings['broker_url']))

        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback)

        print(self.start_message)
        channel.start_consuming()

    @property
    def queue(self):
        raise NotImplementedError
