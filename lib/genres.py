# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import permutations
import re

from lib.models.artist import get_artist
from lib.models.genre_attributes import (
    GenreAttributes,
    get_default_genre_attributes,
    get_genre_attribute_means,
    get_genre_attributes,
)
from lib.models.track import Track


def get_track_genre_attributes(track: Track) -> GenreAttributes:
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


def genres_and_members(artists):
    """Returns a dictionary mapping genres to their artists."""
    genre_artists = defaultdict(set)  # genre: artists in genre

    for artist in artists:
        for genre in artist.genres:
            genre_artists[genre].add(artist)

    return dict(genre_artists)


def genres_matching(keyword, artists):
    """Returns the genres containing `keyword` in their names."""
    pattern = re.compile(keyword)
    return {genre for genre in genres_and_members(artists) if pattern.fullmatch(genre)}


def artists_of_genres_matching(keyword, artists, regex=True, match_individual=True):
    """
    Returns the artists of genres containing `keyword` in their names.

    If match_individual is True, an artist matches whenever any of its genres
        match the keyword pattern.
    If match_individual is False, then the joined, comma-separated string of
        genres (e.g., 'album rock,classic rock,hard rock,rock') must be matched
        by the keyword pattern.
    """
    if not match_individual:
        pattern = re.compile(keyword)
        return {
            artist for artist in artists if pattern.fullmatch(",".join(artist.genres))
        }

    members = set()

    genre_artists = genres_and_members(artists)

    for genre in genres_matching(keyword, artists):
        members.update(genre_artists[genre])

    return members


def genre_overlaps(artists):
    """Returns a dictionary mapping pairs of genres to their shared artists."""
    mutuals = defaultdict(set)

    for artist in artists:
        for pair in permutations(get_artist(artist).genres, 2):
            mutuals[pair].add(artist)

    return dict(mutuals)


def related_genres(genre, artists):
    """Returns the genres that share artists with `genre`."""
    related = set()

    for pair in genre_overlaps(artists):
        if genre in pair:
            related.update(pair)

    return related - {genre}
