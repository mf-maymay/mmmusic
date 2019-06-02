# -*- coding: utf-8 -*-
import spotipy
from credentials import client_credentials_manager

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Artist(object):
    def __init__(self, artist_id):
        artist = sp.artist(artist_id)

        self._hash = hash(artist_id)

        self.id = artist_id
        self.name = artist["name"]
        self.genres = artist["genres"]
        self.popularity = artist["popularity"]

        self._related = None

    @property
    def related(self):
        if self._related is None:
            related = sp.artist_related_artists(self.id)["artists"]
            self._related = set(get_artist(a["id"]) for a in related)
        return self._related

    def __eq__(self, other):
        return (self._hash == hash(other))

    def __hash__(self):
        return self._hash

    def __lt__(self, other):
        return (self.name < str(other))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Cache(dict):
    def __init__(self, func):
        self.func = func

    def __getitem__(self, item):
        if item not in self:
            self[item] = self.func(item)
        return dict.__getitem__(self, item)

    def __call__(self, item):
        return self[item]

    def get(self, item):
        return self[item]


@Cache
def get_artist(artist_id):
    return Artist(artist_id)


def get_artist_name(artist_id):
    return get_artist(artist_id).name  # XXX: unnecessary


def get_genres(artist_id):
    return get_artist(artist_id).genres  # XXX: unnecessary


def get_related(artist_id):
    return get_artist(artist_id).related  # XXX: unnecessary


def plt_safe(string):
    return string.replace(r"$", r"\$")
