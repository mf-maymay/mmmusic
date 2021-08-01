# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from cache import Cache


def _cache_key(cls, id=None, *, info=None):
    if isinstance(id, cls):
        return cls, id
    if info is None:
        return cls, id
    return cls, info["id"]


class SpotifyObjectBase:
    FIELDS: tuple

    _sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())  # XXX

    use_name_for_repr = False  # Use to replace default repr with name.

    def __init__(self, id=None, *, info=None):
        self.info = info if info else self.full_response(id)
        self.id = self.info["id"]
        self.name = self.info["name"]

    @Cache(key_func=_cache_key)
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
