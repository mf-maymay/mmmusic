from lib.models.playlist_configs import PlaylistConfig
from lib.playlists.management import (
    add_tracks_to_playlist,
    create_playlist,
    replace_playlist,
)
from lib.users import User

MAX_TRACKS = 11_000


class GeneratedPlaylist:
    def __init__(
        self,
        *,
        config: PlaylistConfig,
        user: User,
    ):
        self.config = config
        self.user = user

        self.id = config.id

        self.name = config.name
        self.description = config.description

        self.track_source = (
            config.track_source
            if config.track_source is not None
            else user.get_tracks_from_saved_albums
        )
        self.track_filters = config.track_filters
        self.order_tracks_func = config.order_tracks_func

        self.tracks = None

    def get_tracks(self):
        self.tracks = self.track_source()

        for track_filter in self.track_filters:
            self.tracks = track_filter(self.tracks)

    def order_tracks(self):
        if self.tracks is None:
            raise ValueError("tracks not set")

        self.tracks = self.order_tracks_func(self.tracks)

    def create(self):
        self.id = create_playlist(
            name=self.name, description=self.description, user=self.user
        )

        add_tracks_to_playlist(self.id, tracks=self.tracks, user=self.user)

    def recreate(self):
        if self.id is None:
            raise ValueError("id not set")
        replace_playlist(self.id, new_tracks=self.tracks, user=self.user)
