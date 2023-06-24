from lib.models.playlist_configs import PlaylistConfig
from lib.playlists.generated_playlists import GeneratedPlaylist
from lib.track_sources import from_playlist
from lib.users import User

ID = "67azW1qgFpSn7MDYO2QTl1"

playlist_config = PlaylistConfig(
    name="Monsters and Trains",
    id=ID,
    track_source=from_playlist(ID),
)

playlist = GeneratedPlaylist(
    config=playlist_config,
    user=User(),
)

playlist.get_tracks()
playlist.order_tracks()
playlist.recreate()
