from django.core.management.base import BaseCommand
from django_kiwi.base_task import BaseTask


class Command(BaseCommand):
    help = 'Runs worker that consumes from simple queue.'

    def handle(self, *args, **options):
        BaseTask().start()
