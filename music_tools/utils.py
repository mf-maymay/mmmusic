# -*- coding: utf-8 -*-
from functools import wraps

import requests


def no_timeout(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                print(f"ConnectionError on {func.__name__}. Retrying...")
                continue
            except requests.ReadTimeout:
                print(f"ReadTimout on {func.__name__}. Retrying...")
                continue

    return wrapped


def record_calls(func):  # TODO: delete?
    @wraps(func)
    def wrapped(*args, **kwargs):
        args_list = ", ".join(
            [repr(arg) for arg in args]
            + [f"{kw}={repr(arg)}" for kw, arg in kwargs.items()]
        )
        print(f"{func.__name__}({args_list})")
        return func(*args, **kwargs)

    return wrapped


def take_x_at_a_time(sequence, x):
    quotient, remainder = divmod(len(sequence), x)
    for i in range(quotient + bool(remainder)):
        yield sequence[i * x : (i + 1) * x]
