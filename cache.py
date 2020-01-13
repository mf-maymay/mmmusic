# -*- coding: utf-8 -*-
from functools import wraps
import types


def default_key(*args, **kwargs):
    return (tuple(args) + tuple(sorted(kwargs.items())))


def Cache(base=dict, *, name=None, key_func=None):  # XXX: check function defs
    if name is None:
        name = base.__name__ + "Cache"

    if key_func is None:
        key_func = default_key

    def init(self, func):  # XXX: use mixin instead?
        wraps(func)(self)
        base.__init__(self)

    def call(self, *args, **kwargs):
        key = key_func(*args, **kwargs)
        if key not in self:
            result = self.__wrapped__(*args, **kwargs)
            self[key] = result
        else:
            result = self[key]
        return result  # indirection for weakref

    def get(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    return type(name, (base,), {"__init__": init,
                                "__call__": call,
                                "__get__": get})


Cache = Cache()(Cache)  # remember created classes (e.g., dictCache)


if __name__ == "__main__":
    from weakref import WeakValueDictionary

    @Cache()
    def add(x, y):
        """Add x and y."""
        return x + y

    @Cache()
    def sub(x, y):
        return x - y

    class Test(object):
        def __init__(self, x, y):
            self.out = x * y

        @Cache()
        def div(self, a, b):
            return a / b

        def __repr__(self):
            return str(self.out)

    @Cache(WeakValueDictionary)
    def mul(x, y):
        return Test(x, y)
