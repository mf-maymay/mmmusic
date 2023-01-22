from contextlib import contextmanager
from datetime import datetime as dt

from lib.playlist_utils import (
    add_tracks_to_playlist,
    clear_playlist,
    get_tracks_from_playlist,
    remove_tracks_from_playlist,
    shuffle_playlist,
)
from lib.user import User


@contextmanager
def note_when_done(message: str):
    print(message, end="", flush=True)
    start = dt.now()
    yield
    total_secs = (dt.now() - start).total_seconds()
    total_mins, secs = divmod(int(total_secs), 60)
    hours, mins = divmod(total_mins, 60)
    print(f" Done. (Took {hours}h {mins}m {secs}s.)")


CANDIDATES_ID = "5AZxg3qZIC7cGnxWa7EuSd"
Q_ALL_ID = "4Mr3AVGL2jGI4Jc2qr3PLf"
REJECTS_ID = "2Cm0uu5nAGb1ISfXPluvks"

user = User()

# Get playlist tracks
with note_when_done("Getting tracks..."):
    candidates = set(get_tracks_from_playlist(CANDIDATES_ID, user=user))

    q_all_tracks = set(get_tracks_from_playlist(Q_ALL_ID, user=user))

    rejects = set(get_tracks_from_playlist(REJECTS_ID, user=user))

    user_tracks = set(user.all_tracks())

# Add candidates to 'q - all'
candidates_to_add = candidates - q_all_tracks

with note_when_done(f"Adding {len(candidates_to_add):,} candidates..."):
    add_tracks_to_playlist(Q_ALL_ID, tracks=candidates_to_add, user=user)

q_all_tracks |= candidates_to_add

clear_playlist(CANDIDATES_ID, user=user)

# Remove rejects from 'q - all'
rejects_to_remove = rejects & q_all_tracks

with note_when_done(f"Removing {len(rejects_to_remove):,} rejects..."):
    remove_tracks_from_playlist(Q_ALL_ID, tracks=rejects_to_remove, user=user)

q_all_tracks -= rejects_to_remove

clear_playlist(REJECTS_ID, user=user)

# Remove already-saved from 'q - all'
already_saved_to_remove = q_all_tracks & user_tracks

with note_when_done(
    f"Removing {len(already_saved_to_remove):,} already-saved tracks..."
):
    remove_tracks_from_playlist(Q_ALL_ID, tracks=already_saved_to_remove, user=user)

q_all_tracks -= already_saved_to_remove

# Shuffle 'q - all'
with note_when_done("Shuffing 'q - all'..."):
    shuffle_playlist(Q_ALL_ID, user=user)
