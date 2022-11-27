from functools import cache

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lib.utils import no_timeout

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)

_get_album = no_timeout(sp.album)
_get_album_tracks = no_timeout(sp.album_tracks)
_next = no_timeout(sp.next)


@cache
def get_album(album_id: str) -> dict:
    return _get_album(album_id)


@cache
def get_album_tracks(album_id: str) -> list[dict]:
    tracks = []

    response = _get_album_tracks(album_id)

    while response is not None and (items := response["items"]):
        tracks.extend(items)

        response = _next(response)

    return tracks
