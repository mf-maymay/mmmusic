from typing import TYPE_CHECKING, Callable

from mmmusic.models.tracks import Track
from mmmusic.playlists.management import get_tracks_from_playlist
from mmmusic.users import User

if TYPE_CHECKING:
    from mmmusic.models.playlist_configs import PlaylistConfig

TrackSource = Callable[[User], list[Track]]


from_saved_albums: TrackSource = User.get_tracks_from_saved_albums


def from_playlist(playlist_id: str) -> TrackSource:
    def track_source(user: User) -> list[Track]:
        return get_tracks_from_playlist(playlist_id, user=user)

    return track_source


def from_playlist_config(playlist_config: "PlaylistConfig") -> TrackSource:
    def track_source(user: User) -> list[Track]:
        tracks = playlist_config.track_source(user)

        if playlist_config.track_list_processor is not None:
            tracks = playlist_config.track_list_processor(tracks)

        return tracks

    return track_source


def from_tracks(tracks: list[Track]) -> TrackSource:
    def track_source(user: User) -> list[Track]:
        return tracks

    return track_source
