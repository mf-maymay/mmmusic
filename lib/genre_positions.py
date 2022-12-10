# -*- coding: utf-8 -*-
from lib.models.artist import get_artist
from lib.models.genre_attributes import (
    GenreAttributes,
    get_default_genre_attributes,
    get_genre_attribute_means,
    get_genre_attributes,
)
from lib.models.track import Track


def genre_position(track: Track) -> GenreAttributes:
    genre_positions = get_genre_attributes()

    genres = set()
    for artist in track.artist_ids:
        genres |= get_artist(artist).genres & genre_positions.keys()
        # NOTE: genres missing from genre_positions are ignored.

    return (
        get_genre_attribute_means(genres) if genres else get_default_genre_attributes()
    )
