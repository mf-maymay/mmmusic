from lib.models.playlist_configs import PlaylistConfig
from lib.models.tracks import get_track
from lib.playlists.ordering import by_similarity
from lib.playlists.generated_playlists import GeneratedPlaylist
from lib.track_sources import from_tracks
from lib.users import User

ACHILLES_LAST_STAND = get_track("1ibHApXtb0pgplmNDRLHrJ")

user = User()

all_tracks = user.get_tracks_from_saved_albums()

most_similar = by_similarity(seed=ACHILLES_LAST_STAND, tracks=all_tracks)[:69]

als_playlist_config = PlaylistConfig(
    name="Ankou's Last Stand",
    track_source=from_tracks(most_similar),
)

als_playlist = GeneratedPlaylist(
    config=als_playlist_config,
    user=user,
)

als_playlist.get_tracks()
als_playlist.order_tracks()
als_playlist.create()
