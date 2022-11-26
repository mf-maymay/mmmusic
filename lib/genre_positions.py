# -*- coding: utf-8 -*-
from collections import namedtuple
import json
from pathlib import Path

import numpy as np

from lib.models.artist import get_artist
from lib.models.track import Track

GenreCoordinates = namedtuple("GenreCoordinates", ["top", "left"])

with open(Path(__file__).parent / "genre_positions.json") as f:
    _genre_positions_raw = json.load(f)

genre_positions = {
    genre: GenreCoordinates(**coords) for genre, coords in _genre_positions_raw.items()
}

average_genre_position = GenreCoordinates(
    *np.mean(list(genre_positions.values()), axis=0)
)


def genre_position(track: Track) -> tuple:
    genres = set()
    for artist in track.artist_ids:
        genres |= get_artist(artist).genres & genre_positions.keys()
        # XXX: genres missing from genre_positions are ignored

    if not genres:
        return average_genre_position

    return GenreCoordinates(
        *np.mean([genre_positions[genre] for genre in genres], axis=0)
    )
