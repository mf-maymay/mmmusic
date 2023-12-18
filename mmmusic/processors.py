import random

from mmmusic.features import get_scores_for_tracks, similarity
from mmmusic.genres import artists_of_genres_matching_pattern
from mmmusic.models.albums import get_album
from mmmusic.models.artists import Artist, ArtistID, get_artist
from mmmusic.models.operations import combinable
from mmmusic.models.tracks import Track, get_track
from mmmusic.models.types import TrackListTransformer
from mmmusic.music_theory import get_spotify_friendly_key, get_spotify_friendly_mode


def exclude_artists(*artists: Artist | ArtistID) -> TrackListTransformer:
    if not artists:
        raise ValueError

    artists_to_exclude = {get_artist(artist) for artist in artists}

    artist_names = sorted(artist.name for artist in artists_to_exclude)

    display_name = "not by " + (
        " or ".join(artist_names)
        if len(artist_names) < 3
        else ", ".join([*artist_names[:-1], f"or {artist_names[-1]}"])
    )

    @combinable(display_name=display_name)
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [
            track for track in tracks if not set(track.artist_ids) & artists_to_exclude
        ]

    return filter_tracks


def filter_by_artist_attribute(
    attr: str,
    *,
    lower_bound: int | float | None = None,
    upper_bound: int | float | None = None,
    inclusive: bool = True,
) -> TrackListTransformer:
    if lower_bound is None and upper_bound is None:
        raise ValueError

    display_name = _construct_display_name_for_bounded_feature(
        f"artist {attr}",
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        inclusive=inclusive,
    )

    if lower_bound is None:
        lower_bound = float("-inf")

    if upper_bound is None:
        upper_bound = float("inf")

    def attr_in_range_inclusive(artist: Artist) -> bool:
        return lower_bound <= getattr(artist, attr) <= upper_bound

    def attr_in_range_exclusive(artist: Artist) -> bool:
        return lower_bound < getattr(artist, attr) < upper_bound

    attr_in_range = attr_in_range_inclusive if inclusive else attr_in_range_exclusive

    @combinable(display_name=display_name)
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [
            track
            for track in tracks
            if all(
                attr_in_range(get_artist(artist_id)) for artist_id in track.artist_ids
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
    start_year: int | float | None = None,
    end_year: int | float | None = None,
) -> TrackListTransformer:
    if start_year is None and end_year is None:
        raise ValueError

    if start_year is not None and end_year is not None:
        display_name = f"released between {start_year} and {end_year}"

    if start_year is None:
        display_name = f"released before {end_year}"
        start_year = float("-inf")

    if end_year is None:
        display_name = f"released after {start_year}"
        end_year = float("inf")

    @combinable(display_name=display_name)
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [
            track
            for track in tracks
            if start_year <= get_album(track.album_id).release_date.year < end_year
        ]

    return filter_tracks


def filter_by_similarity_to_track(
    track: Track | str, *, number_of_tracks: int
) -> TrackListTransformer:
    seed = get_track(track)

    return combinable(
        order_by_similarity_to_track(seed)
        & filter_by_number_of_tracks(number_of_tracks),
        display_name=f"{number_of_tracks} tracks most similar to '{seed.name}'",
    )


def filter_by_track_attribute(
    attr: str,
    *,
    lower_bound: int | float | None = None,
    upper_bound: int | float | None = None,
    inclusive: bool = True,
) -> TrackListTransformer:
    if lower_bound is None and upper_bound is None:
        raise ValueError

    display_name = _construct_display_name_for_bounded_feature(
        attr,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        inclusive=inclusive,
    )

    if lower_bound is None:
        lower_bound = float("-inf")

    if upper_bound is None:
        upper_bound = float("inf")

    def attr_in_range_inclusive(track: Track) -> bool:
        return lower_bound <= getattr(track, attr) <= upper_bound

    def attr_in_range_exclusive(track: Track) -> bool:
        return lower_bound < getattr(track, attr) < upper_bound

    attr_in_range = attr_in_range_inclusive if inclusive else attr_in_range_exclusive

    @combinable(display_name=display_name)
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
    if lower_bound is None and upper_bound is None:
        raise ValueError

    display_name = _construct_display_name_for_bounded_feature(
        feature,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        inclusive=inclusive,
    )

    if lower_bound is None:
        lower_bound = float("-inf")

    if upper_bound is None:
        upper_bound = float("inf")

    def attr_in_range_inclusive(track: Track) -> bool:
        return lower_bound <= track[feature] <= upper_bound

    def attr_in_range_exclusive(track: Track) -> bool:
        return lower_bound < track[feature] < upper_bound

    attr_in_range = attr_in_range_inclusive if inclusive else attr_in_range_exclusive

    @combinable(display_name=display_name)
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [track for track in tracks if attr_in_range(track)]

    return filter_tracks


def filter_by_key(key: str) -> TrackListTransformer:
    spotify_friendly_key = get_spotify_friendly_key(key)

    @combinable(display_name=f"key is {key}")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [track for track in tracks if track["key"] == spotify_friendly_key]

    return filter_tracks


def filter_by_mode(mode: str) -> TrackListTransformer:
    spotify_friendly_mode = get_spotify_friendly_mode(mode)

    @combinable(display_name=f"mode is {mode}")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        return [track for track in tracks if track["mode"] == spotify_friendly_mode]

    return filter_tracks


@combinable(display_name="ordered by popularity")
def order_by_popularity(tracks: list[Track]) -> list[Track]:
    return sorted(
        tracks,
        key=lambda track: track.popularity,
        reverse=True,
    )


def order_by_similarity_to_track(track: Track | str) -> TrackListTransformer:
    seed = get_track(track)

    @combinable(display_name=f"ordered by similarity to '{seed.name}'")
    def filter_tracks(tracks: list[Track]) -> list[Track]:
        scores = get_scores_for_tracks([*tracks, seed])

        similarities: dict[Track, float] = {
            track: similarity(scores[track], scores[seed]) for track in tracks
        }

        return sorted(tracks, key=similarities.get, reverse=True)

    return filter_tracks


def _construct_display_name_for_bounded_feature(
    feature_name: str,
    *,
    lower_bound: int | float | None = None,
    upper_bound: int | float | None = None,
    inclusive: bool = True,
) -> str:
    if lower_bound is None and upper_bound is None:
        raise ValueError

    eq = "=" if inclusive else ""

    if lower_bound is None:
        return f"{feature_name} <{eq} {upper_bound}"

    if upper_bound is None:
        return f"{feature_name} >{eq} {lower_bound}"

    return f"{lower_bound} <{eq} {feature_name} <{eq} {upper_bound}"
