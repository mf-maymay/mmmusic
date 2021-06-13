# -*- coding: utf-8 -*-
from genres import artists_of_genres_matching
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


def tracks_by_album_attribute(album_filter_func):  # XXX
    def get_tracks(user):
        albums = [album for album in user.albums()
                  if album_filter_func(album)]
        return tracks_from_albums(albums)

    get_tracks.__doc__ = "tracks_by_artist_attribute(...)"
    return get_tracks


def tracks_by_artist_attribute(artist_filter_func):  # XXX
    def get_tracks(user):
        artists = [artist for artist in user.artists()
                   if artist_filter_func(artist)]
        return tracks_from_albums(albums_from_artists(user, artists))

    get_tracks.__doc__ = "tracks_by_artist_attribute(...)"
    return get_tracks


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


def tracks_by_genre_pattern(pattern, artists_to_exclude=()):
    def get_tracks(user):
        artists = (
            artists_of_genres_matching(pattern, user.artists())
            - set(artists_to_exclude)
        )
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
