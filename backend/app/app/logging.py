import logging
from typing import Literal


logger = logging.getLogger(__name__)

def log(func):
    def wrapper(*args, **kwargs):
        logger.debug(f'Logger: Calling {func.__name__} with args: {args}, kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logger.debug(f'Logger: Result for {func.__name__}: {result}')
        return result
    return wrapper


def log_in(
    color: Literal['green', 'red', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'gray'],
    *args, **kwargs
):
    color_map = dict(
        gray=90,
        red=91,
        green=92,
        yellow=93,
        blue=94,
        magenta=95,
        cyan=96,
        white=97,
    )
    # logger.info('\033[{}m'.format(color_map[color]), *args, '\033[0m', **kwargs)
    print('\033[{}m'.format(color_map[color]), *args, '\033[0m', **kwargs)


def log_red(*args, **kwargs):
    log_in('red', *args, **kwargs)


def log_green(*args, **kwargs):
    log_in('green', *args, **kwargs)


def log_yellow(*args, **kwargs):
    log_in('yellow', *args, **kwargs)


def log_cyan(*args, **kwargs):
    log_in('cyan', *args, **kwargs)
