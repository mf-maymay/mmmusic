# -*- coding: utf-8 -*-
from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache
from utils import no_timeout


_Track = namedtuple("_Track", ("id", "name", "album_id", "artist_ids"))


class Track(_Track):
    __slots__ = ()

    _sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials()
    )

    _use_name_for_repr = False  # Use to replace namedtuple's repr with name.

    @Cache(key_func=lambda *args, **kwargs:  # Let kwargs fail in __new__.
           args[1] if len(args) == 2 else args[1:])
    def __new__(cls, track_id, *args):
        if not args:
            if isinstance(track_id, Track):
                return track_id  # Track(Track(x)) == Track(x)

            track = cls._sp.track(track_id)

            return super().__new__(cls,
                                   track_id,
                                   track["name"],
                                   track["album"]["id"],
                                   tuple(artist["id"]
                                         for artist in track["artists"])
                                   )

        return super().__new__(cls, track_id, *args)

    @classmethod
    def clear(cls):
        cls.__new__.clear()

    @no_timeout
    @Cache()
    def audio_features(self):
        return self._sp.audio_features(self.id)[0]

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
    tracks = [
        Track("0vFabeTqtOtj918sjc5vYo"),
        Track("id", "name", "album_id", "artist_ids")
    ]
