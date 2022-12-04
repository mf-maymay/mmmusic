# -*- coding: utf-8 -*-
from collections import namedtuple
from functools import cache
import json
from pathlib import Path

import numpy as np

_genre_positions_file_path = Path(__file__).parent / "genre_positions.json"

GenreAttributes = namedtuple("GenreAttributes", ["top", "left"])


@cache
def get_genre_attributes():
    with _genre_positions_file_path.open() as f:
        genre_positions = json.load(f)

    return {
        genre: GenreAttributes(**coords) for genre, coords in genre_positions.items()
    }


@cache
def get_genre_attributes_means():
    return GenreAttributes(*np.mean(list(get_genre_attributes().values()), axis=0))
