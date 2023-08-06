from django.urls import include, path

from . import views

urlpatterns = [
    path('sample_task', views.SampleTask.as_view()),
]
