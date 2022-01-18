# -*- coding: utf-8 -*-
import json
from pathlib import Path

import numpy as np

from music_tools.artist import Artist
from music_tools.track import Track

_positions_file_path = Path(__file__).parent / "genre_positions.json"

with open(_positions_file_path) as f:
    genre_positions = json.load(f)

averages_genre_positions = {}
averages_genre_positions["top"] = np.mean(
    [pos["top"] for pos in genre_positions.values()]
)
averages_genre_positions["left"] = np.mean(
    [pos["left"] for pos in genre_positions.values()]
)


def genre_position(track: Track) -> tuple:
    genres = set()
    for artist in track.artist_ids:
        genres |= Artist(artist).genres & genre_positions.keys()
        # XXX: genres missing from genre_positions are ignored

    if not genres:
        return averages_genre_positions["top"], averages_genre_positions["left"]

    top = np.mean([genre_positions[genre]["top"] for genre in genres])
    left = np.mean([genre_positions[genre]["left"] for genre in genres])

    return top, left
