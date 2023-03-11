from lib.features import get_scores_for_tracks, similarity
from lib.models.track import get_track
from lib.playlist import Playlist
from lib.user import User

seeds = [
    get_track("1ibHApXtb0pgplmNDRLHrJ"),  # Achilles Last Stand by Led Zeppelin
    # get_track("4g14R1u5Vc4hYUP56qyM3N"),  # La faulx by Univers Zero
    # get_track("0yY0Gba40gNEBFCWWMZGZo"),  # Summoning the Rain by Drudkh
]

user = User()

all_tracks = user.get_tracks_from_saved_albums()

assert all(seed in all_tracks for seed in seeds)

track_scores = get_scores_for_tracks(all_tracks)

similarity_vectors = {
    track: [similarity(track_scores[track], track_scores[seed]) for seed in seeds]
    for track in all_tracks
}

similarity_scalars = {
    track: sum(similarity_vectors[track])  # higher -> more similar
    for track in all_tracks
}

ordered_by_sim_desc = sorted(all_tracks, key=similarity_scalars.get, reverse=True)

most_similar = ordered_by_sim_desc[:69]

als_playlist = Playlist(
    "Ankou's Last Stand",
    track_source=lambda x: list(set(most_similar) | set(seeds)) + seeds * 2,
)

als_playlist.get_tracks(user)

als_playlist.order_tracks()

als_playlist.create(user)
