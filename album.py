# -*- coding: utf-8 -*-
from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache
from track import Track
from utils import no_timeout


_Album = namedtuple("_Album", ("id", "name", "artist_ids"))


class Album(_Album):
    __slots__ = ()

    _sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials()
    )

    _use_name_for_repr = False  # Use to replace namedtuple's repr with name.

    @Cache(key_func=lambda *args, **kwargs:  # Let kwargs fail in __new__.
           args[1] if len(args) == 2 else args[1:])
    def __new__(cls, album_id, *args):
        if not args:
            if isinstance(album_id, Album):
                return album_id  # Album(Album(x)) == Album(x)

            album = cls.full_response(album_id)

            return super().__new__(cls,
                                   album_id,
                                   album["name"],
                                   tuple(artist["id"]
                                         for artist in album["artists"])
                                   )

        return super().__new__(cls, album_id, *args)

    @classmethod
    def clear(cls):
        cls.__new__.clear()

    @classmethod
    @no_timeout
    @Cache()
    def full_response(cls, album_id):
        return cls._sp.album(album_id if not isinstance(album_id, Album)
                             else album_id.id)

    def release_date(self):
        return self.full_response(self)["release_date"]

    @Cache()
    def tracks(self):
        return [Track(item["id"])
                for item in self.full_response(self)["tracks"]["items"]]

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name < str(other)

    def __repr__(self):
        return self.name if self._use_name_for_repr else super().__repr__()

    def __str__(self):
        return self.name


if __name__ == "__main__":
    albums = [
        Album("2w1YJXWMIco6EBf0CovvVN"),
        Album("id", "name", "artist_ids")
    ]

    tracks = albums[0].tracks()
