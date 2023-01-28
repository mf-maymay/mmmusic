from contextlib import contextmanager
from datetime import datetime as dt

from lib.filter import by_genre_pattern
from lib.playlist import Playlist
from lib.playlist_management import (
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
    print(
        f" \x1b[1;32;20mDone.\033[0m"
        f" (\x1b[33;20mTook {hours}h {mins}m {secs}s.\033[0m)"
    )


CANDIDATES_ID = "5AZxg3qZIC7cGnxWa7EuSd"
Q_ALL_ID = "4Mr3AVGL2jGI4Jc2qr3PLf"
REJECTS_ID = "2Cm0uu5nAGb1ISfXPluvks"

Q_PLAYLISTS = {
    "q - harder": {
        "id": "5mRa71QUmE6EWavxTA22g6",
        "pattern": ".*(core|doom|metal|punk).*",
    },
    "q - hop": {"id": "0sFhYQaTiuZlG1vMDSiFMR", "pattern": ".*hop.*"},
    "q - jazz": {"id": "4HQnus8hcLfX5pYtG95pKY", "pattern": ".*jazz.*"},
    "q - misc": {
        "id": "7DOqATuWsl640ustK8lhhI",
        "pattern": "^(?!.*?(core|doom|hop|jazz|metal|punk|rock)).*",
    },
    "q - rock": {"id": "1tlzpLpRdQXUicLbhIJMcM", "pattern": ".*rock.*"},
}

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

# Recreate Q playlists
for playlist_name, details in Q_PLAYLISTS.items():
    with note_when_done(f"Recreating '{playlist_name}'..."):
        playlist = Playlist(
            playlist_name,
            playlist_id=details["id"],
            track_filters=[by_genre_pattern(pattern := details["pattern"])],
            track_source=lambda user: q_all_tracks,
        )

        playlist.get_tracks(user)
        playlist.order_tracks()
        playlist.recreate(user)
