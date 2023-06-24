from typing import Callable

from lib.models.types import Tracks
from lib.playlists.management import get_tracks_from_playlist
from lib.users import User

TrackSource = Callable[[User], Tracks]


from_saved_albums: TrackSource = User.get_tracks_from_saved_albums


def from_playlist(playlist_id: str) -> TrackSource:
    def track_source(user: User) -> Tracks:
        return get_tracks_from_playlist(playlist_id, user=user)

    return track_source
