import json

import pika

from .settings import get_settings


class Producer:
    def __init__(self, destination_queue=False):
        self.settings = get_settings()

        if destination_queue:
            self.queue = destination_queue

        connection = pika.BlockingConnection(
            pika.URLParameters(self.settings['broker_url']))
        self.channel = connection.channel()
        self.channel.queue_declare(self.queue, durable=True)

    def send_message(self, data):
        message = self.parser_data(data)
        self.channel.basic_publish(exchange='',
                            routing_key=self.queue,
                            body=message,
                            properties=pika.BasicProperties(
                            delivery_mode = 2
                        ))
        print(" [x] Sent %r" % message)

    def parser_data(self, data):
        return json.dumps(data)

def call_task(task_name, data, module_name=False):
    settings = get_settings()
    queue_prefix = settings['queue_prefix']

    if not module_name:
        module_name = settings['module_name']

    Producer(destination_queue=f'{queue_prefix}-{module_name}').send_message(
        {
            'task_name': task_name,
            'data': data
        },
    )
