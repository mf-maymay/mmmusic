# -*- coding: utf-8 -*-
from cache import Cache
from genres import artists_of_genres_matching
from shuffling import smart_shuffle
from track import Track, get_audio_features, get_tracks_from_albums
from utils import no_timeout, take_x_at_a_time


def albums_from_artists(user, artists):
    artists = set(artists)
    return sorted({album for album in user.albums() if set(album.artist_ids) & artists})


@Cache()
def all_user_tracks(user):
    return get_tracks_from_albums(user.albums())


def tracks_by_album_attribute(album_filter_func):  # XXX
    def get_tracks(user):
        albums = [album for album in user.albums() if album_filter_func(album)]
        return get_tracks_from_albums(albums)

    get_tracks.__doc__ = "tracks_by_artist_attribute(...)"
    return get_tracks


def tracks_by_artist_attribute(artist_filter_func):  # XXX
    def get_tracks(user):
        artists = [artist for artist in user.artists() if artist_filter_func(artist)]
        return get_tracks_from_albums(albums_from_artists(user, artists))

    get_tracks.__doc__ = "tracks_by_artist_attribute(...)"
    return get_tracks


def tracks_by_track_attribute(track_filter_func, base=None):  # XXX
    def get_tracks(user):
        if base is None:
            all_tracks = all_user_tracks(user)
        else:
            all_tracks = base(user)
        return [track for track in all_tracks if track_filter_func(track)]

    get_tracks.__doc__ = "tracks_by_track_attribute(...)"
    return get_tracks


def tracks_by_audio_feature(features_filter_func, base=None):  # XXX
    def get_tracks(user):
        if base is None:
            all_tracks = all_user_tracks(user)
        else:
            all_tracks = base(user)
        all_features = get_audio_features(all_tracks)
        return [
            track
            for track, features in zip(all_tracks, all_features)
            if features_filter_func(features)
        ]

    get_tracks.__doc__ = "tracks_by_audio_feature(...)"
    return get_tracks


def tracks_by_genre_pattern(pattern, artists_to_exclude=()):
    def get_tracks(user):
        artists = artists_of_genres_matching(pattern, user.artists()) - set(
            artists_to_exclude
        )
        albums = albums_from_artists(user, artists)
        return get_tracks_from_albums(albums)

    get_tracks.__doc__ = f"tracks_by_genre_pattern({repr(pattern)})"
    return get_tracks


def tracks_from_playlist(playlist_id):
    def get_tracks(user):
        tracks = []
        items = no_timeout(user.sp.playlist_items)(playlist_id)

        while items:
            tracks.extend(Track(info=item["track"]) for item in items["items"])
            items = no_timeout(user.sp.next)(items)

        return tracks

    get_tracks.__doc__ = f"tracks_from_playlist({repr(playlist_id)})"
    return get_tracks


def shuffle_playlist(user, playlist_id):
    # get tracks
    tracks = tracks_from_playlist(playlist_id)(user)
    # clear playlist
    for subset in take_x_at_a_time(tracks, 100):
        to_remove = [track.id for track in subset]
        no_timeout(user.sp.user_playlist_remove_all_occurrences_of_tracks)(
            user._username, playlist_id, to_remove
        )
    # shuffle tracks
    shuffled = smart_shuffle(tracks, user)
    # write back to playlist
    for subset in take_x_at_a_time(shuffled, 100):
        to_add = [track.id for track in subset]
        no_timeout(user.sp.user_playlist_add_tracks)(
            user._username, playlist_id, to_add
        )
