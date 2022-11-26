# -*- coding: utf-8 -*-
from datetime import date
from functools import lru_cache

from pydantic import BaseModel, validator
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lib.models.track import Track
from lib.utils import no_timeout

AlbumID = str

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)
_get_album_json = lru_cache(maxsize=None)(no_timeout(sp.album))
_get_album_tracks_json = lru_cache(maxsize=None)(no_timeout(sp.album_tracks))


class Album(BaseModel):
    name: str
    id: str
    album_type: str
    release_date: date
    artist_ids: tuple[str, ...]

    @validator("release_date", pre=True)
    def coerce_to_full_date(cls, value):
        if not isinstance(value, str):
            return value

        fields = value.split("-")

        if (num_fields := len(fields)) in {1, 2}:
            return "-".join(fields + ["1"] * (3 - num_fields))

        return value

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        return self.name


def get_album(album_id: AlbumID | Album) -> Album:
    if isinstance(album_id, Album):
        return album_id

    album_json = _get_album_json(album_id)
    artist_ids = tuple(artist["id"] for artist in album_json["artists"])

    return Album.parse_obj({**album_json, "artist_ids": artist_ids})


def get_album_tracks(album: Album | AlbumID) -> list[Track]:
    album = get_album(album)

    tracks: list[Track] = []

    album_tracks_json = _get_album_tracks_json(album.id)

    while album_tracks_json is not None and (items := album_tracks_json["items"]):
        tracks.extend(Track(item["id"]) for item in items)

        album_tracks_json = no_timeout(sp.next)(album_tracks_json)

    return tracks


def get_tracks_from_albums(albums: list[Album | AlbumID]) -> tuple[Track, ...]:
    return tuple(track for album in albums for track in get_album_tracks(album))


if __name__ == "__main__":
    album_id = "5Tw0sanofDSd7h44GySmoa"

    album = get_album(album_id)

    tracks = get_album_tracks(album_id)

    assert len(tracks) > 50
