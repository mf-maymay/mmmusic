from mmmusic.models.playlist_configs import PlaylistConfig
from mmmusic.playlists.management import (
    add_tracks_to_playlist,
    create_playlist,
    replace_playlist,
)
from mmmusic.users import User

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

        self.tracks = None

    @property
    def name(self) -> str:
        return self.config.name

    def get_tracks(self):
        self.tracks = self.config.track_source(self.user)

        if self.config.track_list_processor is not None:
            self.tracks = self.config.track_list_processor(self.tracks)

    def order_tracks(self):
        if self.tracks is None:
            raise ValueError("tracks not set")

        self.tracks = self.config.order_tracks_func(self.tracks)

    def create(self):
        if self.id is not None:
            raise ValueError("id is already set")

        self.id = create_playlist(
            name=self.name,
            description=self.config.description,
            user=self.user,
        )

        add_tracks_to_playlist(self.id, tracks=self.tracks, user=self.user)

    def recreate(self):
        if self.id is None:
            raise ValueError("id not set")

        replace_playlist(
            self.id,
            new_tracks=self.tracks,
            user=self.user,
            new_name=self.name,
            new_description=self.config.description,
        )
