import uuid

from django.db import models


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200, null=True)
    success = models.BooleanField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    data = models.TextField(null=True)
    traceback = models.TextField(null=True)

    def __str__(self):
        return f'Task: {self.id} - {self.name}'

    class Meta:
        ordering = ('-start_time',)
