# -*- coding: utf-8 -*-
from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


_Artist = namedtuple("_Artist", ("id", "name", "genres", "popularity"))


class Artist(_Artist):
    __slots__ = ()

    @Cache()
    def __new__(cls, artist_id):
        if isinstance(artist_id, Artist):
            return artist_id  # Artist(Artist(x)) == Artist(x)

        artist = sp.artist(artist_id)

        return super().__new__(cls,
                               artist_id,
                               artist["name"],
                               tuple(sorted(artist["genres"])),
                               artist["popularity"])

    @Cache()
    def related(self):
        return set(Artist(a["id"])
                   for a in sp.artist_related_artists(self.id)["artists"])

    def __eq__(self, other):
        return (hash(self) == hash(other))

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return (self.name < str(other))

    def __str__(self):
        return self.name


def get_artist(artist_id):
    return Artist(artist_id)


def get_artist_name(artist_id):
    return Artist(artist_id).name


def get_genres(artist_id):
    return Artist(artist_id).genres


def get_related(artist_id):
    return Artist(artist_id).related()


def plt_safe(string):
    return string.replace(r"$", r"\$")
