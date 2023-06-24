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

        self.track_source = (
            config.track_source
            if config.track_source is not None
            else user.get_tracks_from_saved_albums
        )

        self.tracks = None

    @property
    def name(self) -> str:
        return self.config.name

    def get_tracks(self):
        self.tracks = self.track_source()

        for track_filter in self.config.track_filters:
            self.tracks = track_filter(self.tracks)

    def order_tracks(self):
        if self.tracks is None:
            raise ValueError("tracks not set")

        self.tracks = self.config.order_tracks_func(self.tracks)

    def create(self):
        if self.id is not None:
            raise ValueError("id is already set")

        self.id = create_playlist(
            name=self.config.name,
            description=self.config.description,
            user=self.user,
        )

        add_tracks_to_playlist(self.id, tracks=self.tracks, user=self.user)

    def recreate(self):
        if self.id is None:
            raise ValueError("id not set")

        replace_playlist(self.id, new_tracks=self.tracks, user=self.user)
