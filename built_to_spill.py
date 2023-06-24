from functools import partial

from lib.models.playlist_configs import PlaylistConfig
from lib.playlists import GeneratedPlaylist
from lib.playlists.management import get_tracks_from_playlist
from lib.shuffling import _story_picker, smart_shuffle
from lib.users import User

ID = "0WXuGXw1OSkSct4aYW4Nnu"


def track_source(user):
    return get_tracks_from_playlist(ID, user=user)


playlist_config = PlaylistConfig(
    name="Building Up Built To Spill",
    track_source=track_source,
    order_tracks_func=partial(smart_shuffle, picker_factory=_story_picker),
)

playlist = GeneratedPlaylist(
    config=playlist_config,
    user=User(),
)

playlist.get_tracks()
playlist.order_tracks()
playlist.create()
