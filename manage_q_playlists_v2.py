from lib.playlist_utils import clear_playlist, tracks_from_playlist
from lib.user import User
from lib.utils import take_x_at_a_time

CANDIDATES_ID = "5AZxg3qZIC7cGnxWa7EuSd"
Q_ALL_ID = "4Mr3AVGL2jGI4Jc2qr3PLf"
REJECTS_ID = "2Cm0uu5nAGb1ISfXPluvks"


def add_tracks_to_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    for to_add in take_x_at_a_time(tracks, 100):
        user.sp.user_playlist_add_tracks(user.username, playlist_id, to_add)


def remove_tracks_from_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    for to_remove in take_x_at_a_time(tracks, 100):
        user.sp.user_playlist_remove_all_occurrences_of_tracks(
            user.username, playlist_id, to_remove
        )


user = User()

# Get playlist tracks
print("Getting tracks...")

candidates = set(tracks_from_playlist(CANDIDATES_ID)(user))

q_all_tracks = set(tracks_from_playlist(Q_ALL_ID)(user))

rejects = set(tracks_from_playlist(REJECTS_ID)(user))

user_tracks = set(user.all_tracks())

# Add candidates to 'q - all'
candidates_to_add = candidates - q_all_tracks

print(f"Adding {len(candidates_to_add):,} candidates...")

add_tracks_to_playlist(Q_ALL_ID, tracks=candidates_to_add, user=user)

q_all_tracks |= candidates_to_add

clear_playlist(CANDIDATES_ID, user=user)

# Remove rejects from 'q - all'
rejects_to_remove = rejects & q_all_tracks

print(f"Removing {len(rejects_to_remove):,} rejects...")

remove_tracks_from_playlist(Q_ALL_ID, tracks=rejects_to_remove, user=user)

q_all_tracks -= rejects_to_remove

clear_playlist(REJECTS_ID, user=user)

# Remove already-saved from 'q - all'
already_saved_to_remove = q_all_tracks & user_tracks

print(f"Removing {len(already_saved_to_remove):,} already-saved tracks...")

remove_tracks_from_playlist(Q_ALL_ID, tracks=already_saved_to_remove, user=user)

q_all_tracks -= already_saved_to_remove