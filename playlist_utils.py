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


def tracks_by_audio_feature(features_filter_func, base=None):  # XXX
    def get_tracks(user):
        if base is None:
            all_tracks = all_user_tracks(user)
        else:
            all_tracks = base(user)
        all_features = Track.get_audio_features(all_tracks)
        return [track for track, features in zip(all_tracks, all_features)
                if features_filter_func(features)]

    get_tracks.__doc__ = "tracks_by_audio_feature(...)"
    return get_tracks


def tracks_by_genre_pattern(pattern, artists_to_exclude=(), display=True):
    def get_tracks(user):
        artists = (
            artists_of_genres_matching(pattern, user.artists())
            - set(artists_to_exclude)
        )

        if display:
            print(f"'{pattern}' genres:")
            for genre in sorted(genres_matching(pattern, artists)):
                print("*", genre)
            print()
            print(f"'{pattern}' artists:")
            for artist in sorted(artists):
                print("*", artist)

        albums = albums_from_artists(user, artists)

        return tracks_from_albums(albums)

    get_tracks.__doc__ = f"tracks_by_genre_pattern({repr(pattern)})"
    return get_tracks


def tracks_from_playlist(playlist_id):
    def get_tracks(user):
        tracks = []
        items = user.sp.playlist_items(playlist_id)

        while items:
            tracks.extend(
                Track(
                    item["track"]["id"],
                    item["track"]["name"],
                    item["track"]["album"]["id"],
                    tuple(artist["id"] for artist in item["track"]["artists"])
                )
                for item in items["items"]
            )
            items = user.sp.next(items)

        return tracks

    get_tracks.__doc__ = f"tracks_from_playlist({repr(playlist_id)})"
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
