import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from lib.models.albums import get_album, get_tracks_from_albums
from lib.models.artists import get_artist
from lib.utils import no_timeout

DEFAULT_SCOPE = "playlist-modify-private,playlist-modify-public,user-library-read"


class User:
    def __init__(self, username=None, *, redirect_uri=None):
        username_from_environ = os.environ.get("SPOTIPY_CLIENT_USERNAME")

        self.username = (
            username
            if username is not None
            else username_from_environ
            if username_from_environ is not None
            else input("username: ")
        )

        self._albums = None
        self._artists = None
        self._tracks = None

        auth_manager = SpotifyOAuth(
            username=self.username, redirect_uri=redirect_uri, scope=DEFAULT_SCOPE
        )

        self.sp = spotipy.Spotify(auth_manager=auth_manager, retries=None)

    @no_timeout
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
        print(f"{artist} ({len(albums)} albums)")
        for album in albums:
            print(f"* {album} [{album.release_date.year}]")