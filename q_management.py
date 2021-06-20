# -*- coding: utf-8 -*-
from math import ceil
import re
import pandas as pd
from album import Album
from artist import Artist
from playlist_utils import all_user_tracks, tracks_from_playlist
from user import User

DUMP_ID = "5AZxg3qZIC7cGnxWa7EuSd"

Q_IDS = {
    "q - harder": "5mRa71QUmE6EWavxTA22g6",
    "q - hop": "0sFhYQaTiuZlG1vMDSiFMR",
    "q - jazz": "4HQnus8hcLfX5pYtG95pKY",
    "q - misc": "7DOqATuWsl640ustK8lhhI"
}

Q_PATTERNS = [
    ("q - hop", ".*hop.*"),
    ("q - harder", ".*(core|doom|metal|punk).*"),
    ("q - jazz", ".*jazz.*")
]

user = User(input("username: "))
user.setup_sp(scope="playlist-modify-private")


# TODO: dump flush
dump_tracks = tracks_from_playlist(DUMP_ID)(user)
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
dump_frame.loc[dump_frame["playlist"].isna(), "playlist"] = "q - misc"


# remove already-saved items from q playlists
user_tracks = set(all_user_tracks(user))

q_tracks = {
    q: set(tracks_from_playlist(q_id)(user))
    for q, q_id in Q_IDS.items()
}

for q, q_id in Q_IDS.items():
    tracks = [track.id for track in q_tracks[q] & user_tracks]
    for i in range(ceil(len(tracks) / 100)):
        to_remove = tracks[(100 * i):(100 * (i + 1))]
        user.sp.playlist_remove_all_occurrences_of_items(
            q_id,
            to_remove
        )
    print(f"Cleaned '{q}'")


# TODO: shuffle q playlists
