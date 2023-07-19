from datetime import datetime, timedelta
import os
import shelve
from typing import Any

import cachetools


def _get_key_for_shelve(key_for_cache: Any) -> str:
    return str(key_for_cache)


class ShelveCache(cachetools.Cache):
    # TODO: Consider inheriting from a Cache subclass.

    _path_to_shelf = ".shelf/"
    _shelf_life = timedelta(days=30)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        os.makedirs(self._path_to_shelf, exist_ok=True)

    def __setitem__(self, key: Any, value: Any):
        shelve_key = _get_key_for_shelve(key)

        item_to_shelve = {
            "item": value,
            "expires_at": (datetime.now() + self._shelf_life).isoformat(),
        }

        # store item in shelf
        with shelve.open(self._path_to_shelf) as shelf:
            shelf[shelve_key] = item_to_shelve

        super().__setitem__(key, value)

    def __missing__(self, key: str) -> str:
        shelve_key = _get_key_for_shelve(key)

        with shelve.open(self._path_to_shelf) as shelf:
            # Check shelf, raising KeyError if it's not in the shelf.
            shelved_item = shelf[shelve_key]

            # Delete item from shelf and raise KeyError if shelved item as expired.
            if datetime.fromisoformat(shelved_item["expires_at"]) <= datetime.now():
                del shelf[shelve_key]
                raise KeyError

        return shelved_item["item"]


# XXX: shelve is not thread safe, but cachetools.cached can be made to use a lock.

# Set up cache to hold up to 20k items.
# TODO: Change size handling,
_shelf_cache = ShelveCache(maxsize=20_000, getsizeof=lambda *args, **kwargs: 1)

# TODO: Use lock.
cache_with_shelve = cachetools.cached(cache=_shelf_cache, lock=None)
