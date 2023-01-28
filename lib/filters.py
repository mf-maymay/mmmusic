from lib.genres import artists_of_genres_matching
from lib.models.album import get_album
from lib.models.artist import get_artist


def by_album_attribute(album_filter_func):
    def filter_tracks(tracks):
        return [
            track for track in tracks if album_filter_func(get_album(track.album_id))
        ]

    return filter_tracks


def by_artist_attribute(artist_filter_func):
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


def by_genre_pattern(pattern):
    def filter_tracks(tracks):
        return [
            track
            for track in tracks
            if artists_of_genres_matching(
                pattern, [get_artist(artist_id) for artist_id in track.artist_ids]
            )  # TODO: switch to actual regex evaluation
        ]

    return filter_tracks


def by_track_attribute(track_filter_func):
    def filter_tracks(tracks):
        return [track for track in tracks if track_filter_func(track)]

    return filter_tracks


def by_release_year(start_year, end_year):
    if start_year is None:
        start_year = float("-inf")

    if end_year is None:
        end_year = float("inf")

    def release_date_filter(album):
        return album.album_type != "compilation" and (
            start_year <= album.release_date.year <= end_year
        )

    return by_album_attribute(release_date_filter)
