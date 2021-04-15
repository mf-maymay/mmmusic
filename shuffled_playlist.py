# -*- coding: utf-8 -*-
from album import Album
from artist import Artist
from genre_graph import artists_of_genres_matching
from playlists import create_playlist, playlists
from shuffling import order_tracks
from user import User


def make_shuffled_playlist(user, playlist, confirm=True):
    artists = (
        artists_of_genres_matching(playlist.pattern, user.artists())
        - playlist.artists_to_exclude
    )

    print(f"'{playlist.name}' artists:")
    for artist in sorted(artists):
        print("*", artist)

    albums = {album for album in user.albums()
              if set(album.artist_ids) & artists}

    artist_albums = {artist: sorted((album for album in albums
                                     if artist in album.artist_ids),
                                    key=Album.release_date)
                     for artist in artists}

    albums_order = []
    tracks = []

    for artist in artists:
        for album in artist_albums[artist]:
            if album not in albums_order:
                albums_order.append(album)
                tracks.extend(track["id"] for track in album.tracks())

    ordered = order_tracks(tracks, user)

    create_playlist(
        user, ordered, playlist.name,
        description=playlist.pattern,
        confirm=confirm
    )


if __name__ == "__main__":
    Artist._use_name_for_repr = True

    user = User(input("username: "))
    print()

    for name in sorted(playlists):
        make_shuffled_playlist(user, playlists[name], confirm=False)
        print()
