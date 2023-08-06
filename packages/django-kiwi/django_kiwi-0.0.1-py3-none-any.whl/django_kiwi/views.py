from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django_kiwi.producer import call_task


class SampleTask(View):
    def get(self, request):
        call_task(
            'sample-task',
            {
                'a': 1,
                'b': 2,
            },
        )
        return HttpResponse('Called')
