# -*- coding: utf-8 -*-
from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


_Album = namedtuple("_Album", ("id", "name", "artist_ids"))


class Album(_Album):
    __slots__ = ()

    @Cache()
    def __new__(cls, *args):
        if len(args) == 1:
            album_id = args[0]

            if isinstance(album_id, Album):
                return album_id  # Album(Album(x)) == Album(x)

            album = sp.album(album_id)

            return super().__new__(cls,
                                   album_id,
                                   album["name"],
                                   tuple(artist["id"]
                                         for artist in album["artists"])
                                   )

        return super().__new__(cls, *args)

    def __eq__(self, other):
        return (hash(self) == hash(other))

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return (self.name < str(other))

    def __str__(self):
        return self.name
