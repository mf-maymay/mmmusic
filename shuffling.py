# -*- coding: utf-8 -*-
from functools import partial
from random import shuffle
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import percentileofscore


METRICS = ("danceability", "energy", "key", "loudness", "mode",
           "speechiness", "acousticness", "instrumentalness", "liveness",
           "valence", "tempo")


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


def picker(left, right, item):
    # add item to left if diff less with item in left than in right
    left_score = np.average(left, 0)
    left_score_with_item = np.average(np.vstack((left, item)), 0)
    right_score = np.average(right, 0)
    right_score_with_item = np.average(np.vstack((right, item)), 0)

    left_less_diff = (cosine(left_score_with_item, right_score)
                      < cosine(left_score, right_score_with_item))

    return left_less_diff


def song_picker(left, right, item, item_scores):
    return picker([item_scores[x] for x in left],
                  [item_scores[x] for x in right],
                  item_scores[item])


def swap_to_smooth(track_0, track_1, track_2, *, item_scores, features):
    # if 0 and 1 share artists and 0 and 2 do not
    artists_0 = set(track_0.artist_ids)
    artist_cause = (
        (artists_0 & set(track_1.artist_ids))
        and not (artists_0 & set(track_2.artist_ids))
    )

    # if 0 and 2 are (significantly) more similar than 0 and 1
    cosine_cause = (
        cosine(item_scores[track_0], item_scores[track_2])
        - cosine(item_scores[track_0], item_scores[track_1])
    ) > 0.1

    # if key of 1 is inappropriate for 0 and the key of 2 is appropriate
    good_keys = features[track_0]["key"] + (
        np.array([0, 2, 4, 5, 7, 9, 11]) if features[track_0]["mode"]
        else np.array([0, 2, 3, 5, 7, 8, 10])
    ) % 12
    good_modes = (
        (1, 0, 0, 1, 1, 0, 0) if features[track_0]["mode"]
        else (0, 0, 1, 0, 0, 1, 1)
    )
    key_cause = (
        (features[track_1]["key"], features[track_1]["mode"])
        not in zip(good_keys, good_modes)
        and (features[track_2]["key"], features[track_2]["mode"])
        in zip(good_keys, good_modes)
    )

    return artist_cause or cosine_cause or key_cause


def order_tracks(tracks, user):
    features = {track: track.audio_features() for track in tracks}
    metrics = np.array([[features[track][metric] for metric in METRICS]
                        for track in tracks])
    scores = metrics.copy()  # XXX
    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]

    track_scores = dict(zip(tracks, scores))

    func = partial(song_picker, item_scores=track_scores)

    order = quick_pick(tracks, func)

    # playlist smoothing
    num = len(order)

    for i in range(4 * num - 2):
        if swap_to_smooth(
            order[i % num],
            order[(i + 1) % num],
            order[(i + 2) % num],
            item_scores=track_scores,
            features=features
        ):
            order[(i + 1) % num], order[(i + 2) % num] = (
                order[(i + 2) % num],
                order[(i + 1) % num]
            )

    return order


if __name__ == "__main__":
    from user import User
    user = User(input("username: "))

    songs = ["0vFabeTqtOtj918sjc5vYo", "3HWxpLKnTlz6jE3Vi5dTF2",
             "6PSma9xvYhGabJNrbUAE4e", "3qSJD2hjnZ7YDOQx9ieQ0m",
             "09uV1Sli9wapcKQmmyaG4E", "5vaCmKjItq2Da5BKNFHlEb"]

    ordered = order_tracks(songs, user)
