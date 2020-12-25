# -*- coding: utf-8 -*-
import requests


def no_timeout(func):
    def wrapped(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                print(f"ConnectionError on {func.__name__}. Retrying...")
                continue
            except requests.ReadTimeout:
                print(f"ReadTimout on {func.__name__}. Retrying...")
                continue
    return wrapped


def create_playlist(user, tracks, playlist_name, confirm=True):
    if (not confirm or
            input(f"Create playlist '{playlist_name}'? (y/n): ")[0] in "yY"):
        print(f"Creating '{playlist_name}'...")

        user.setup_sp(scope="playlist-modify-private")  # XXX

        playlist = user.sp.user_playlist_create(user._username,
                                                playlist_name,
                                                public=False)

        for i in range(0, (l := len(tracks)) // 100 + bool(l % 100)):
            to_add = tracks[(100 * i):(100 * (i + 1))]
            user.sp.user_playlist_add_tracks(user._username,
                                             playlist["id"],
                                             to_add)
