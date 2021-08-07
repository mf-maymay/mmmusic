# -*- coding: utf-8 -*-
import atexit
import shelve

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from cache import Cache

_SHELVE_NAME = "shelf"


def _cache_key(cls, id=None, *, info=None):
    if isinstance(id, cls):
        return cls, id
    if info is None:
        return cls, id
    return cls, info["id"]


def _shelve_key(cls, id=None, *, info=None):
    cls, id = _cache_key(cls, id=id, info=info)
    return f"{cls.__name__}-{id}"


def _from_shelve(func):
    def wrapped(cls, id=None, *, info=None):
        key = _shelve_key(cls, id=id, info=info)
        with shelve.open(_SHELVE_NAME) as shelf:
            if key in shelf:
                return func(cls, info=shelf[key])
        return func(cls, id=id, info=info)
    return wrapped


class SpotifyObjectBase:
    FIELDS: tuple

    _sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())  # XXX

    use_name_for_repr = False  # Use to replace default repr with name.

    def __init__(self, id=None, *, info=None):
        self.info = info if info else self.full_response(id)
        self.id = self.info["id"]
        self.name = self.info["name"]

    @Cache.with_key_func(_cache_key)
    @_from_shelve
    def __new__(cls, id=None, *, info=None):  # TODO: kwargs
        if id is None and info is None:
            raise ValueError("Must supply either id or info")
        return super().__new__(cls)

    @classmethod
    def full_response(cls, id):
        raise NotImplementedError

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __getitem__(self, key):
        return self.info[key]

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name < str(other)

    def __repr__(self):
        return (
            self.name
            if self.use_name_for_repr
            else "{}({})".format(
                type(self).__name__,
                ", ".join(
                    "{}={}".format(field, repr(getattr(self, field)))
                    for field in self.FIELDS
                ),
            )
        )

    def __str__(self):
        return self.name


@atexit.register
def shelve_spotify_objects():
    with shelve.open(_SHELVE_NAME) as shelf:
        for (cls, id), spotify_object in SpotifyObjectBase.__new__.dict.items():
            key = f"{cls.__name__}-{id}"
            if key not in shelf:
                shelf[key] = spotify_object.info
