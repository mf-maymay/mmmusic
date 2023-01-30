import numpy as np

from lib.genres import get_track_genre_attributes
from lib.models.album import get_album
from lib.models.track import Track

Metrics = list[float]

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
