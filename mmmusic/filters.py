import random
from typing import Callable

from mmmusic.genres import artists_of_genres_matching
from mmmusic.models.albums import Album, get_album
from mmmusic.models.artists import Artist, get_artist
from mmmusic.models.tracks import Track, get_track
from mmmusic.models.types import TrackListTransformer, Tracks
from mmmusic.music_theory import get_spotify_friendly_key, get_spotify_friendly_mode
from mmmusic.playlists.ordering import by_similarity


def by_album_attribute(
    album_filter_func: Callable[[Album], bool]
) -> TrackListTransformer:
    def filter_tracks(tracks: Tracks) -> Tracks:
        return [
            track for track in tracks if album_filter_func(get_album(track.album_id))
        ]

    return filter_tracks


def by_artist_attribute(
    artist_filter_func: Callable[[Artist], bool]
) -> TrackListTransformer:
    def filter_tracks(tracks: Tracks) -> Tracks:
        return [
            track
            for track in tracks
            if all(
                artist_filter_func(get_artist(artist_id))
                for artist_id in track.artist_ids
            )
        ]  # XXX: any or all?

    return filter_tracks


def by_genre_pattern(pattern: str) -> TrackListTransformer:
    def filter_tracks(tracks: Tracks) -> Tracks:
        return [
            track
            for track in tracks
            if artists_of_genres_matching(
                pattern,
                [get_artist(artist_id) for artist_id in track.artist_ids],
            )  # TODO: switch to actual regex evaluation
        ]

    return filter_tracks


def by_scale(*, key: str, mode: str) -> TrackListTransformer:
    spotify_friendly_key = get_spotify_friendly_key(key)
    spotify_friendly_mode = get_spotify_friendly_mode(mode)

    def track_matches_scale(track: Track) -> bool:
        return (
            track["key"] == spotify_friendly_key
            and track["mode"] == spotify_friendly_mode
        )

    return by_track_attribute(track_matches_scale)


def by_number_of_tracks(
    n: int,
    *,
    randomly_sampled: bool = False,
) -> TrackListTransformer:
    def filter_tracks(tracks: Tracks) -> Tracks:
        return random.sample(tracks, n) if randomly_sampled else tracks[:n]

    return filter_tracks


def by_release_year(
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

    return by_album_attribute(album_matches_release_date)


def by_similarity_to_track(track: Track | str) -> TrackListTransformer:
    track = get_track(track)

    def filter_tracks(tracks: Tracks) -> Tracks:
        return by_similarity(seed=track, tracks=tracks)

    return filter_tracks


def by_track_attribute(
    track_filter_func: Callable[[Track], bool]
) -> TrackListTransformer:
    def filter_tracks(tracks: Tracks) -> Tracks:
        return [track for track in tracks if track_filter_func(track)]

    return filter_tracks