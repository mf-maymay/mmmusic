from typing import Callable

import numpy as np
from scipy.stats import percentileofscore

from lib.genres import get_track_genre_attributes
from lib.models.albums import get_album
from lib.models.tracks import Track
from lib.types import Item, Items, Metrics, Tracks

TRACK_FEATURES = (
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
)


def similarity(u: Metrics, v: Metrics) -> float:
    """Calculates the cosine similarity of two vectors."""
    return np.dot(u, v) / np.sqrt(np.dot(u, u) * np.dot(v, v))


def get_metrics_for_track(track: Track) -> Metrics:
    return [
        *(track[feature] for feature in TRACK_FEATURES),
        int(get_album(track.album_id).release_date.year),
        *get_track_genre_attributes(track),
    ]


def get_percentile_scores_for_attributes_of_items(
    items: Items, *, item_attributes_func: Callable[[Item], Metrics]
) -> dict[Item, Metrics]:
    metrics = np.array([item_attributes_func(item) for item in items])
    scores = metrics.copy()

    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]

    return dict(zip(items, scores))


def get_scores_for_tracks(tracks: Tracks) -> dict[Track, Metrics]:
    return get_percentile_scores_for_attributes_of_items(
        tracks, item_attributes_func=get_metrics_for_track
    )
