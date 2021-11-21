# -*- coding: utf-8 -*-
import json
from pathlib import Path

import numpy as np

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
