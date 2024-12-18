from typing import TYPE_CHECKING, Callable

from mmmusic.models.tracks import Track
from mmmusic.playlists.management import get_tracks_from_playlist
from mmmusic.users import User

if TYPE_CHECKING:
    from mmmusic.models.playlist_configs import PlaylistConfig

TrackSource = Callable[[User], list[Track]]


def _exclude_featureless_tracks(track_source: TrackSource) -> TrackSource:
    # Tracks without audio features cannot be used in most applications, so we will drop
    # them (for now).

    def track_source_without_featureless_tracks(user: User) -> list[Track]:
        return [
            track for track in track_source(user) if track.audio_features is not None
        ]

    return track_source_without_featureless_tracks


from_saved_albums: TrackSource = _exclude_featureless_tracks(
    User.get_tracks_from_saved_albums
)


def from_playlist(playlist_id: str) -> TrackSource:
    def track_source(user: User) -> list[Track]:
        return get_tracks_from_playlist(playlist_id, user=user)

    return _exclude_featureless_tracks(track_source)


def from_playlist_config(playlist_config: "PlaylistConfig") -> TrackSource:
    def track_source(user: User) -> list[Track]:
        tracks = playlist_config.track_source(user)

        if playlist_config.combined_processor is not None:
            tracks = playlist_config.combined_processor(tracks)

        return tracks

    return _exclude_featureless_tracks(track_source)


def from_tracks(tracks: list[Track]) -> TrackSource:
    def track_source(user: User) -> list[Track]:
        return tracks

    return _exclude_featureless_tracks(track_source)
