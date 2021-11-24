# -*- coding: utf-8 -*-
import random
import re

import pandas as pd

from music_tools.album import Album, get_tracks_from_albums
from music_tools.artist import Artist
from music_tools.shuffling import smart_shuffle
from music_tools.playlist_utils import (
    clear_playlist,
    shuffle_playlist,
    tracks_from_playlist,
)
from music_tools.user import User
from music_tools.utils import take_x_at_a_time

DUMP_ID = "5AZxg3qZIC7cGnxWa7EuSd"

REVIEW_ID = "6P9AB5NtkXBmQxnTqFFoZK"

Q_IDS = {
    "q - harder": "5mRa71QUmE6EWavxTA22g6",
    "q - hop": "0sFhYQaTiuZlG1vMDSiFMR",
    "q - jazz": "4HQnus8hcLfX5pYtG95pKY",
    "q - misc": "7DOqATuWsl640ustK8lhhI",
    "q - rock": "1tlzpLpRdQXUicLbhIJMcM",
}

Q_PATTERNS = [
    ("q - hop", ".*hop.*"),
    ("q - harder", ".*(core|doom|metal|punk).*"),
    ("q - jazz", ".*jazz.*"),
    ("q - rock", ".*rock.*"),
]


user = User()


def refresh_review_playlist():
    print("Picking random albums for 'review' playlist")
    random_albums = random.choices(user.albums(), k=12)
    review_tracks = get_tracks_from_albums(random_albums)

    print("Clearing 'review' playlist")
    clear_playlist(user, REVIEW_ID)

    print("Shuffling 'review' tracks")
    shuffled = smart_shuffle(review_tracks)

    print("Adding shuffled tracks to 'review'")
    for subset in take_x_at_a_time(shuffled, 100):
        to_add = [track.id for track in subset]
        user.sp.user_playlist_add_tracks(user._username, REVIEW_ID, to_add)


# Identify playlists for tracks
def separate_dump_tracks_to_q_playlists():
    print("Identifying 'dump' tracks")
    dump_tracks = tracks_from_playlist(DUMP_ID)(user)  # XXX

    print(f"Found {len(dump_tracks)} tracks in 'dump' playlist")

    if not dump_tracks:
        return

    print("Mapping tracks to 'q' playlists")

    dump_frame = pd.DataFrame()
    dump_frame["track"] = dump_tracks
    dump_frame["id"] = [track.id for track in dump_frame["track"]]
    dump_frame["album"] = [Album(track.album_id) for track in dump_frame["track"]]
    dump_frame["genres"] = [
        tuple(
            sorted(
                set(
                    genre
                    for artist_id in album.artist_ids
                    for genre in Artist(artist_id).genres
                )
            )
        )
        for album in dump_frame["album"]
    ]
    dump_frame["playlist"] = None

    for q, pattern in Q_PATTERNS:
        print(f"Identifying '{q}' tracks")
        compiled = re.compile(pattern)
        dump_frame["playlist"] = [
            playlist
            if pd.notna(playlist)
            else q
            if any(map(compiled.fullmatch, genres))
            else None
            for playlist, genres in zip(dump_frame["playlist"], dump_frame["genres"])
        ]

    print("Identifying 'q - misc' tracks")
    dump_frame.loc[dump_frame["playlist"].isna(), "playlist"] = "q - misc"

    # Add tracks to playlists
    for q, q_id in Q_IDS.items():
        tracks = list(dump_frame.loc[dump_frame["playlist"] == q, "id"].values)
        print(f"Adding {len(tracks)} tracks to '{q}'")
        for to_add in take_x_at_a_time(tracks, 100):
            user.sp.user_playlist_add_tracks(user._username, q_id, to_add)
        print(f"Added tracks to '{q}'")

    # Clear dump
    print("Clearing dump")
    clear_playlist(user, DUMP_ID)
    print("Cleared dump")


def prepare_q_playlists():
    user_tracks = set(user.all_tracks())

    user.setup_sp(scope="playlist-modify-private")  # XXX

    for q, q_id in Q_IDS.items():
        tracks = [
            track.id for track in set(tracks_from_playlist(q_id)(user)) & user_tracks
        ]

        print(f"Removing {len(tracks)} saved tracks from '{q}'")
        for to_remove in take_x_at_a_time(tracks, 100):
            user.sp.user_playlist_remove_all_occurrences_of_tracks(
                user._username, q_id, to_remove
            )

        print(f"Cleaned '{q}'")

        print(f"Shuffling '{q}'")
        shuffle_playlist(user, q_id)

        print(f"Shuffled '{q}'")


if __name__ == "__main__":
    refresh_review_playlist()

    separate_dump_tracks_to_q_playlists()

    prepare_q_playlists()
