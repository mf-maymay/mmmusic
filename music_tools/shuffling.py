# -*- coding: utf-8 -*-
from collections import Counter
from typing import Any, Callable, Dict, Optional, Sequence, Tuple

import numpy as np
from scipy.stats import percentileofscore

from music_tools.album import Album
from music_tools.genre_positions import genre_position
from music_tools.track import Track

Item = Any
Items = Sequence[Item]
ItemPicker = Callable[[Item, Item, Item, Items], bool]
Metrics = Sequence[float]
SeedPicker = Callable[[Items, Optional[Item]], Tuple[Item, Item]]
Tracks = Sequence[Track]


MAX_SMOOTH_CYCLES = 30

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


def quick_pick(
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
    left: Item, right: Item, to_add: Item, values: Dict[Item, Metrics]
) -> Dict[str, Metrics]:
    averages = {}

    left_values = [values[x] for x in left]
    averages["left"] = np.average(left_values, axis=0)
    averages["left with new"] = np.average(
        np.vstack((left_values, values[to_add])), axis=0
    )

    right_values = [values[x] for x in right]
    averages["right"] = np.average(right_values, axis=0)
    averages["right with new"] = np.average(
        np.vstack((right_values, values[to_add])), axis=0
    )

    return averages


def _get_categorical_scores(
    left: Item, right: Item, to_add: Item
) -> Dict[str, Metrics]:
    scores = {}

    # key, mode, artist
    left_values = [
        sum(track["key"] == to_add["key"] for track in left),
        sum(track["mode"] == to_add["mode"] for track in left),
        sum(track.artist_ids[0] == to_add.artist_ids[0] for track in left),
    ]
    scores["left"] = [x / len(left) for x in left_values]
    scores["left with new"] = [(x + 1) / (len(left) + 1) for x in left_values]

    right_values = [
        sum(track["key"] == to_add["key"] for track in right),
        sum(track["mode"] == to_add["mode"] for track in right),
        sum(track.artist_ids[0] == to_add.artist_ids[0] for track in right),
    ]
    scores["right"] = [x / len(right) for x in right_values]
    scores["right with new"] = [(x + 1) / (len(right) + 1) for x in right_values]

    return scores


def _scores(
    items: Items, metrics_func: Callable[[Item], Metrics]
) -> Dict[Item, Metrics]:
    metrics = np.array([metrics_func(item) for item in items])

    scores = metrics.copy()
    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]

    return dict(zip(items, scores))


def _balanced_metrics(track: Track) -> Metrics:
    return [track[metric] for metric in METRICS] + [
        track["duration_ms"],
        int(Album(track.album_id).release_date.split("-")[0]),
        *genre_position(track),
    ]


def _balanced_picker(tracks: Tracks) -> ItemPicker:
    values = _scores(tracks, _balanced_metrics)

    def picker(left: Track, right: Track, to_add: Track, items: Tracks) -> bool:
        # add item to left if diff less with item in left than in right
        averages = _get_average_values(left, right, to_add, values)
        scores = _get_categorical_scores(left, right, to_add)
        return similarity(
            np.append(averages["left with new"], scores["left with new"]),
            np.append(averages["right"], scores["right"]),
        ) > similarity(
            np.append(averages["left"], scores["left"]),
            np.append(averages["right with new"], scores["right with new"]),
        )

    return picker


def _story_metrics(track: Track) -> Metrics:
    return [track[metric] for metric in METRICS] + [
        int(Album(track.album_id).release_date.split("-")[0]),
        *genre_position(track),
    ]


def _story_picker(tracks: Tracks) -> ItemPicker:
    values = _scores(tracks, _story_metrics)

    def picker(left: Track, right: Track, to_add: Track, items: Tracks) -> bool:
        # maximize polarity
        averages = _get_average_values(left, right, to_add, values)
        return similarity(averages["left with new"], averages["right"]) < similarity(
            averages["left"], averages["right with new"]
        )

    return picker


def _artists_of_tracks(tracks: Tracks) -> Dict[Track, int]:
    """Identifies artists of tracks and counts each artist's appearances."""
    artists = Counter()
    for track in tracks:
        artists.update(track.artist_ids)
    return artists


