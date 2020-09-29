# -*- coding: utf-8 -*-
from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache


_Artist = namedtuple("_Artist", ("id", "name", "genres", "popularity"))


class Artist(_Artist):
    __slots__ = ()

    _sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials()
    )

    _use_name_for_repr = False  # Use to replace namedtuple's repr with name.

    @Cache(key_func=lambda *args, **kwargs:  # Let kwargs fail in __new__.
           args[1] if len(args) == 2 else args[1:])
    def __new__(cls, artist_id, *args):
        if not args:
            if isinstance(artist_id, Artist):
                return artist_id  # Artist(Artist(x)) == Artist(x)

            artist = cls._sp.artist(artist_id)

            return super().__new__(cls,
                                   artist_id,
                                   artist["name"],
                                   tuple(sorted(artist["genres"])),
                                   artist["popularity"])

        return super().__new__(cls, artist_id, *args)

    @Cache()
    def related(self):
        return set(Artist(a["id"])
                   for a in self._sp.artist_related_artists(self.id)["artists"]
                   )

    @classmethod
    def clear(cls):
        cls.__new__.clear()

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
    artists = [
        Artist("0oSGxfWSnnOXhD2fKuz2Gy"),  # David Bowie
        Artist("id", "name", "genres", "popularity")
    ]
