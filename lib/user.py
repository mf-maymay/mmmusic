# -*- coding: utf-8 -*-
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from lib.models.album import get_album, get_tracks_from_albums
from lib.models.artist import Artist
from lib.utils import no_timeout

DEFAULT_SCOPE = "playlist-modify-private,user-library-read"


class User:
    def __init__(self, username=None, *, redirect_uri=None):
        username_from_environ = os.environ.get("SPOTIFY_USERNAME")

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
    def albums(self):
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

    def artists(self):
        if self._artists is None:
            artists = set()
            for album in self.albums():
                artists.update(Artist(artist_id) for artist_id in album.artist_ids)
            self._artists = tuple(sorted(artists))
        return self._artists

    def all_tracks(self):
        if self._tracks is None:
            self._tracks = get_tracks_from_albums(self.albums())
        return self._tracks

    def __hash__(self):
        return hash(self.username)


if __name__ == "__main__":
    from collections import defaultdict

    user = User()

    artist_albums = defaultdict(list)
    for album in sorted(user.albums(), key=lambda a: a.release_date):
        for artist_id in album.artist_ids:
            artist_albums[Artist(artist_id)].append(album)

    for artist, albums in sorted(
        artist_albums.items(), key=lambda k: (len(k[1]), k[0])
    ):
        print(f"{artist} ({len(albums)} albums)")
        for album in albums:
            print(f"* {album} [{album.release_date.year}]")