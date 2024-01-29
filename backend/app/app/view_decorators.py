
import inspect
import json
from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest, JsonResponse

from .logging import log, logger


def unpack_to_dict(request: HttpRequest, view_func: Callable, target: dict[str, Any]):
    sig = inspect.signature(view_func)

    if 'user' in sig.parameters:
        target['user'] = request.user
    if 'request' in sig.parameters:
        target['request'] = request

    # Always include query parameters from request.GET
    target.update(request.GET.dict())

    # Unpack request based on content type
    if request.content_type in ['application/x-www-form-urlencoded', 'multipart/form-data']:
        target.update(request.POST.dict())
    elif request.content_type == 'application/json':
        data_dict = json.loads(request.body)
        target.update(data_dict)

    # Add files, if any, under respective keys
    if request.FILES:
        target.update(request.FILES.dict())

def unpack_request(view_func):
    """
    A decorator for Django views that automatically unpacks parameters from the HttpRequest object.

    It extracts query parameters and body contents (whether url-encoded or JSON) and passes them as keyword arguments to the view function.
    The 'request' and 'request.user' objects are also included in the kwargs for convenience as 'request' and 'user' respectively.
    """

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):

        unpack_to_dict(request, view_func, kwargs)
        logger.debug('Unpacked request: {}, {}, {}'.format(
            # view_self, request, rest, kwargs
            request, args, kwargs
        ))

        logger.debug('Unpacked request: {}, {}, {}'.format(
            # view_self, request, rest, kwargs
            request, args, kwargs
        ))

        logger.debug('Unpacked request: {}, {}, {}'.format(
            # view_self, request, rest, kwargs
            request, args, kwargs
        ))

        # Remove keyword arguments that are not in the function signature (unless they are 'kwargs')
        sig = inspect.signature(view_func)
        logger.debug('Function signature: {}, kwargs: {}'.format(sig, kwargs))
        if not sig.parameters.get('kwargs'):
            for key in kwargs.copy():
                if key not in sig.parameters:
                    logger.debug('Removing key: {}'.format(key))
                    del kwargs[key]
        logger.debug('Updated kwargs: {}'.format(kwargs))

        return view_func(*args, **kwargs)

    return wrapper

def add_data_dict(view_func):
    """
    A decorator for Django views that automatically unpacks parameters from the HttpRequest object and adds them to the request object as 'data_dict'.
    """

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        data_dict = kwargs.copy()
        unpack_to_dict(request, view_func, data_dict)
        kwargs['data_dict'] = data_dict
        return view_func(request, *args, **kwargs)

    return wrapper

def return_json(view_func):
    """
    A decorator for Django views that automatically returns a 200/204 (depending on whether the function returns a value) response.
    """

    @wraps(view_func)
    # @log
    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)
        return JsonResponse(response, safe=False, status=200 if response else 204)

    return wrapper

def json_endpoint(view_func):
    """
    A decorator for Django class-based views that combines the effect of @staticmethod, @unpack_request and @return_json.
    """
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        return return_json(unpack_request(view_func))(request, *args, **kwargs)

    return wrapper
