# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic import BaseModel
from requests.exceptions import HTTPError
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from lib.utils import no_timeout

ArtistID = str

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)
_get_artist_json = lru_cache(maxsize=None)(no_timeout(sp.artist))
_get_related_artists_json = lru_cache(maxsize=None)(
    no_timeout(sp.artist_related_artists)
)


class Artist(BaseModel):
    name: str
    id: str
    genres: tuple[str, ...]
    popularity: int

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        return self.name


def get_artist(artist_id: ArtistID | Artist) -> Artist:
    if isinstance(artist_id, Artist):
        return artist_id

    artist_json = _get_artist_json(artist_id)

    return Artist.parse_obj(artist_json)


def get_related_artists(artist: ArtistID | Artist) -> tuple[Artist, ...]:
    if isinstance(artist, Artist):
        artist = artist.id

    related_artists_json = _get_related_artists_json(artist)

    return tuple(get_artist(artist["id"]) for artist in related_artists_json["artists"])


def search_for_artist(search_text: str) -> Artist:
    try:
        return get_artist(search_text)
    except (HTTPError, SpotifyException):
        search = no_timeout(sp.search)
        search_result = search(search_text, limit=1, type="artist")
        return get_artist(search_result["artists"]["items"][0]["id"])


if __name__ == "__main__":
    artist = get_artist("0oSGxfWSnnOXhD2fKuz2Gy")

    related = get_related_artists(artist)

    tool = search_for_artist("tool")
