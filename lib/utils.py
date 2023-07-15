from contextlib import contextmanager
from datetime import datetime as dt
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


@contextmanager
def time_and_note_when_done(message: str):
    print(message)
    start = dt.now()
    yield
    total_secs = (dt.now() - start).total_seconds()
    total_mins, secs = divmod(int(total_secs), 60)
    hours, mins = divmod(total_mins, 60)
    print(
        f"\x1b[1;32;20mDone.\033[0m"
        f" (\x1b[33;20mTook {hours}h {mins}m {secs}s.\033[0m)"
    )
