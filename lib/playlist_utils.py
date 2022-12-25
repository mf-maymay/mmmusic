from lib.genres import artists_of_genres_matching
from lib.models.album import get_album
from lib.models.artist import get_artist
from lib.models.track import get_track
from lib.shuffling import smart_shuffle
from lib.utils import no_timeout, take_x_at_a_time


def filter_by_album_attribute(album_filter_func):
    def filter_tracks(tracks):
        return [
            track for track in tracks if album_filter_func(get_album(track.album_id))
        ]

    return filter_tracks


def filter_by_artist_attribute(artist_filter_func):
    def filter_tracks(tracks):
        return [
            track
            for track in tracks
            if all(
                artist_filter_func(get_artist(artist_id))
                for artist_id in track.artist_ids
            )
        ]  # XXX: any or all?

    return filter_tracks


def filter_by_genre_pattern(pattern):
    def filter_tracks(tracks):
        return [
            track
            for track in tracks
            if artists_of_genres_matching(
                pattern, [get_artist(artist_id) for artist_id in track.artist_ids]
            )  # TODO: switch to actual regex evaluation
        ]

    return filter_tracks


def filter_by_track_attribute(track_filter_func):
    def filter_tracks(tracks):
        return [track for track in tracks if track_filter_func(track)]

    return filter_tracks


def filter_by_release_year(start_year, end_year):
    if start_year is None:
        start_year = float("-inf")
    if end_year is None:
        end_year = float("inf")

    def release_date_filter(album):
        return album.album_type != "compilation" and (
            start_year <= album.release_date.year <= end_year
        )

    return filter_by_album_attribute(release_date_filter)


def tracks_from_playlist(playlist_id):
    def get_tracks(user):
        tracks = []
        items = no_timeout(user.sp.playlist_items)(playlist_id)

        while items:
            tracks.extend(get_track(item["track"]["id"]) for item in items["items"])
            items = no_timeout(user.sp.next)(items)
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
