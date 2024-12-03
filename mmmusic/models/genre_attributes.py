from collections import namedtuple
from collections.abc import Iterable
from functools import cache
import json
from pathlib import Path

import numpy as np

_genre_positions_file_path = Path(__file__).parent.parent / "data/genre_positions.json"

GenreAttributes = namedtuple("GenreAttributes", ["top", "left"])


@cache
def get_genre_attributes() -> dict[str, GenreAttributes]:
    with _genre_positions_file_path.open() as f:
        genre_positions = json.load(f)

    return {
        genre: GenreAttributes(**coords) for genre, coords in genre_positions.items()
    }


def get_genre_attribute_means(genres: Iterable[str]) -> GenreAttributes:
    genre_positions = get_genre_attributes()
    return GenreAttributes(
        *np.mean([genre_positions[genre] for genre in genres], axis=0)
    )


@cache
def get_default_genre_attributes() -> GenreAttributes:
    return get_genre_attribute_means(get_genre_attributes())
