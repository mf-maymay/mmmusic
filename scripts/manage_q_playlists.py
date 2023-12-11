from mmmusic.data import playlist_configs, playlist_ids
from mmmusic.logging import get_logger
from mmmusic.playlists.generated_playlists import GeneratedPlaylist
from mmmusic.playlists.management import (
    add_tracks_to_playlist,
    clear_playlist,
    get_tracks_from_playlist,
    remove_tracks_from_playlist,
    shuffle_playlist,
)
from mmmusic.users import User

logger = get_logger()

user = User()

# Get playlist tracks
logger.info("Getting tracks")

candidates = set(get_tracks_from_playlist(playlist_ids.CANDIDATES, user=user))

q_all_tracks = set(get_tracks_from_playlist(playlist_ids.Q_ALL, user=user))

rejects = set(get_tracks_from_playlist(playlist_ids.REJECTS, user=user))

user_tracks = set(user.get_tracks_from_saved_albums())

# Add candidates to 'q - all'
candidates_to_add = candidates - q_all_tracks

logger.info(f"Adding {len(candidates_to_add):,} candidates")

add_tracks_to_playlist(playlist_ids.Q_ALL, tracks=candidates_to_add, user=user)

q_all_tracks |= candidates_to_add

clear_playlist(playlist_ids.CANDIDATES, user=user)

# Remove rejects from 'q - all'
rejects_to_remove = rejects & q_all_tracks

logger.info(f"Removing {len(rejects_to_remove):,} rejects")

remove_tracks_from_playlist(playlist_ids.Q_ALL, tracks=rejects_to_remove, user=user)

q_all_tracks -= rejects_to_remove

clear_playlist(playlist_ids.REJECTS, user=user)

# Remove already-saved from 'q - all'
already_saved_to_remove = q_all_tracks & user_tracks

logger.info(f"Removing {len(already_saved_to_remove):,} already-saved tracks")

remove_tracks_from_playlist(
    playlist_ids.Q_ALL, tracks=already_saved_to_remove, user=user
)

q_all_tracks -= already_saved_to_remove

# Shuffle 'q - all'
logger.info("Shuffing 'q - all'")

shuffle_playlist(playlist_ids.Q_ALL, user=user)

# Recreate Q playlists
for playlist_config in playlist_configs.q_playlists:
    logger.info(f"Recreating '{playlist_config.name}'")

    playlist = GeneratedPlaylist(config=playlist_config, user=user)

    playlist.get_tracks()

    playlist.build()
