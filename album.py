# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache
from track import Track
from utils import no_timeout


ALBUM_FIELDS = ("id", "name", "artist_ids")


def _album_cache_key_func(cls, album_id=None, *, info=None):
    if isinstance(album_id, cls):
        return album_id.id
    if info is None:
        return album_id
    return info["id"]


class Album(object):
    __slots__ = (*ALBUM_FIELDS, "info")

    _sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials()
    )

    _use_name_for_repr = False  # Use to replace default repr with name.

    def __init__(self, album_id=None, *, info=None):
        self.info = info if info else self.full_response(album_id)

        self.id = self.info["id"]

        self.name = self.info["name"]

        self.artist_ids = tuple(
            artist["id"] for artist in self.info["artists"]
        )

    @Cache(key_func=_album_cache_key_func)
    def __new__(cls, album_id=None, *, info=None):  # TODO: kwargs
        if album_id is None and info is None:
            raise ValueError("Must supply either album_id or info")
        return super().__new__(cls)

    @classmethod
    @no_timeout
    def full_response(cls, album_id):
        return cls._sp.album(
            album_id if not isinstance(album_id, cls) else album_id.id
        )

    @Cache()
    def tracks(self):
        return [
            Track(info={**item, "album": self.info})
            for item in self.info["tracks"]["items"]
        ]

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name < str(other)

    def __repr__(self):
        return (
            self.name if self._use_name_for_repr
            else "Album({})".format(
                ", ".join(
                    "{}={}".format(field, repr(getattr(self, field)))
                    for field in ALBUM_FIELDS
                )
            )
        )

    def __str__(self):
        return self.name


if __name__ == "__main__":
    album = Album("2w1YJXWMIco6EBf0CovvVN")

    tracks = album.tracks()
