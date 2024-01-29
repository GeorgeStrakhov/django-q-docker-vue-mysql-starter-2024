from django.contrib import admin

from .models import Task
from django_q.tasks import Task as QTask

admin.site.register(Task)
admin.site.register(QTask)
