from functools import partial

from lib.playlists import GeneratedPlaylist
from lib.playlists.management import get_tracks_from_playlist
from lib.shuffling import _story_picker, smart_shuffle
from lib.users import User


def track_source(user):
    return get_tracks_from_playlist("0WXuGXw1OSkSct4aYW4Nnu", user=user)


user = User()

playlist = GeneratedPlaylist(
    "Building Up Built To Spill",
    track_source=partial(track_source, user),
    order_tracks_func=partial(smart_shuffle, picker_factory=_story_picker),
    user=user,
)

playlist.get_tracks()
playlist.order_tracks()
playlist.create()
