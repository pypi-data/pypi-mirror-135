from django.contrib import admin

from django_kiwi.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'success',
        'start_time',
        'end_time',
    ]

    readonly_fields = [
        'id',
        'name',
        'success',
        'start_time',
        'end_time',
        'data',
        'traceback',
    ]
