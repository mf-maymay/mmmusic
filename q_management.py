# -*- coding: utf-8 -*-
from math import ceil
from playlist_utils import all_user_tracks, tracks_from_playlist
from user import User

DUMP_ID = "93656e7638db4b2a"

Q_IDS = {
    "q - harder": "5mRa71QUmE6EWavxTA22g6",
    "q - hop": "0sFhYQaTiuZlG1vMDSiFMR",
    "q - jazz": "4HQnus8hcLfX5pYtG95pKY",
    "q - misc": "7DOqATuWsl640ustK8lhhI"
}

user = User(input("username: "))
user.setup_sp(scope="playlist-modify-private")


# TODO: dump flush


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
