from collections import defaultdict
from itertools import permutations
import re

from mmmusic.models.artists import Artist, get_artist
from mmmusic.models.genre_attributes import (
    GenreAttributes,
    get_default_genre_attributes,
    get_genre_attribute_means,
    get_genre_attributes,
)
from mmmusic.models.tracks import Track


def get_genre_attributes_for_track(track: Track) -> GenreAttributes:
    genre_attributes = get_genre_attributes()

    track_genres = set()
    for artist in track.artist_ids:
        track_genres |= get_artist(artist).genres & genre_attributes.keys()
        # NOTE: genres missing from genre_attributes are ignored.

    return (
        get_genre_attribute_means(track_genres)
        if track_genres
        else get_default_genre_attributes()
    )


def get_genre_artists_map(artists: list[Artist]) -> dict[str, set[Artist]]:
    """Returns a dictionary mapping genres to their artists."""
    genre_artists = defaultdict(set)  # genre: artists in genre

    for artist in artists:
        for genre in artist.genres:
            genre_artists[genre].add(artist)

    return dict(genre_artists)


def genres_matching_pattern(keyword: str, *, artists: list[Artist]) -> set[str]:
    pattern = re.compile(keyword)
    return {
        genre for genre in get_genre_artists_map(artists) if pattern.fullmatch(genre)
    }


def artists_of_genres_matching_pattern(
    keyword: str,
    *,
    artists: list[Artist],
) -> set[Artist]:
    members: set[Artist] = set()

    genre_artists = get_genre_artists_map(artists)

    for genre in genres_matching_pattern(keyword, artists=artists):
        members.update(genre_artists[genre])

    return members


def genre_overlaps(artists: list[Artist]) -> dict[tuple[str, str], set[Artist]]:
    """Returns a dictionary mapping pairs of genres to their shared artists."""
    mutuals = defaultdict(set)

    for artist in artists:
        for pair in permutations(get_artist(artist).genres, 2):
            mutuals[pair].add(artist)

    return dict(mutuals)
