from lib.data import playlist_ids
from lib.filters import by_genre_pattern
from lib.models.playlist_configs import PlaylistConfig
from lib.playlists.generated_playlists import GeneratedPlaylist
from lib.playlists.management import (
    add_tracks_to_playlist,
    clear_playlist,
    get_tracks_from_playlist,
    remove_tracks_from_playlist,
    shuffle_playlist,
)
from lib.track_sources import from_playlist
from lib.users import User
from lib.utils import time_and_note_when_done

q_playlists = [
    PlaylistConfig(
        name="q - harder",
        id="5mRa71QUmE6EWavxTA22g6",
        track_filters=[by_genre_pattern("^(?!.*?(hop|rap)).*(core|doom|metal|punk).*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - hop",
        id="0sFhYQaTiuZlG1vMDSiFMR",
        track_filters=[by_genre_pattern(".*(hop|rap).*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - jazz",
        id="4HQnus8hcLfX5pYtG95pKY",
        track_filters=[by_genre_pattern(".*jazz.*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - misc",
        id="7DOqATuWsl640ustK8lhhI",
        track_filters=[
            by_genre_pattern("^(?!.*?(core|doom|hop|jazz|metal|punk|rap|rock)).*")
        ],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - rock",
        id="1tlzpLpRdQXUicLbhIJMcM",
        track_filters=[by_genre_pattern(".*rock.*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
]

user = User()

# Get playlist tracks
print("Getting tracks...")
with time_and_note_when_done():
    candidates = set(get_tracks_from_playlist(playlist_ids.CANDIDATES, user=user))

    q_all_tracks = set(get_tracks_from_playlist(playlist_ids.Q_ALL, user=user))

    rejects = set(get_tracks_from_playlist(playlist_ids.REJECTS, user=user))

    user_tracks = set(user.get_tracks_from_saved_albums())

# Add candidates to 'q - all'
candidates_to_add = candidates - q_all_tracks

print(f"Adding {len(candidates_to_add):,} candidates...")
with time_and_note_when_done():
    add_tracks_to_playlist(playlist_ids.Q_ALL, tracks=candidates_to_add, user=user)

q_all_tracks |= candidates_to_add

clear_playlist(playlist_ids.CANDIDATES, user=user)

# Remove rejects from 'q - all'
rejects_to_remove = rejects & q_all_tracks

print(f"Removing {len(rejects_to_remove):,} rejects...")
with time_and_note_when_done():
    remove_tracks_from_playlist(playlist_ids.Q_ALL, tracks=rejects_to_remove, user=user)

q_all_tracks -= rejects_to_remove

clear_playlist(playlist_ids.REJECTS, user=user)

# Remove already-saved from 'q - all'
already_saved_to_remove = q_all_tracks & user_tracks

print(f"Removing {len(already_saved_to_remove):,} already-saved tracks...")
with time_and_note_when_done():
    remove_tracks_from_playlist(
        playlist_ids.Q_ALL, tracks=already_saved_to_remove, user=user
    )

q_all_tracks -= already_saved_to_remove

# Shuffle 'q - all'
print("Shuffing 'q - all'...")
with time_and_note_when_done():
    shuffle_playlist(playlist_ids.Q_ALL, user=user)

# Recreate Q playlists
for playlist_config in q_playlists:
    print(f"Recreating '{playlist_config.name}'...")
    with time_and_note_when_done():
        playlist = GeneratedPlaylist(config=playlist_config, user=user)

        playlist.get_tracks()
        playlist.order_tracks()
        playlist.recreate()
