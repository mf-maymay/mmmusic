# -*- coding: utf-8 -*-
from artist import Artist
from genres import artists_of_genres_matching, genres_matching
from playlists import playlists
from shuffling import order_tracks
from user import User
from utils2 import albums_from_artists, tracks_from_albums


def make_shuffled_playlist(user, playlist, confirm=True):
    artists = (
        artists_of_genres_matching(playlist.pattern, user.artists())
        - playlist.artists_to_exclude
    )

    print(f"'{playlist.pattern}' genres:")
    for genre in sorted(genres_matching(playlist.pattern, artists)):
        print("*", genre)
    print()
    print(f"'{playlist.name}' artists:")
    for artist in sorted(artists):
        print("*", artist)

    albums = albums_from_artists(user, artists)

    tracks = tracks_from_albums(albums)

    playlist.tracks = order_tracks(tracks, user)

    playlist.create(user, confirm=confirm)


if __name__ == "__main__":
    Artist._use_name_for_repr = True

    user = User(input("username: "))
    print()

    for name in sorted(playlists):
        make_shuffled_playlist(user, playlists[name], confirm=False)
        print()
