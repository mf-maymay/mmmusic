# -*- coding: utf-8 -*-
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from music_tools.album import Album, get_tracks_from_albums
from music_tools.artist import Artist
from music_tools.utils import no_timeout

DEFAULT_SCOPE = "playlist-modify-private,user-library-read"


class User:
    def __init__(self, username=None):
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

        auth_manager = SpotifyOAuth(username=self.username, scope=DEFAULT_SCOPE)

        self.sp = spotipy.Spotify(auth_manager=auth_manager, retries=None)

    @no_timeout
    def albums(self):
        if self._albums is None:
            albums = []

            albums_on_page = self.sp.current_user_saved_albums(limit=50, offset=0)

            while albums_on_page:
                albums.extend(
                    Album(info=item["album"]) for item in albums_on_page["items"]
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
    user = User()

    for album in user.albums():
        print(album)

    for artist in user.artists():
        print(artist)
