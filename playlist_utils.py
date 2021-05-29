# -*- coding: utf-8 -*-
from genres import artists_of_genres_matching, genres_matching
from track import Track


def albums_from_artists(user, artists):
    artists = set(artists)
    return sorted(
        {album for album in user.albums() if set(album.artist_ids) & artists}
    )


def tracks_from_albums(albums):
    return [track for album in albums for track in album.tracks()]


def all_user_tracks(user):
    return tracks_from_albums(user.albums())


def tracks_by_audio_feature(features_filter_func):
    def get_tracks(playlist, user):
        all_tracks = all_user_tracks(user)
        all_features = Track.get_audio_features(all_tracks)
        return [track for track, features in zip(all_tracks, all_features)
                if features_filter_func(features)]
    return get_tracks


def tracks_by_genre_pattern(pattern, display=True):
    def get_tracks(playlist, user):
        artists = (
            artists_of_genres_matching(pattern, user.artists())
            - playlist.artists_to_exclude
        )

        if display:
            print(f"'{pattern}' genres:")
            for genre in sorted(genres_matching(pattern, artists)):
                print("*", genre)
            print()
            print(f"'{playlist.name}' artists:")
            for artist in sorted(artists):
                print("*", artist)

        albums = albums_from_artists(user, artists)
        playlist.description = pattern

        return tracks_from_albums(albums)
    return get_tracks


if __name__ == "__main__":
    from artist import Artist
    from user import User

    artists = [Artist("4Z8W4fKeB5YxbusRsdQVPb"),
               Artist("0oSGxfWSnnOXhD2fKuz2Gy")]

    user = User(input("username: "))

    albums = albums_from_artists(user, artists)

    tracks = tracks_from_albums(albums)

    # -------

    all_tracks = all_user_tracks(user)
