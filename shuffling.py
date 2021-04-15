# -*- coding: utf-8 -*-
from functools import partial
import random
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import percentileofscore
from utils import get_audio_features


METRICS = ("danceability", "energy", "key", "loudness", "mode",
           "speechiness", "acousticness", "instrumentalness", "liveness",
           "valence", "tempo")


def quick_pick(items: list, add_to_left: callable) -> list:
    items = list(items)  # XXX

    if len(items) > 1:
        random.shuffle(items)

    if len(items) <= 2:
        return items

    left = [items.pop()]
    right = [items.pop()]

    for item in items:
        # value_in_left = abs(character(left + [item]) - character(right))
        # value_in_right = abs(character(left) - character(right + [item]))

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


def order_tracks(tracks, user):
    features = dict(zip(tracks, get_audio_features(user, tracks)))  # XXX
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

    for i in range(2 * num - 2):
        scores_0 = track_scores[order[i % num]]
        scores_1 = track_scores[order[(i + 1) % num]]
        scores_2 = track_scores[order[(i + 2) % num]]

        if cosine(scores_0, scores_2) < cosine(scores_0, scores_1):
            temp = order[(i + 1) % num]
            order[(i + 1) % num] = order[(i + 2) % num]
            order[(i + 2) % num] = temp

    return order


if __name__ == "__main__":
    from user import User
    user = User(input("username: "))  # XXX

    songs = ["0vFabeTqtOtj918sjc5vYo", "3HWxpLKnTlz6jE3Vi5dTF2",
             "6PSma9xvYhGabJNrbUAE4e", "3qSJD2hjnZ7YDOQx9ieQ0m",
             "09uV1Sli9wapcKQmmyaG4E", "5vaCmKjItq2Da5BKNFHlEb"]

    ordered = order_tracks(songs, user)
