from functools import cache

import requests
import requests.adapters
import spotipy
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials
import urllib3

from mmmusic.log_utils import get_logger

logger = get_logger()


def create_requests_session_for_spotify() -> requests.Session:
    retry = urllib3.Retry(
        total=10,
        connect=5,
        read=5,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE"]),
        status=5,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
    )

    adapter = requests.adapters.HTTPAdapter(max_retries=retry)

    session = requests.Session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


@cache
def get_client_credentials_managed_client() -> spotipy.Spotify:
    # NOTE: This is not thread safe.
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            cache_handler=CacheFileHandler(
                cache_path=".cache-client-credentials-token-info"
            )
        ),
        requests_session=create_requests_session_for_spotify(),
    )


@cache
def get_album(album_id: str) -> dict:
    _get_album = get_client_credentials_managed_client().album
    return _get_album(album_id)


@cache
def get_album_tracks(album_id: str) -> list[dict]:
    _get_album_tracks = get_client_credentials_managed_client().album_tracks
    _next = get_client_credentials_managed_client().next

    tracks = []

    response = _get_album_tracks(album_id)

    while response is not None and (items := response["items"]):
        tracks.extend(items)

        response = _next(response)

    return tracks


@cache
def get_artist(artist_id: str) -> dict:
    _get_artist = get_client_credentials_managed_client().artist
    return _get_artist(artist_id)


@cache
def get_artist_related_artists(artist_id: str) -> list[dict]:
    _get_artist_related_artists = (
        get_client_credentials_managed_client().artist_related_artists
    )
    return _get_artist_related_artists(artist_id)["artists"]


@cache
def get_track(track_id: str) -> dict:
    _get_track = get_client_credentials_managed_client().track
    return _get_track(track_id)


@cache
def get_track_audio_features(track_id: str) -> dict | None:
    _get_track_audio_features = get_client_credentials_managed_client().audio_features

    try:
        return _get_track_audio_features(track_id)[0]
    except Exception:
        logger.error(f"Failed to get audio feature for track {track_id!r}")
        raise


def search_for_artist(search_text: str) -> dict:
    _search = get_client_credentials_managed_client().search
    return _search(search_text, limit=1, type="artist")["artists"]["items"][0]
