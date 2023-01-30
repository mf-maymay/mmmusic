import numpy as np

from lib.genres import get_track_genre_attributes
from lib.models.album import Album, get_album, get_album_tracks
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


def get_metrics_for_album(album: Album) -> Metrics:
    return np.mean(
        [get_metrics_for_track(track) for track in get_album_tracks(album)], axis=0
    )


if __name__ == "__main__":
    album = get_album("2Ul7B1LEHxXzYubtkTMENs")

    album_metrics = get_metrics_for_album(album)
