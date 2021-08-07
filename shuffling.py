# -*- coding: utf-8 -*-
from functools import partial
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import percentileofscore
from track import get_audio_features

MAX_SMOOTH_CYCLES = 20

METRICS = (
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
)

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


def _get_average_values(left, right, to_add, values):
    # add item to left if diff less with item in left than in right
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


def _picker(left, right, to_add, values):
    averages = _get_average_values(left, right, to_add, values)
    return cosine(averages["left with new"], averages["right"]) < cosine(
        averages["left"], averages["right with new"]
    )


def _swap_to_smooth(track_0, track_1, track_2, *, item_scores, features):
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
        features[track_0]["key"]
        + (
            np.array([0, 2, 4, 5, 7, 9, 11])
            if features[track_0]["mode"]
            else np.array([0, 2, 3, 5, 7, 8, 10])
        )
        % 12
    )
    good_modes = (
        (1, 0, 0, 1, 1, 0, 0) if features[track_0]["mode"] else (0, 0, 1, 0, 0, 1, 1)
    )
    key_1 = features[track_1]["key"]
    mode_1 = features[track_1]["mode"]
    key_2 = features[track_2]["key"]
    mode_2 = features[track_2]["mode"]

    swap_for_key = (key_1, mode_1) not in zip(good_keys, good_modes) and (
        key_2,
        mode_2,
    ) in zip(good_keys, good_modes)

    keep_for_key = (key_2, mode_2) not in zip(good_keys, good_modes) and (
        key_1,
        mode_1,
    ) in zip(good_keys, good_modes)

    if swap_for_key:
        return True
    if keep_for_key:
        return False

    # if 0 and 2 are (significantly) more similar than 0 and 1
    cos_0_1 = cosine(item_scores[track_0], item_scores[track_1])
    cos_0_2 = cosine(item_scores[track_0], item_scores[track_2])

    swap_for_cosine = cos_0_2 - cos_0_1 > 0.1

    return swap_for_cosine


def smart_shuffle(tracks, user):
    features = dict(zip(tracks, get_audio_features(tracks)))
    metrics = np.array(
        [[features[track][metric] for metric in METRICS] for track in tracks]
    )
    scores = metrics.copy()  # XXX
    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]

    track_scores = dict(zip(tracks, scores))

    func = partial(_picker, values=track_scores)

    order = quick_pick(tracks, func)

    # playlist smoothing
    cycle_len = len(order)

    last_swap = 0

    for i in range(MAX_SMOOTH_CYCLES * cycle_len - 2):
        if _swap_to_smooth(
            order[i % cycle_len],
            order[(i + 1) % cycle_len],
            order[(i + 2) % cycle_len],
            item_scores=track_scores,
            features=features,
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
    from user import User

    user = User(input("username: "))

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

    ordered = smart_shuffle(tracks, user)
