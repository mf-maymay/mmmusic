import random
from typing import Callable

from mmmusic.genres import artists_of_genres_matching_pattern
from mmmusic.models.albums import Album, get_album
from mmmusic.models.artists import Artist, get_artist
from mmmusic.models.operations import combinable
from mmmusic.models.tracks import Track, get_track
from mmmusic.models.types import TrackListTransformer
from mmmusic.music_theory import get_spotify_friendly_key, get_spotify_friendly_mode
from mmmusic.playlists.ordering import by_similarity


def filter_by_album_attribute(
    album_filter_func: Callable[[Album], bool]
) -> TrackListTransformer:
    @combinable
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [
            track for track in tracks if album_filter_func(get_album(track.album_id))
        ]

    return filter_tracks


def filter_by_artist_attribute(
    artist_filter_func: Callable[[Artist], bool]
) -> TrackListTransformer:
    @combinable
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [
            track
            for track in tracks
            if all(
                artist_filter_func(get_artist(artist_id))
                for artist_id in track.artist_ids
            )
        ]  # XXX: any or all?

    return filter_tracks


def filter_by_genre_pattern(pattern: str) -> TrackListTransformer:
    @combinable(display_name=f"genre matches {pattern!r}")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [
            track
            for track in tracks
            if artists_of_genres_matching_pattern(
                pattern,
                artists=[get_artist(artist_id) for artist_id in track.artist_ids],
            )
        ]

    return filter_tracks


def filter_by_number_of_tracks(
    n: int,
    *,
    randomly_sampled: bool = False,
) -> TrackListTransformer:
    @combinable(display_name=f"no. tracks = {n}")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return random.sample(tracks, n) if randomly_sampled else tracks[:n]

    return filter_tracks


def filter_by_release_year(
    start_year: int | None,
    end_year: int | None,
) -> TrackListTransformer:
    if start_year is None:
        start_year = float("-inf")

    if end_year is None:
        end_year = float("inf")

    def album_matches_release_date(album: Album) -> bool:
        return album.album_type != "compilation" and (
            start_year <= album.release_date.year <= end_year
        )

    return combinable(
        filter_by_album_attribute(album_matches_release_date),
        display_name=f"release year between {start_year} and {end_year}",
    )


def filter_by_similarity_to_track(track: Track | str) -> TrackListTransformer:
    track = get_track(track)

    @combinable
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return by_similarity(seed=track, tracks=tracks)

    return filter_tracks


def filter_by_track_attribute(
    attr: str,
    *,
    lower_bound: int | float | None = None,
    upper_bound: int | float | None = None,
    inclusive: bool = True,
) -> TrackListTransformer:
    operands = (
        ([str(lower_bound)] if lower_bound is not None else [])
        + [attr]
        + ([str(upper_bound)] if upper_bound is not None else [])
    )

    operator = " <= " if inclusive else " < "

    if lower_bound is None:
        lower_bound = float("-inf")

    if upper_bound is None:
        upper_bound = float("inf")

    def attr_in_range_inclusive(track: Track) -> bool:
        return lower_bound <= getattr(track, attr) <= upper_bound

    def attr_in_range_exclusive(track: Track) -> bool:
        return lower_bound < getattr(track, attr) < upper_bound

    attr_in_range = attr_in_range_inclusive if inclusive else attr_in_range_exclusive

    @combinable(display_name=f"({operator.join(operands)})")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [track for track in tracks if attr_in_range(track)]

    return filter_tracks


def filter_by_audio_feature(
    feature: str,
    *,
    lower_bound: int | float | None = None,
    upper_bound: int | float | None = None,
    inclusive: bool = True,
) -> TrackListTransformer:
    operands = (
        ([str(lower_bound)] if lower_bound is not None else [])
        + [feature]
        + ([str(upper_bound)] if upper_bound is not None else [])
    )

    operator = " <= " if inclusive else " < "

    if lower_bound is None:
        lower_bound = float("-inf")

    if upper_bound is None:
        upper_bound = float("inf")

    def attr_in_range_inclusive(track: Track) -> bool:
        return lower_bound <= track[feature] <= upper_bound

    def attr_in_range_exclusive(track: Track) -> bool:
        return lower_bound < track[feature] < upper_bound

    attr_in_range = attr_in_range_inclusive if inclusive else attr_in_range_exclusive

    @combinable(display_name=f"({operator.join(operands)})")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [track for track in tracks if attr_in_range(track)]

    return filter_tracks
