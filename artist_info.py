# -*- coding: utf-8 -*-
import spotipy
from spotipy.util import prompt_for_user_token
from artists import get_artist


def get_user_artists(username):
    token = prompt_for_user_token(username, "user-library-read")

    if not token:
        raise RuntimeError("Failed to get token for " + username)

    sp = spotipy.Spotify(auth=token)

    saved = set()

    offset = 0

    while True:
        albums = sp.current_user_saved_albums(limit=50, offset=offset)

        items = albums["items"]

        for item in items:
            saved |= {get_artist(artist["id"])
                      for artist in item["album"]["artists"]}

        offset += len(items)

        if len(items) == 0:
            break

    return saved


if __name__ == "__main__":
    username = input("username: ")

    saved = get_user_artists(username)

    for artist in saved:
        print(artist)
