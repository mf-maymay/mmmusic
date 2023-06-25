from lib.filters import by_similarity_to_track
from lib.models.playlist_configs import PlaylistConfig
from lib.models.tracks import get_track
from lib.playlists.generated_playlists import GeneratedPlaylist
from lib.users import User

ACHILLES_LAST_STAND = get_track("1ibHApXtb0pgplmNDRLHrJ")

als_playlist_config = PlaylistConfig(
    name="Ankou's Last Stand",
    track_filters=[by_similarity_to_track(ACHILLES_LAST_STAND, limit=69)],
)

als_playlist = GeneratedPlaylist(
    config=als_playlist_config,
    user=User(),
)

als_playlist.get_tracks()
als_playlist.order_tracks()
als_playlist.create()
