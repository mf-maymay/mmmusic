# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lib.models.track import Track
from lib.utils import no_timeout


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)


@dataclass(init=False, order=True, frozen=True)  # TODO: add slots=True
class Album:
    __slots__ = ("name", "id", "album_type", "release_date", "artist_ids")

    name: str
    id: str
    album_type: str
    release_date: datetime
    artist_ids: tuple  # TODO: switch to "artists", put first in order

    get_json = lru_cache(maxsize=None)(no_timeout(sp.album))

    def __init__(self, album_id):
        if hasattr(album_id, "id"):
            # Album(Album(album_id)) == Album(album_id)
            album_id = album_id.id
        super().__setattr__("id", album_id)

        info = type(self).get_json(album_id)

        super().__setattr__("name", info["name"])
        super().__setattr__("album_type", info["album_type"])
        super().__setattr__(
            "artist_ids", tuple(artist["id"] for artist in info["artists"])
        )

        if info["release_date_precision"] == "day":
            super().__setattr__(
                "release_date", datetime.strptime(info["release_date"], "%Y-%m-%d")
            )
        elif info["release_date_precision"] == "month":
            super().__setattr__(
                "release_date", datetime.strptime(info["release_date"], "%Y-%m")
            )
        elif info["release_date_precision"] == "year":
            super().__setattr__(
                "release_date", datetime.strptime(info["release_date"], "%Y")
            )
        else:
            raise RuntimeError(
                f"Unexpected release_date_precision: {info['release_date_precision']}"
            )

    def __str__(self):
        return self.name

    def tracks(self):
        info = type(self).get_json(self.id)

        tracks = []
        items = info["tracks"]

        while items:
            tracks.extend(Track(item["id"]) for item in items["items"])
            items = no_timeout(sp.next)(items)

        return tracks


def get_tracks_from_albums(albums):
    return tuple(track for album in albums for track in album.tracks())


if __name__ == "__main__":
    album = Album("5Tw0sanofDSd7h44GySmoa")

    tracks = album.tracks()

    assert len(tracks) > 50
