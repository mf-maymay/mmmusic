# -*- coding: utf-8 -*-
from pydantic import BaseModel
from requests.exceptions import HTTPError
from spotipy.exceptions import SpotifyException

from lib.models import spotify

ArtistID = str


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

    artist_json = spotify.get_artist(artist_id)

    return Artist.parse_obj(artist_json)


def get_related_artists(artist: ArtistID | Artist) -> tuple[Artist, ...]:
    if isinstance(artist, Artist):
        artist = artist.id

    related_artists_json = spotify.get_artist_related_artists(artist)

    return tuple(get_artist(artist["id"]) for artist in related_artists_json)


def search_for_artist(search_text: str) -> Artist:
    try:
        return get_artist(search_text)
    except (HTTPError, SpotifyException):
        search_result = spotify.search_for_artist(search_text)
        return get_artist(search_result["id"])


if __name__ == "__main__":
    artist = get_artist("0oSGxfWSnnOXhD2fKuz2Gy")

    related = get_related_artists(artist)

    tool = search_for_artist("tool")
