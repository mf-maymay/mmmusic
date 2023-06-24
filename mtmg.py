from lib.models.playlist_configs import PlaylistConfig
from lib.playlists import GeneratedPlaylist
from lib.playlists.management import get_tracks_from_playlist
from lib.users import User

ID = "67azW1qgFpSn7MDYO2QTl1"


def track_source(user):
    return get_tracks_from_playlist(ID, user=user)


playlist_config = PlaylistConfig(
    name="Monsters and Trains",
    id=ID,
    track_source=track_source,
)

playlist = GeneratedPlaylist(
    config=playlist_config,
    user=User(),
)

playlist.get_tracks()
playlist.order_tracks()
playlist.recreate()
