# -*- coding: utf-8 -*-
from math import ceil
import re
import pandas as pd
from album import Album
from artist import Artist
from playlist_utils import (
    all_user_tracks,
    shuffle_playlist,
    tracks_from_playlist
)
from user import User

DUMP_ID = "5AZxg3qZIC7cGnxWa7EuSd"

Q_IDS = {
    "q - harder": "5mRa71QUmE6EWavxTA22g6",
    "q - hop": "0sFhYQaTiuZlG1vMDSiFMR",
    "q - jazz": "4HQnus8hcLfX5pYtG95pKY",
    "q - misc": "7DOqATuWsl640ustK8lhhI",
    "q - rock": "1tlzpLpRdQXUicLbhIJMcM"
}

Q_PATTERNS = [
    ("q - hop", ".*hop.*"),
    ("q - harder", ".*(core|doom|metal|punk).*"),
    ("q - jazz", ".*jazz.*"),
    ("q - rock", ".*rock.*")
]

user = User(input("username: "))
user.setup_sp(scope="playlist-modify-private")


# Identify playlists for tracks
dump_tracks = tracks_from_playlist(DUMP_ID)(user)

print(f"Found {len(dump_tracks)} tracks in 'dump'")
print("Identifying playlists for tracks ...")

dump_frame = pd.DataFrame(dump_tracks)
dump_frame["album"] = [Album(x) for x in dump_frame["album_id"]]
dump_frame["genres"] = [
    tuple(sorted(set(
        genre for artist_id in album.artist_ids
        for genre in Artist(artist_id).genres
    )))
    for album in dump_frame["album"]
]
dump_frame["playlist"] = None

for q, pattern in Q_PATTERNS:
    compiled = re.compile(pattern)
    dump_frame["playlist"] = [
        playlist if pd.notna(playlist)
        else q if any(map(compiled.fullmatch, genres))
        else None
        for playlist, genres in zip(dump_frame["playlist"],
                                    dump_frame["genres"])
    ]
    print(f"Identified '{q}' tracks")

dump_frame.loc[dump_frame["playlist"].isna(), "playlist"] = "q - misc"
print("Identified 'q - misc' tracks")


# Add tracks to playlists
for q, q_id in Q_IDS.items():
    tracks = list(dump_frame.loc[dump_frame["playlist"] == q, "id"].values)
    print(f"Adding {len(tracks)} tracks to '{q}' ...")
    for i in range(ceil(len(tracks) / 100)):
        to_add = tracks[(100 * i):(100 * (i + 1))]
        user.sp.user_playlist_add_tracks(
            user._username,
            q_id,
            to_add
        )
    print(f"Added tracks to '{q}' ...")


# Clear dump
print("Clearing dump ...")
for i in range(ceil(len(dump_tracks) / 100)):
    to_remove = [track.id for track in dump_tracks[(100 * i):(100 * (i + 1))]]
    user.sp.user_playlist_remove_all_occurrences_of_tracks(
        user._username,
        DUMP_ID,
        to_remove
    )
print("Cleared dump")

# Remove already-saved tracks from playlists
print("Identifying saved tracks ...")
user_tracks = set(all_user_tracks(user))

q_tracks = {
    q: set(tracks_from_playlist(q_id)(user))
    for q, q_id in Q_IDS.items()
}

for q, q_id in Q_IDS.items():
    tracks = [track.id for track in q_tracks[q] & user_tracks]
    print(f"Removing {len(tracks)} saved tracks from '{q}' ...")
    for i in range(ceil(len(tracks) / 100)):
        to_remove = tracks[(100 * i):(100 * (i + 1))]
        user.sp.user_playlist_remove_all_occurrences_of_tracks(
            user._username,
            q_id,
            to_remove
        )
    print(f"Cleaned '{q}'")


# Shuffle playlists
for q, q_id in Q_IDS.items():
    print(f"Shuffling '{q}' ...")
    shuffle_playlist(user, q_id)
    print(f"Shuffled '{q}'")
