from collections import Counter
from typing import Any, Callable, Optional, Tuple

import numpy as np
from scipy.stats import percentileofscore

from lib.genres import get_track_genre_attributes
from lib.models.album import get_album
from lib.models.track import Track, get_track

Item = Any
Items = list[Item]
ItemPicker = Callable[[Items, Items, Item, Items], bool]
Metrics = list[float]
SeedPicker = Callable[[Items, Optional[Item]], Tuple[Item, Item]]
Tracks = list[Track]


METRICS = (
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

_shuffle = np.random.default_rng().shuffle


def similarity(u: Metrics, v: Metrics) -> float:
    """Calculates the cosine similarity of two vectors."""
    return np.dot(u, v) / np.sqrt(np.dot(u, u) * np.dot(v, v))


def quick_pick(  # TODO: separate
    items: Items,
    add_to_left: ItemPicker,
    seed_picker: Optional[SeedPicker] = None,
    left_neighbor: Optional[Item] = None,
) -> Items:
    items = list(items)

    if len(items) < 2:
        return items
    _shuffle(items)

    if seed_picker is None:
        left_seed, right_seed = items[:2]
    else:
        left_seed, right_seed = seed_picker(items, left_neighbor=left_neighbor)
    left = [left_seed]
    right = [right_seed]

    items.remove(left_seed)
    items.remove(right_seed)

    for item in items:
        if add_to_left(left, right, item, items):
            left.append(item)
        else:
            right.append(item)
    # If left_neighbor would not belong to left, then swap left and right.
    if left_neighbor is not None and not add_to_left(left, right, left_neighbor, items):
        left, right = right, left
    new_left = quick_pick(left, add_to_left, seed_picker=seed_picker)
    new_right = quick_pick(
        right, add_to_left, seed_picker=seed_picker, left_neighbor=new_left[-1]
    )

    return new_left + new_right


def _get_average_values(
    left: Item, right: Item, to_add: Item, values: dict[Item, Metrics]
) -> dict[str, Metrics]:
    left_values = [values[x] for x in left]
    right_values = [values[x] for x in right]
    return {
        "left": np.average(left_values, axis=0),
        "left with new": np.average(np.vstack((left_values, values[to_add])), axis=0),
        "right": np.average(right_values, axis=0),
        "right with new": np.average(np.vstack((right_values, values[to_add])), axis=0),
    }


def _scores(
    items: Items, metrics_func: Callable[[Item], Metrics]
) -> dict[Item, Metrics]:
    metrics = np.array([metrics_func(item) for item in items])

    scores = metrics.copy()
    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]
    return dict(zip(items, scores))


def _story_metrics(track: Track) -> Metrics:
    return [track[metric] for metric in METRICS] + [
        int(get_album(track.album_id).release_date.year),
        *get_track_genre_attributes(track),
    ]


def _story_picker(tracks: Tracks) -> ItemPicker:
    values = _scores(tracks, _story_metrics)

    def picker(left: Tracks, right: Tracks, to_add: Track, items: Tracks) -> bool:
        # maximize polarity
        averages = _get_average_values(left, right, to_add, values)
        return similarity(averages["left with new"], averages["right"]) < similarity(
            averages["left"], averages["right with new"]
        )

    return picker


def _artists_of_tracks(tracks: Tracks) -> dict[Track, int]:
    """Identifies artists of tracks and counts each artist's appearances."""
    artists: Counter[Track] = Counter()
    for track in tracks:
        artists.update(track.artist_ids)
    return artists


def _radio_picker(tracks: Tracks) -> ItemPicker:
    story_picker = _story_picker(tracks)

    def picker(left: Tracks, right: Tracks, to_add: Track, items: Tracks) -> bool:
        num_mutual_artists_in_left = sum(
            counts
            for artist, counts in _artists_of_tracks(left).items()
            if artist in to_add.artist_ids
        )
        num_mutual_artists_in_right = sum(
            counts
            for artist, counts in _artists_of_tracks(right).items()
            if artist in to_add.artist_ids
        )

        # If one side has fewer of to_add's artists, add to that side.
        if num_mutual_artists_in_left != num_mutual_artists_in_right:
            return num_mutual_artists_in_left < num_mutual_artists_in_right

        # Otherwise, use story mode.
        return story_picker(left, right, to_add, items)

    return picker


def _smart_seed_picker(tracks: Tracks) -> SeedPicker:
    values = _scores(tracks, _story_metrics)

    def picker(items: Tracks, left_neighbor: Optional[Track]) -> Tuple[Track, Track]:
        if left_neighbor is None:
            left_seed = items[0]
        else:
            # Pick item most similar to left neighbor
            neighbor_value = values[left_neighbor]
            left_seed = max(
                items, key=lambda item: similarity(neighbor_value, values[item])
            )

        # Pick item least similar to left seed
        left_value = values[left_seed]
        right_seed = min(items, key=lambda item: similarity(left_value, values[item]))

        return left_seed, right_seed

    return picker


def smart_shuffle(tracks: Tracks, mode: str = "radio"):
    tracks = list(tracks)

    seed_picker = None

    if mode == "radio":
        picker = _radio_picker(tracks)
        seed_picker = _smart_seed_picker(tracks)
    elif mode == "story":
        picker = _story_picker(tracks)
    else:
        raise ValueError("Invalid mode")

    return quick_pick(tracks, picker, seed_picker=seed_picker)


if __name__ == "__main__":
    tracks = [
        get_track(x)
        for x in [
            "0vFabeTqtOtj918sjc5vYo",
            "3HWxpLKnTlz6jE3Vi5dTF2",
            "6PSma9xvYhGabJNrbUAE4e",
            "3qSJD2hjnZ7YDOQx9ieQ0m",
            "09uV1Sli9wapcKQmmyaG4E",
            "5vaCmKjItq2Da5BKNFHlEb",
        ]
    ]

    ordered = smart_shuffle(tracks, mode="radio")
