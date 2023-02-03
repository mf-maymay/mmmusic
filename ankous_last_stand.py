from lib.features import get_scores_for_tracks, similarity
from lib.models.track import get_track
from lib.playlist import Playlist
from lib.user import User

user = User()

all_tracks = user.get_tracks_from_saved_albums()

als = get_track("1ibHApXtb0pgplmNDRLHrJ")

assert als in all_tracks

track_scores = get_scores_for_tracks(all_tracks)

als_scores = track_scores[als]

ordered_by_sim_asc = sorted(
    all_tracks, key=lambda x: similarity(als_scores, track_scores[x])
)

most_similar = ordered_by_sim_asc[-69:]

als_playlist = Playlist("Ankou's Last Stand", track_source=lambda x: most_similar)

als_playlist.get_tracks(user)

als_playlist.order_tracks()

als_playlist.create(user)
