# -*- coding: utf-8 -*-
import spotipy
from credentials import client_credentials_manager

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


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
    return sp.artist(artist_id)


def get_artist_name(artist_id):
    return get_artist(artist_id)["name"]


def get_genres(artist):
    return get_artist(artist)["genres"]


def get_related(artist_id):
    return sp.artist_related_artists(artist_id)["artists"]


def search_artist(name):
    return sp.search("artist:" + name, type="artist")
