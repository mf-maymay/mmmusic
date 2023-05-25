from functools import cache

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lib.utils import no_timeout


@cache
def get_client_credentials_managed_client() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)


_get_album = no_timeout(get_client_credentials_managed_client().album)
_get_album_tracks = no_timeout(get_client_credentials_managed_client().album_tracks)
_get_artist = no_timeout(get_client_credentials_managed_client().artist)
_get_artist_related_artists = no_timeout(
    get_client_credentials_managed_client().artist_related_artists
)
_get_track = no_timeout(get_client_credentials_managed_client().track)
_get_track_audio_features = no_timeout(
    get_client_credentials_managed_client().audio_features
)
_next = no_timeout(get_client_credentials_managed_client().next)
_search = no_timeout(get_client_credentials_managed_client().search)


def get_album(album_id: str) -> dict:
    return _get_album(album_id)


def get_album_tracks(album_id: str) -> list[dict]:
    tracks = []

    response = _get_album_tracks(album_id)

    while response is not None and (items := response["items"]):
        tracks.extend(items)

        response = _next(response)

    return tracks


def get_artist(artist_id: str) -> dict:
    return _get_artist(artist_id)


def get_artist_related_artists(artist_id: str) -> list[dict]:
    return _get_artist_related_artists(artist_id)["artists"]


def get_track(track_id: str) -> dict:
    return _get_track(track_id)


def get_track_audio_features(track_id: str) -> dict:
    return _get_track_audio_features(track_id)[0]


def search_for_artist(search_text: str) -> dict:
    return _search(search_text, limit=1, type="artist")["artists"]["items"][0]