def _smart_picker(tracks: Tracks) -> ItemPicker:
    balanced_picker = _balanced_picker(tracks)
    story_picker = _story_picker(tracks)

    def picker(left: Track, right: Track, to_add: Track, items: Tracks) -> bool:
        artist_counts = _artists_of_tracks(items)

        # If any tracks share artists, use balanced picker.
        if any(count > 1 for count in artist_counts.values()):
            return balanced_picker(left, right, to_add, items)

        # If all tracks have unique artists, use story picker.
        return story_picker(left, right, to_add, items)

    return picker


def _radio_picker(tracks: Tracks) -> ItemPicker:
    story_picker = _story_picker(tracks)

    def picker(left: Track, right: Track, to_add: Track, items: Tracks) -> bool:
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


def _swap_to_smooth(
    track_0: Track, track_1: Track, track_2: Track, *, values: Dict[Track, Metrics]
) -> bool:
    # if 0 and 1 share artists and 0 and 2 do not, swap
    # if vice versa, keep
    artists_0 = set(track_0.artist_ids)
    artists_1 = set(track_1.artist_ids)
    artists_2 = set(track_2.artist_ids)

    swap_for_artists = (artists_0 & artists_1) and not (artists_0 & artists_2)

    keep_for_artists = (artists_0 & artists_2) and not (artists_0 & artists_1)

    if swap_for_artists:
        return True
    if keep_for_artists:
        return False

    # if key of 1 is inappropriate for 0 and the key of 2 is appropriate, swap
    # if vice versa, keep
    good_keys = (
        track_0["key"]
        + (
            np.array([0, 2, 4, 5, 7, 9, 11])
            if track_0["mode"]
            else np.array([0, 2, 3, 5, 7, 8, 10])
        )
        % 12
    )
    good_modes = (1, 0, 0, 1, 1, 0, 0) if track_0["mode"] else (0, 0, 1, 0, 0, 1, 1)

    swap_for_key = (track_1["key"], track_1["mode"]) not in zip(
        good_keys, good_modes
    ) and (track_2["key"], track_2["mode"],) in zip(good_keys, good_modes)

    keep_for_key = (track_2["key"], track_2["mode"]) not in zip(
        good_keys, good_modes
    ) and (track_1["key"], track_1["mode"],) in zip(good_keys, good_modes)

    if swap_for_key:
        return True
    if keep_for_key:
        return False

    # if 0 and 2 are more similar than 0 and 1
    cos_0_1 = similarity(values[track_0], values[track_1])
    cos_0_2 = similarity(values[track_0], values[track_2])

    swap_for_cosine = cos_0_2 > cos_0_1

    return swap_for_cosine


def smooth_playlist(tracks: Tracks) -> Tracks:
    tracks = list(tracks)

    if len(tracks) <= 2:
        return tracks

    cycle_len = len(tracks)
    swap_count = 0
    last_swap = 0

    scores_for_swaps = _scores(tracks, _story_metrics)

    for i in range(MAX_SMOOTH_CYCLES * cycle_len - 2):
        if _swap_to_smooth(
            tracks[i % cycle_len],
            tracks[(i + 1) % cycle_len],
            tracks[(i + 2) % cycle_len],
            values=scores_for_swaps,
        ):
            tracks[(i + 1) % cycle_len], tracks[(i + 2) % cycle_len] = (
                tracks[(i + 2) % cycle_len],
                tracks[(i + 1) % cycle_len],
            )
            last_swap = i
            swap_count += 1

        elif i - last_swap > cycle_len:
            break

    print(f"smoothed after {i // cycle_len} cycles and {swap_count} swaps")

    return tracks


def smart_shuffle(tracks: Tracks, mode: str = "smart", smooth: Optional[bool] = None):
    # smooth defaults to True except for radio mode

    tracks = list(tracks)

    seed_picker = None

    if mode == "balanced":
        picker = _balanced_picker(tracks)
    elif mode == "radio":
        picker = _radio_picker(tracks)
        seed_picker = _smart_seed_picker(tracks)
        if smooth is None:
            smooth = False  # Don't smooth by default for radio mode
    elif mode == "smart":
        picker = _smart_picker(tracks)
    elif mode == "story":
        picker = _story_picker(tracks)
    else:
        raise ValueError("Invalid mode")

    if smooth is None:
        smooth = True

    ordered = quick_pick(tracks, picker, seed_picker=seed_picker)

    if smooth:
        return smooth_playlist(ordered)

    return ordered


if __name__ == "__main__":
    tracks = [
        Track(x)
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
