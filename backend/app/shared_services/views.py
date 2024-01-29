from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django_q.tasks import result as get_result, fetch
from django.views.decorators.csrf import csrf_exempt
from app.logging import logger

from django.http import Http404, JsonResponse
from django_q.tasks import Task as QTask
from django.core.exceptions import ObjectDoesNotExist

import time
from app.view_decorators import unpack_request

from tasks.models import Task, TaskStatus

@unpack_request
@csrf_exempt
def check_task_view(request, task_id: str):

    task = fetch(task_id) or Task.get_task(task_id)
    logger.debug('Task for task_id {} is {}'.format(task_id, task))

    if not task:
        raise Http404('Task not found')

    if task:
        if task.success:
            logger.debug('Task completed')
            result = task.result
            logger.debug('Result for task_id {} is {}'.format(task_id, result))

            return JsonResponse(dict(
                result=result,
                completed=True,
                code=200,
                message='Task completed successfully',
            ), status=200)

        elif task.success == False:
            if isinstance(task, Task):
                raise Exception('Task failed: {}'.format(task.exception))
            else:
                raise Exception('Task failed: {}'.format(task.result))

    return JsonResponse(dict(
        completed=False,
        code=100,
        message='Task in progress',
    ), status=202)
