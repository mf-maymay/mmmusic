# -*- coding: utf-8 -*-
import numpy as np

from lib.models.artist import get_artist
from lib.models.genre_attributes import (
    GenreAttributes,
    get_genre_attributes,
    get_genre_attributes_means,
)
from lib.models.track import Track


def genre_position(track: Track) -> tuple:
    genre_positions = get_genre_attributes()

    genres = set()
    for artist in track.artist_ids:
        genres |= get_artist(artist).genres & genre_positions.keys()
        # NOTE: genres missing from genre_positions are ignored.

    if not genres:
        return get_genre_attributes_means()

    return GenreAttributes(
        *np.mean([genre_positions[genre] for genre in genres], axis=0)
    )
