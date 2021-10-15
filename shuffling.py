# -*- coding: utf-8 -*-
from collections import Counter
import json

import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import percentileofscore

from album import Album
from artist import Artist

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

with open("genre_positions.json") as f:
    _GENRE_POSITIONS = json.load(f)

_DEFAULT_TOP = np.mean([pos["top"] for pos in _GENRE_POSITIONS.values()])
_DEFAULT_LEFT = np.mean([pos["left"] for pos in _GENRE_POSITIONS.values()])


def quick_pick(
    items: list, add_to_left: callable, seed_picker: callable = None, left_neighbor=None
) -> list:
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


def _get_categorical_scores(left, right, to_add) -> dict:
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


def _scores(tracks, metrics_func):
    metrics = np.array([metrics_func(track) for track in tracks])
    scores = metrics.copy()
    for j, col in enumerate(metrics.T):
        scores[:, j] = [percentileofscore(col, x, kind="mean") for x in col]
    return dict(zip(tracks, scores))


def _genre_position(track):
    genres = set()
    for artist in track.artist_ids:
        genres |= Artist(artist).genres & _GENRE_POSITIONS.keys()

    if not genres:
        return _DEFAULT_TOP, _DEFAULT_LEFT

    top = np.mean([_GENRE_POSITIONS[genre]["top"] for genre in genres])
    left = np.mean([_GENRE_POSITIONS[genre]["left"] for genre in genres])
    return top, left


def _balanced_metrics(track):
    return [track[metric] for metric in METRICS] + [
        track["duration_ms"],
        int(Album(track.album_id)["release_date"].split("-")[0]),
        *_genre_position(track),
    ]


def _balanced_picker(tracks):
    values = _scores(tracks, _balanced_metrics)

    def picker(left, right, to_add, items) -> bool:
        # add item to left if diff less with item in left than in right
        averages = _get_average_values(left, right, to_add, values)
        scores = _get_categorical_scores(left, right, to_add)
        return cosine(
            np.append(averages["left with new"], scores["left with new"]),
            np.append(averages["right"], scores["right"]),
        ) < cosine(
            np.append(averages["left"], scores["left"]),
            np.append(averages["right with new"], scores["right with new"]),
        )

    return picker


def _story_metrics(track):
    return [track[metric] for metric in METRICS] + [
        int(Album(track.album_id)["release_date"].split("-")[0]),
        *_genre_position(track),
    ]


def _story_picker(tracks, values=None):
    if values is None:
        values = _scores(tracks, _story_metrics)

    def picker(left, right, to_add, items) -> bool:
        # maximize polarity
        averages = _get_average_values(left, right, to_add, values)
        return cosine(averages["left with new"], averages["right"]) > cosine(
            averages["left"], averages["right with new"]
        )

    return picker


def _genre_picker(tracks):
    genre_picker = _story_picker(tracks, values=_scores(tracks, _genre_position))
    story_picker = _story_picker(tracks)

    ms_per_3_hours = 3.6e6 * 3

    def picker(left, right, to_add, items) -> bool:
        total_duration = sum(track["duration_ms"] for track in items)
        if total_duration > ms_per_3_hours:
            return genre_picker(left, right, to_add, items)
        return story_picker(left, right, to_add, items)

    return picker


def _smart_picker(tracks, story_picker=None):
    balanced_picker = _balanced_picker(tracks)

    if story_picker is None:
        story_picker = _story_picker(tracks)

    def picker(left, right, to_add, items) -> bool:
        artists_seen = set()
        for track in items:
            artists = set(track.artist_ids)
            if artists & artists_seen:
                return balanced_picker(left, right, to_add, items)
            artists_seen.update(artists)
        return story_picker(left, right, to_add, items)

    return picker


def _radio_picker(tracks):
    genre_picker = _genre_picker(tracks)

    return _smart_picker(tracks, story_picker=genre_picker)


def _test_picker(tracks):
    story_picker = _story_picker(tracks)
    smart_picker = _smart_picker(tracks)

    def picker(left, right, to_add, items) -> bool:
        if len(items) > 100:
            return story_picker(left, right, to_add, items)
        return smart_picker(left, right, to_add, items)

    return picker


def _artists_of_tracks(tracks):
    artists = Counter()
    for track in tracks:
        artists.update(track.artist_ids)
    return artists


def _smart_story_picker(tracks):
    story_picker = _story_picker(tracks)

    def picker(left, right, to_add, items) -> bool:
        left_artists = _artists_of_tracks(left)
        right_artists = _artists_of_tracks(right)

        primary_artist = to_add.artist_ids[0]  # XXX: assumes first is primary
        primary_in_left = left_artists.get(primary_artist, 0)
        primary_in_right = right_artists.get(primary_artist, 0)

        if primary_in_left != primary_in_right:
            return primary_in_left < primary_in_right

        return story_picker(left, right, to_add, items)

    return picker


def _smart_seed_picker(tracks):
    values = _scores(tracks, _story_metrics)

    def picker(items, left_neighbor):

        if left_neighbor is None:
            left_seed = items[0]
        else:
            # Pick item most similar to left neighbor
            neighbor_value = values[left_neighbor]
            left_seed = min(
                items, key=lambda item: cosine(neighbor_value, values[item])
            )

        # Pick item least similar to left seed
        left_value = values[left_seed]
        right_seed = max(items, key=lambda item: cosine(left_value, values[item]))

        return left_seed, right_seed

    return picker


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

    # if 0 and 2 are more similar than 0 and 1
    cos_0_1 = cosine(values[track_0], values[track_1])
    cos_0_2 = cosine(values[track_0], values[track_2])

    swap_for_cosine = cos_0_2 > cos_0_1

    return swap_for_cosine


def smooth_playlist(tracks):
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


def smart_shuffle(tracks, mode="smart", smooth=True):
    tracks = list(tracks)

    seed_picker = None

    if mode == "balanced":
        picker = _balanced_picker(tracks)
    elif mode == "genre":
        picker = _genre_picker(tracks)
    elif mode == "radio":
        picker = _radio_picker(tracks)
    elif mode == "smart":
        picker = _smart_picker(tracks)
    elif mode == "smart-story":
        picker = _smart_story_picker(tracks)
        seed_picker = _smart_seed_picker(tracks)
    elif mode == "story":
        picker = _story_picker(tracks)
    elif mode == "test":
        picker = _test_picker(tracks)
    else:
        raise ValueError("Invalid mode")

    ordered = quick_pick(tracks, picker, seed_picker=seed_picker)

    if smooth:
        return smooth_playlist(ordered)

    return ordered


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

    ordered = smart_shuffle(tracks, mode="smart-story")
