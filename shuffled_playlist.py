# -*- coding: utf-8 -*-
from album import Album
from artist import Artist
from genre_graph import artists_of_genres_matching
from playlists import playlists
from shuffling import order_tracks
from user import User
from utils import create_playlist, no_timeout, record_calls

Album.tracks = no_timeout(Album.tracks)
Artist.related = record_calls(no_timeout(Artist.related))
User.artists = no_timeout(User.artists)

Artist._use_name_for_repr = True


def make_shuffled_playlist(user, playlist):
    artists = (
        artists_of_genres_matching(playlist.pattern, user.artists())
        - playlist.artists_to_exclude
    )

    print("\nArtists:")
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

    create_playlist(user, ordered, playlist.name, description=playlist.pattern)


if __name__ == "__main__":
    user = User(input("username: "))

    playlist = playlists["classical"]

    make_shuffled_playlist(user, playlist)
