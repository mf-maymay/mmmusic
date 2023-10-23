from typing import TYPE_CHECKING, Callable

from lib.models.types import Tracks
from lib.playlists.management import get_tracks_from_playlist
from lib.users import User

if TYPE_CHECKING:
    from lib.models.playlist_configs import PlaylistConfig

TrackSource = Callable[[User], Tracks]


from_saved_albums: TrackSource = User.get_tracks_from_saved_albums


def from_playlist(playlist_id: str) -> TrackSource:
    def track_source(user: User) -> Tracks:
        return get_tracks_from_playlist(playlist_id, user=user)

    return track_source


def from_playlist_config(playlist_config: "PlaylistConfig") -> TrackSource:
    def track_source(user: User) -> Tracks:
        tracks = playlist_config.track_source(user)

        for track_filter in playlist_config.track_filters:
            tracks = track_filter(tracks)

        return tracks

    return track_source


def from_tracks(tracks: Tracks) -> TrackSource:
    def track_source(user: User) -> Tracks:
        return tracks

    return track_source
