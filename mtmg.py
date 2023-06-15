from lib.playlists import GeneratedPlaylist
from lib.playlists.management import get_tracks_from_playlist
from lib.users import User

ID = "67azW1qgFpSn7MDYO2QTl1"

user = User()


def track_source():
    return get_tracks_from_playlist(ID, user=user)


playlist = GeneratedPlaylist(
    "Monsters and Trains",
    playlist_id=ID,
    track_source=track_source,
    user=user,
)

playlist.get_tracks()
playlist.order_tracks()
playlist.recreate()
