# -*- coding: utf-8 -*-
import spotipy
from spotipy.util import prompt_for_user_token
from albums import Album
from artists import Artist

# TODO: rename to "users"


class User(object):
    def __init__(self, username):
        self._username = username

        token = prompt_for_user_token(self._username, "user-library-read")

        if not token:
            raise RuntimeError("Failed to get token")

        self.sp = spotipy.Spotify(auth=token)

        self._albums = None
        self._artists = None

    def albums(self):
        if self._albums:
            return self._albums

        saved = []

        albums = self.sp.current_user_saved_albums(limit=50, offset=0)

        while albums:
            saved.extend(
                Album(album["album"]["id"],
                      album["album"]["name"],
                      tuple(artist["id"]
                            for artist in album["album"]["artists"]))
                for album in albums["items"]
            )

            albums = self.sp.next(albums)

        self._albums = tuple(sorted(saved))

        return self._albums

    def artists(self):
        if self._artists:
            return self._artists

        saved = set()

        for album in self.albums():
            saved |= {Artist(artist_id) for artist_id in album.artist_ids}

        self._artists = tuple(sorted(saved))

        return self._artists


if __name__ == "__main__":
    user = User(input("username: "))

    for album in user.albums():
        print(album)

    for artist in user.artists():
        print(artist)
