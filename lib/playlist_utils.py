from lib.genres import artists_of_genres_matching
from lib.models.album import get_album
from lib.models.artist import get_artist
from lib.models.track import get_track
from lib.shuffling import smart_shuffle
from lib.user import User
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


# Playlist management
def add_tracks_to_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    for to_add in take_x_at_a_time(tracks, 100):
        no_timeout(user.sp.user_playlist_add_tracks)(user.username, playlist_id, to_add)


def clear_playlist(playlist_id, *, user: User):
    tracks = get_tracks_from_playlist(playlist_id, user=user)

    remove_tracks_from_playlist(playlist_id, tracks=tracks, user=user)


def get_tracks_from_playlist(playlist_id, *, user: User):
    tracks = []

    items = no_timeout(user.sp.playlist_items)(playlist_id)

    while items:
        tracks.extend(get_track(item["track"]["id"]) for item in items["items"])
        items = no_timeout(user.sp.next)(items)

    return tracks


def remove_tracks_from_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    for to_remove in take_x_at_a_time(tracks, 100):
        no_timeout(user.sp.user_playlist_remove_all_occurrences_of_tracks)(
            user.username, playlist_id, to_remove
        )


def replace_playlist(playlist_id, *, new_tracks, user: User):
    clear_playlist(playlist_id, user=user)

    add_tracks_to_playlist(playlist_id, tracks=new_tracks, user=user)


def shuffle_playlist(playlist_id, *, user: User):
    tracks = get_tracks_from_playlist(playlist_id, user=user)

    shuffled = smart_shuffle(tracks)

    replace_playlist(playlist_id, new_tracks=shuffled, user=user)
