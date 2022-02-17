# -*- coding: utf-8 -*-
from dataclasses import dataclass
from functools import lru_cache

import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from music_tools.utils import no_timeout

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)


@dataclass(init=False, order=True, frozen=True)  # TODO: add slots=True
class Artist:
    __slots__ = ("name", "id", "genres", "popularity")

    name: str
    id: str
    genres: tuple
    popularity: int

    get_json = lru_cache(maxsize=None)(no_timeout(sp.artist))

    def __init__(self, artist_id):
        if hasattr(artist_id, "id"):
            # Artist(Artist(artist_id)) == Artist(artist_id)
            artist_id = artist_id.id
        super().__setattr__("id", artist_id)

        info = type(self).get_json(artist_id)

        super().__setattr__("name", info["name"])
        super().__setattr__("genres", tuple(sorted(info["genres"])))
        super().__setattr__("popularity", info["popularity"])

    def __str__(self):
        return self.name

    def related(self):
        return RelatedArtists(self)


@dataclass(init=False, frozen=True)  # TODO: add slots=True
class RelatedArtists:
    __slots__ = ("id", "artists")

    id: str
    artists: tuple

    get_json = lru_cache(maxsize=None)(no_timeout(sp.artist_related_artists))

    def __init__(self, artist_id):
        if hasattr(artist_id, "id"):
            # RelatedArtists(Artist(artist_id)) == RelatedArtists(artist_id)
            artist_id = artist_id.id
        super().__setattr__("id", artist_id)

        info = type(self).get_json(artist_id)

        super().__setattr__(
            "artists", tuple(Artist(artist["id"]) for artist in info["artists"])
        )

    def __iter__(self):
        return iter(self.artists)


def search_for_artist(search_text):
    try:
        return Artist(search_text)
    except SpotifyException:
        search = no_timeout(sp.search)  # TODO: declare globally
        search_result = search(search_text, limit=1, type="artist")
        return Artist(search_result["artists"]["items"][0]["id"])


if __name__ == "__main__":
    artist = Artist("0oSGxfWSnnOXhD2fKuz2Gy")
    related = artist.related()
