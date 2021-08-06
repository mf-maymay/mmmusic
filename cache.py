# -*- coding: utf-8 -*-
from functools import wraps
import types


def default_key(*args, **kwargs):
    return (tuple(args) + tuple(sorted(kwargs.items())))


class Cache:
    def __init__(self, func):
        self.dict = {}
        self.key_func = default_key
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        key = self.key_func(*args, **kwargs)
        if key not in self.dict:
            self.dict[key] = self.__wrapped__(*args, **kwargs)
        return self.dict[key]

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    @classmethod
    def with_key_func(cls, key_func):
        def wrapped(func):
            instance = cls(func)
            instance.key_func = key_func
            return instance
        return wrapped


if __name__ == "__main__":
    @Cache
    def add(x, y):
        """Add x and y."""
        return x + y

    @Cache.with_key_func(lambda x, y: f"{x} - {y}")
    def sub(x, y):
        """subtraction"""
        return x - y

    class Test(object):
        def __init__(self, name):
            self.name = name

        @Cache
        def div(self, a, b):
            return a / b

        def __repr__(self):
            return f"Test({self.name!r})"
