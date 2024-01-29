from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Task
from app.view_decorators import unpack_request
from app.logging import logger
import time

def index_view(request):
    return HttpResponse("you shouldn't really be here...")

def long_task(query):
    logger.debug('long task called with query: {}'.format(query))
    time.sleep(3)
    return {
        "message": "long task finished: " + str(query)
    }

@csrf_exempt
@unpack_request
def task_test_view(query: str):
    task = Task.start_task(long_task, query)
    return task.initial_json_response()

@csrf_exempt
@unpack_request
def data_test_view(request):
    logger.info(request)
    return JsonResponse({
        "result": {
            "message": "ohoho server data!"
        }
    })
