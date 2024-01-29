from django.urls import path

from . import views


urlpatterns = [
    path('check_task', views.check_task_view, name='check_task_view'),
]
