from functools import partial

from lib.playlist import Playlist
from lib.playlist_management import get_tracks_from_playlist
from lib.shuffling import _story_picker, smart_shuffle
from lib.user import User


def track_source(user):
    return get_tracks_from_playlist("0WXuGXw1OSkSct4aYW4Nnu", user=user)


user = User()

playlist = Playlist(
    "Building Up Built To Spill",
    track_source=track_source,
    order_tracks_func=partial(smart_shuffle, picker_factory=_story_picker),
)

playlist.get_tracks(user)
playlist.order_tracks()
playlist.create(user)
