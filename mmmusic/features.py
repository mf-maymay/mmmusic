from typing import Callable

import numpy as np
from scipy.stats import percentileofscore

from mmmusic.genres import get_genre_attributes_for_track
from mmmusic.logging import get_logger
from mmmusic.models.albums import get_album
from mmmusic.models.tracks import Track
from mmmusic.models.types import Item, Items, Metrics

logger = get_logger()

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
    try:
        return [
            *(track[feature] for feature in TRACK_FEATURES),
            int(get_album(track.album_id).release_date.year),
            *get_genre_attributes_for_track(track),
        ]
    except Exception:
        logger.exception(f"Failed to get metrics for track {track!r}")
        raise


def get_percentile_scores_for_attributes_of_items(
    items: Items, *, item_attributes_func: Callable[[Item], Metrics]
) -> dict[Item, Metrics]:
    metrics = np.array([item_attributes_func(item) for item in items])
    scores = metrics.copy()

    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]

    return dict(zip(items, scores))


def get_scores_for_tracks(tracks: list[Track]) -> dict[Track, Metrics]:
    return get_percentile_scores_for_attributes_of_items(
        tracks, item_attributes_func=get_metrics_for_track
    )
