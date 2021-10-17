# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from album import Album
from artist import Artist
from utils import no_timeout


class User(object):
    def __init__(self, username, scope="user-library-read"):
        self._username = username

        self._albums = None
        self._artists = None

        self.sp = None

        self.setup_sp(scope=scope)

    def setup_sp(self, scope="user-library-read"):

        auth_manager = SpotifyOAuth(username=self._username, scope=scope)

        self.sp = spotipy.Spotify(auth_manager=auth_manager, retries=None)

    @no_timeout
    def albums(self):  # XXX: subsequent calls do not update list

        if self._albums is not None:
            return self._albums

        saved = []

        albums = self.sp.current_user_saved_albums(limit=50, offset=0)

        while albums:
            saved.extend(Album(info=item["album"]) for item in albums["items"])

            albums = self.sp.next(albums)

        self._albums = tuple(sorted(saved))

        return self._albums

    def artists(self):  # XXX: subsequent calls do not update list
        if self._artists is not None:
            return self._artists

        artist_ids = {
            artist_id for album in self.albums() for artist_id in album.artist_ids
        }

        saved = {Artist(artist_id) for artist_id in artist_ids}

        self._artists = tuple(sorted(saved))

        return self._artists

    def __hash__(self):
        return hash(self._username)


if __name__ == "__main__":
    user = User(input("username: "))

    for album in user.albums():
        print(album)

    for artist in user.artists():
        print(artist)

    # albums = sorted(", ".join(str(Artist(artist))
    #                           for artist in album.artist_ids) +
    #                 " -- " + str(album) for album in user.albums())
