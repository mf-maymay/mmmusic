from lib.filters import by_genre_pattern
from lib.playlist import Playlist
from lib.playlist_management import (
    add_tracks_to_playlist,
    clear_playlist,
    get_tracks_from_playlist,
    remove_tracks_from_playlist,
    shuffle_playlist,
)
from lib.user import User
from lib.utils import time_and_note_when_done

CANDIDATES_ID = "5AZxg3qZIC7cGnxWa7EuSd"
Q_ALL_ID = "4Mr3AVGL2jGI4Jc2qr3PLf"
REJECTS_ID = "2Cm0uu5nAGb1ISfXPluvks"

Q_PLAYLISTS = {
    "q - harder": {
        "id": "5mRa71QUmE6EWavxTA22g6",
        "pattern": "^(?!.*?(hop|rap)).*(core|doom|metal|punk).*",
    },
    "q - hop": {"id": "0sFhYQaTiuZlG1vMDSiFMR", "pattern": ".*(hop|rap).*"},
    "q - jazz": {"id": "4HQnus8hcLfX5pYtG95pKY", "pattern": ".*jazz.*"},
    "q - misc": {
        "id": "7DOqATuWsl640ustK8lhhI",
        "pattern": "^(?!.*?(core|doom|hop|jazz|metal|punk|rap|rock)).*",
    },
    "q - rock": {"id": "1tlzpLpRdQXUicLbhIJMcM", "pattern": ".*rock.*"},
}

user = User()

# Get playlist tracks
with time_and_note_when_done("Getting tracks..."):
    candidates = set(get_tracks_from_playlist(CANDIDATES_ID, user=user))

    q_all_tracks = set(get_tracks_from_playlist(Q_ALL_ID, user=user))

    rejects = set(get_tracks_from_playlist(REJECTS_ID, user=user))

    user_tracks = set(user.get_tracks_from_saved_albums())

# Add candidates to 'q - all'
candidates_to_add = candidates - q_all_tracks

with time_and_note_when_done(f"Adding {len(candidates_to_add):,} candidates..."):
    add_tracks_to_playlist(Q_ALL_ID, tracks=candidates_to_add, user=user)

q_all_tracks |= candidates_to_add

clear_playlist(CANDIDATES_ID, user=user)

# Remove rejects from 'q - all'
rejects_to_remove = rejects & q_all_tracks

with time_and_note_when_done(f"Removing {len(rejects_to_remove):,} rejects..."):
    remove_tracks_from_playlist(Q_ALL_ID, tracks=rejects_to_remove, user=user)

q_all_tracks -= rejects_to_remove

clear_playlist(REJECTS_ID, user=user)

# Remove already-saved from 'q - all'
already_saved_to_remove = q_all_tracks & user_tracks

with time_and_note_when_done(
    f"Removing {len(already_saved_to_remove):,} already-saved tracks..."
):
    remove_tracks_from_playlist(Q_ALL_ID, tracks=already_saved_to_remove, user=user)

q_all_tracks -= already_saved_to_remove

# Shuffle 'q - all'
with time_and_note_when_done("Shuffing 'q - all'..."):
    shuffle_playlist(Q_ALL_ID, user=user)

# Recreate Q playlists
for playlist_name, details in Q_PLAYLISTS.items():
    with time_and_note_when_done(f"Recreating '{playlist_name}'..."):
        playlist = Playlist(
            playlist_name,
            playlist_id=details["id"],
            track_filters=[by_genre_pattern(pattern := details["pattern"])],
            track_source=lambda user: q_all_tracks,
        )

        playlist.get_tracks(user)
        playlist.order_tracks()
        playlist.recreate(user)
