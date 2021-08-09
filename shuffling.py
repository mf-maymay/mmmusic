# -*- coding: utf-8 -*-
from functools import partial
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import percentileofscore

MAX_SMOOTH_CYCLES = 30

STORY_METRICS = (
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

BALANCE_METRICS = STORY_METRICS + ("key", "mode")

shuffle = np.random.default_rng().shuffle


def quick_pick(items: list, add_to_left: callable) -> list:
    items = list(items)  # XXX

    if len(items) > 1:
        shuffle(items)

    if len(items) <= 2:
        return items

    left = [items.pop()]
    right = [items.pop()]

    for item in items:
        if add_to_left(left, right, item):
            left.append(item)
        else:
            right.append(item)

    return quick_pick(left, add_to_left) + quick_pick(right, add_to_left)


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


def _balanced_picker(left, right, to_add, values) -> bool:
    # add item to left if diff less with item in left than in right
    averages = _get_average_values(left, right, to_add, values)
    return cosine(averages["left with new"], averages["right"]) < cosine(
        averages["left"], averages["right with new"]
    )


def _story_picker(left, right, to_add, values) -> bool:
    # maximize polarity
    averages = _get_average_values(left, right, to_add, values)
    return cosine(averages["left with new"], averages["right"]) > cosine(
        averages["left"], averages["right with new"]
    )


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


def smart_shuffle(tracks, mode="balanced", use_scores=True):
    tracks = list(tracks)  # XXX

    if mode not in ("balanced", "story"):
        raise ValueError("Invalid mode")

    if mode == "balanced":
        picker = _balanced_picker
        metrics = np.array(
            [[track[metric] for metric in BALANCE_METRICS] for track in tracks]
        )
    else:
        picker = _story_picker
        metrics = np.array(
            [[track[metric] for metric in STORY_METRICS] for track in tracks]
        )

    if use_scores:
        values = _scores(tracks, metrics)
    else:
        values = dict(zip(tracks, metrics))

    func = partial(picker, values=values)

    order = quick_pick(tracks, func)

    # playlist smoothing
    cycle_len = len(order)

    last_swap = 0

    for i in range(MAX_SMOOTH_CYCLES * cycle_len - 2):
        if _swap_to_smooth(
            order[i % cycle_len],
            order[(i + 1) % cycle_len],
            order[(i + 2) % cycle_len],
            values=values,
        ):
            order[(i + 1) % cycle_len], order[(i + 2) % cycle_len] = (
                order[(i + 2) % cycle_len],
                order[(i + 1) % cycle_len],
            )
            last_swap = i

        elif i - last_swap > cycle_len:
            print(f"final swap after {i // cycle_len} cycles")
            break
    else:
        print("max smooth cycles reached")

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
