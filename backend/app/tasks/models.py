from functools import wraps
import inspect
import uuid
import json
import os
import signal
import sys
import uuid
from enum import Enum
from typing import (Any, Callable, Generic, List, Literal, Optional, Self, Tuple, Type, TypeVar, Union,
                    cast)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_q.tasks import async_task
from django.utils import timezone
from app.logging import logger
from app.logging import log


# def dummy_report(progress_report: str):
#     pass

Reporter = Callable[[str | None], None]

dummy_report: Reporter = lambda progress_report: None

def q_cluster_is_sync():
    return settings.Q_CLUSTER.get("sync", False)

class TaskStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(key.value, key.name) for key in cls]

def execute_task(
    task: 'Task',
    function: Callable[..., Any],
    *args: Any, **kwargs: Any
):
    task_id = task.id

    # task = Task.objects.get(id=task_id)
    Model = type(task)
    logger.debug("Task model for task {} is {}".format(task_id, Model))
    task = Model.objects.get(id=task_id)

    if not q_cluster_is_sync():
        @log
        def graceful_exit(signum, frame):
            # task = Task.objects.get(id=task_id)
            task = Model.objects.get(id=task_id)
            task.set_status(TaskStatus.STOPPED)
            logger.debug(f"Task {task.id} (PID: {task.pid}) stopped")
            sys.exit(0)

        signal.signal(signal.SIGTERM, graceful_exit)

    task.pid = os.getpid()
    task.func_name = function.__name__
    logger.debug(f"Task {task.id} (PID: {task.pid}, func_name: {task.func_name}) started")
    task.save(update_fields=["pid"])

    try:
        task.input = str({"args": args, "kwargs": kwargs})
        logger.debug(f"Starting task {task.id} (PID: {task.pid}), input: {task.input}")
        if "report" in inspect.signature(function).parameters:
            result = function(*args, report=task.report, **kwargs)
        else:
            result = function(*args, **kwargs)
        task.result_json = json.dumps(result) # output should always be JSON serializable, otherwise we won't be able to return it to the frontend
        task.save(update_fields=["input", "result_json"])
    except Exception as e:
        task.set_status(TaskStatus.FAILED)
        task.exception = str(e)
        task.save(update_fields=["exception"])
        raise e

    task.set_status(TaskStatus.COMPLETED)
    return result

class Task(models.Model):
    id = models.BigAutoField(primary_key=True)

    q_id = models.CharField(max_length=255, unique=False, db_index=True)
    uuid = models.UUIDField(
        null=True, blank=True, unique=True, db_index=True, default=uuid.uuid4, editable=False
    )

    # custom save to ensure unique q_id
    def save(self, *args, **kwargs):
        if self.q_id:
            if Task.objects.filter(q_id=self.q_id).exclude(id=self.id).exists():
                raise ValidationError("A task with this q_id already exists.")
        super(Task, self).save(*args, **kwargs)

    pid = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=TaskStatus.choices(),
        default=TaskStatus.RUNNING.value
    )
    progress_report = models.TextField(null=True, blank=True)
    exception = models.TextField(null=True, blank=True)

    func_name = models.CharField(max_length=255, null=True, blank=True)
    input = models.TextField(null=True, blank=True)
    result_json = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "Task {}: {}".format(
            self.uuid or "Q-{}".format(self.q_id) or self.id,
            self.status
        ) + (
            f" ({self.progress_report})" if self.progress_report else ""
        )

    # @log
    def set_status(self, new_status: TaskStatus):
        self.status = new_status.value
        self.save(update_fields=["status"])
        return self

    def report(self, progress_report: str | None):
        logger.debug("Reporting progress: {} for task {} (task type {})".format(
            progress_report, self, type(self)
        ))
        self.progress_report = progress_report
        self.save()

    @property
    def result(self):
        if self.result_json:
            return json.loads(self.result_json)
        else:
            raise ValueError("Task result not set.")

    @property
    def success(self):
        # Return True if task completed successfully, False if failed or stopped, and None if still running
        if self.status == TaskStatus.COMPLETED.value:
            return True
        elif self.status in [TaskStatus.FAILED.value, TaskStatus.STOPPED.value]:
            return False
        else:
            return None

    @classmethod
    def start_task(cls, function: Callable, *args: Any, **kwargs: Any):
        task = cls.objects.create()
        return task.start(function, *args, **kwargs)

    def start_with_executor(self,
                            execute: Callable[[Self, Callable, Any, Any], Any | None],
                            function: Callable, *args: Any, **kwargs: Any
                            ):
        if q_cluster_is_sync():
            logger.debug("Starting task synchronously")
            execute(self, function, *args, **kwargs)
        else:
            self.q_id = async_task(execute, self, function, *args, **kwargs)
            self.save(update_fields=["q_id"])
        if not self.uuid: raise ValueError("Task UUID not set (this should never happen)")
        return self

    def start(self, function: Callable, *args: Any, **kwargs: Any):
        return self.start_with_executor(execute_task, function, *args, **kwargs)

    def initial_json_response(self, **kwargs):
        return JsonResponse({
            "task_id": self.uuid,
            **kwargs
        }, status=202)

    @classmethod
    def get_task(cls, uuid: str):
        return Task.objects.filter(uuid=uuid).first()

    def stop(self):
        if not self.status == TaskStatus.RUNNING.value:
            logger.debug(f"Task {self.id} (PID: {self.pid}) not running, ignoring")
            return
        if not self.pid:
            raise ValueError("Task PID not set.")
        os.kill(self.pid, signal.SIGTERM)
        logger.debug(f"Stopping task {self.id} (PID: {self.pid})")

    @staticmethod
    def stop_task(q_id: str) -> None:
        task: 'Task' = get_object_or_404(Task, q_id=q_id)
        task.stop()

# Function decorator to run it as a task
def run_as_task(function: Callable[..., Any]):
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any):
        return Task.start_task(function, *args, **kwargs)

    return wrapper
