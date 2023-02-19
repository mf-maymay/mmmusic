from functools import wraps

import requests

from lib.logging import get_logger


def no_timeout(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        logger = get_logger()

        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                logger.warning("ConnectionError on %r. Retrying...", func.__name__)
                continue
            except requests.ReadTimeout:
                logger.warning("ReadTimout on %r. Retrying...", func.__name__)
                continue

    return wrapped


def take_x_at_a_time(items, x):
    sequence = list(items)
    quotient, remainder = divmod(len(sequence), x)
    for i in range(quotient + bool(remainder)):
        yield sequence[i * x : (i + 1) * x]
