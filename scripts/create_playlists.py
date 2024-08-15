from mmmusic.data import playlist_configs
from mmmusic.logging import get_logger
from mmmusic.playlists.generated_playlists import GeneratedPlaylist
from mmmusic.users import User

logger = get_logger()

if __name__ == "__main__":
    user = User()

    playlists = {
        playlist_config.name: GeneratedPlaylist(config=playlist_config, user=user)
        for playlist_config in playlist_configs.regular_playlists
    }

    to_create = sorted(playlists)

    for key in to_create:
        playlist = playlists[key]

        try:
            playlist.build()
        except Exception:
            logger.exception(f"Failed to build playlist {playlist.name!r}. Skipping...")
