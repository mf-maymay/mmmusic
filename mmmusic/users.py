import os
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyAuthBase, SpotifyPKCE

from mmmusic.external.spotify import create_requests_session_for_spotify
from mmmusic.log_utils import get_logger
from mmmusic.models.albums import get_album, get_tracks_from_albums
from mmmusic.models.artists import get_artist

logger = get_logger()

DEFAULT_SCOPE = "playlist-modify-private,playlist-modify-public,user-library-read"


class User:
    def __init__(self, username=None):
        self.username = (
            username
            if username is not None
            else os.environ.get("SPOTIPY_CLIENT_USERNAME")
        )

        if self.username is None:
            raise ValueError("Username not provided")

        self._albums = None
        self._artists = None
        self._tracks = None

        auth_manager = self._prepare_auth_manager()

        self.sp = spotipy.Spotify(
            auth_manager=auth_manager,
            requests_session=create_requests_session_for_spotify(),
        )

    def _prepare_auth_manager(self) -> SpotifyAuthBase:
        logger.debug("Preparing auth manager for user %r", self.username)

        refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        auth_manager = SpotifyPKCE(
            username=self.username,
            scope=DEFAULT_SCOPE,
        )

        if refresh_token is None:
            logger.debug("Refresh token not provided")
        elif (cache_path := Path(auth_manager.cache_handler.cache_path)).exists():
            logger.debug("Using cached token info at %s", cache_path)
        else:
            logger.debug("Cached token info not found at %s", cache_path)

            logger.debug("Refreshing access token using refresh token")

            token_info = auth_manager.refresh_access_token(refresh_token)
            logger.debug("Access token expires in %r", token_info["expires_in"])

            if "refresh_token" not in token_info:
                logger.debug("'refresh_token' missing from token info")
            elif refresh_token != token_info["refresh_token"]:
                logger.warning(
                    "Returned refresh token differs from provided refresh token"
                )

        logger.debug("OAuth manager was successfully prepared")

        return auth_manager

    def get_saved_albums(self):
        if self._albums is None:
            albums = []

            albums_on_page = self.sp.current_user_saved_albums(limit=50, offset=0)

            while albums_on_page:
                albums.extend(
                    get_album(item["album"]["id"]) for item in albums_on_page["items"]
                )
                albums_on_page = self.sp.next(albums_on_page)

            self._albums = tuple(sorted(albums))

        return self._albums

    def get_artists_of_saved_albums(self):
        if self._artists is None:
            artists = set()

            for album in self.get_saved_albums():
                artists.update(get_artist(artist_id) for artist_id in album.artist_ids)

            self._artists = tuple(sorted(artists))

        return self._artists

    def get_tracks_from_saved_albums(self):
        if self._tracks is None:
            self._tracks = get_tracks_from_albums(self.get_saved_albums())

        return self._tracks

    def __hash__(self):
        return hash(self.username)


if __name__ == "__main__":
    from collections import defaultdict

    user = User()

    artist_albums = defaultdict(list)

    for album in sorted(user.get_saved_albums(), key=lambda a: a.release_date):
        for artist_id in album.artist_ids:
            artist_albums[get_artist(artist_id)].append(album)

    for artist, albums in sorted(
        artist_albums.items(), key=lambda k: (len(k[1]), k[0])
    ):
        print(f"{artist} ({len(albums)} albums)")  # noqa: T201

        for album in albums:
            print(f"* {album} [{album.release_date.year}]")  # noqa: T201

    # TODO: Move this functionality to a separate script.
