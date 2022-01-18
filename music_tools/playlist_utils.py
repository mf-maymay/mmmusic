# -*- coding: utf-8 -*-
from scipy.spatial.distance import euclidean as distance

from music_tools.album import get_tracks_from_albums
from music_tools.genre_positions import genre_position
from music_tools.genres import artists_of_genres_matching
from music_tools.shuffling import smart_shuffle
from music_tools.track import Track
from music_tools.utils import no_timeout, take_x_at_a_time


def _albums_from_artists(user, artists):
    artists = set(artists)
    return sorted({album for album in user.albums() if set(album.artist_ids) & artists})


def tracks_by_album_attribute(album_filter_func):
    def get_tracks(user):
        albums = [album for album in user.albums() if album_filter_func(album)]
        return get_tracks_from_albums(albums)

    return get_tracks


def tracks_by_artist_attribute(artist_filter_func):
    def get_tracks(user):
        artists = [artist for artist in user.artists() if artist_filter_func(artist)]
        return get_tracks_from_albums(_albums_from_artists(user, artists))

    return get_tracks


def tracks_by_track_attribute(track_filter_func):
    def filter_tracks(tracks):
        return [track for track in tracks if track_filter_func(track)]

    return filter_tracks


def tracks_by_genre_pattern(pattern, artists_to_exclude=()):
    def get_tracks(user):
        artists = artists_of_genres_matching(pattern, user.artists()) - set(
            artists_to_exclude
        )
        albums = _albums_from_artists(user, artists)
        return get_tracks_from_albums(albums)

    return get_tracks


def tracks_by_release_year(start_year, end_year):
    if start_year is None:
        start_year = float("-inf")
    if end_year is None:
        end_year = float("inf")

    def release_date_filter(album):
        return album["album_type"] != "compilation" and (
            start_year <= int(album["release_date"].split("-")[0]) <= end_year
        )

    return tracks_by_album_attribute(release_date_filter)


def tracks_from_playlist(playlist_id):
    def get_tracks(user):
        tracks = []
        items = no_timeout(user.sp.playlist_items)(playlist_id)

        while items:
            tracks.extend(Track(info=item["track"]) for item in items["items"])
            items = no_timeout(user.sp.next)(items)

        return tracks

    return get_tracks


def tracks_near_genre_coordinates(top, left, *, max_distance):
    def get_tracks(user):
        tracks = [
            track
            for track in user.all_tracks()
            if distance((top, left), genre_position(track)) < max_distance
        ]

        return tracks

    return get_tracks


def clear_playlist(user, playlist_id):
    # get tracks
    tracks = tracks_from_playlist(playlist_id)(user)
    # clear playlist
    for subset in take_x_at_a_time(tracks, 100):
        to_remove = [track.id for track in subset]
        no_timeout(user.sp.user_playlist_remove_all_occurrences_of_tracks)(
            user.username, playlist_id, to_remove
        )


def shuffle_playlist(user, playlist_id):
    # get tracks
    tracks = tracks_from_playlist(playlist_id)(user)
    # clear playlist
    for subset in take_x_at_a_time(tracks, 100):
        to_remove = [track.id for track in subset]
        no_timeout(user.sp.user_playlist_remove_all_occurrences_of_tracks)(
            user.username, playlist_id, to_remove
        )
    # shuffle tracks
    shuffled = smart_shuffle(tracks)
    # write back to playlist
    for subset in take_x_at_a_time(shuffled, 100):
        to_add = [track.id for track in subset]
        no_timeout(user.sp.user_playlist_add_tracks)(user.username, playlist_id, to_add)
