# -*- coding: utf-8 -*-
import numpy as np
from pandas import to_datetime
from scipy.spatial.distance import cosine
from scipy.stats import percentileofscore

from album import Album

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

shuffle = np.random.default_rng().shuffle


def quick_pick(items: list, add_to_left: callable, left_neighbor=None) -> list:
    items = list(items)

    if len(items) < 2:
        return items

    shuffle(items)

    left = [items.pop()]
    right = [items.pop()]

    for item in items:
        if add_to_left(left, right, item, items):
            left.append(item)
        else:
            right.append(item)

    # If left_neighbor would not belong to left, then swap left and right.
    if left_neighbor is not None and not add_to_left(left, right, left_neighbor, items):
        left, right = right, left

    new_left = quick_pick(left, add_to_left)
    new_right = quick_pick(right, add_to_left, left_neighbor=new_left[-1])

    return new_left + new_right


def _get_average_values(left, right, to_add, values) -> dict:
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


def _balanced_picker(values):
    def picker(left, right, to_add, items) -> bool:
        # add item to left if diff less with item in left than in right
        averages = _get_average_values(left, right, to_add, values)
        return cosine(averages["left with new"], averages["right"]) < cosine(
            averages["left"], averages["right with new"]
        )

    return picker


def _story_picker(values):
    def picker(left, right, to_add, items) -> bool:
        # maximize polarity
        averages = _get_average_values(left, right, to_add, values)
        return cosine(averages["left with new"], averages["right"]) > cosine(
            averages["left"], averages["right with new"]
        )

    return picker


def _smart_picker(balanced_picker, story_picker):
    def picker(left, right, to_add, items) -> bool:
        artists_seen = set()
        for track in items:
            artists = set(track.artist_ids)
            if artists & artists_seen:
                return balanced_picker(left, right, to_add, items)
            artists_seen.update(artists)
        return story_picker(left, right, to_add, items)

    return picker


def _balanced_metrics(track):
    return [track[metric] for metric in METRICS] + [
        track["key"],
        track["mode"],
        track["duration_ms"],
        to_datetime(Album(track.album_id)["release_date"]).toordinal(),
    ]


def _story_metrics(track):
    return [track[metric] for metric in METRICS]


def _swap_to_smooth(track_0, track_1, track_2, *, values):
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

    # if 0 and 2 are (significantly) more similar than 0 and 1
    cos_0_1 = cosine(values[track_0], values[track_1])
    cos_0_2 = cosine(values[track_0], values[track_2])

    swap_for_cosine = cos_0_2 - cos_0_1 > 0.1

    return swap_for_cosine


def _scores(tracks, metrics):
    scores = metrics.copy()
    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]
    return dict(zip(tracks, scores))


def smart_shuffle(tracks, mode="smart", use_scores=True):
    tracks = list(tracks)  # XXX

    balanced_metrics = np.array([_balanced_metrics(track) for track in tracks])
    story_metrics = np.array([_story_metrics(track) for track in tracks])

    if use_scores:
        balanced_values = _scores(tracks, balanced_metrics)
        story_values = _scores(tracks, story_metrics)
    else:
        balanced_values = dict(zip(tracks, balanced_metrics))
        story_values = dict(zip(tracks, story_metrics))

    balanced_picker = _balanced_picker(balanced_values)
    story_picker = _story_picker(story_values)

    if mode == "balanced":
        picker = balanced_picker
    elif mode == "story":
        picker = story_picker
    elif mode == "smart":
        picker = _smart_picker(balanced_picker, story_picker)
    else:
        raise ValueError("Invalid mode")

    order = quick_pick(tracks, picker)

    if len(order) <= 2:
        return order

    # playlist smoothing
    cycle_len = len(order)
    swap_count = 0
    last_swap = 0

    for i in range(MAX_SMOOTH_CYCLES * cycle_len - 2):
        if _swap_to_smooth(
            order[i % cycle_len],
            order[(i + 1) % cycle_len],
            order[(i + 2) % cycle_len],
            values=balanced_values,
        ):
            order[(i + 1) % cycle_len], order[(i + 2) % cycle_len] = (
                order[(i + 2) % cycle_len],
                order[(i + 1) % cycle_len],
            )
            last_swap = i
            swap_count += 1

        elif i - last_swap > cycle_len:
            break

    print(f"smoothed after {i // cycle_len} cycles and {swap_count} swaps")

    return order


if __name__ == "__main__":
    from track import Track

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

    ordered = smart_shuffle(tracks)
    ordered_by_story_mode = smart_shuffle(tracks, mode="story")
    ordered_by_smart_mode = smart_shuffle(tracks, mode="smart")
