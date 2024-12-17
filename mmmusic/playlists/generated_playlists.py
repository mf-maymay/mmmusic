from mmmusic.log_utils import get_logger
from mmmusic.models.playlist_configs import PlaylistConfig
from mmmusic.playlists.management import (
    add_tracks_to_playlist,
    create_playlist,
    replace_playlist,
)
from mmmusic.users import User

logger = get_logger()

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
        logger.info("Getting %r tracks", self.name)

        self.tracks = self.config.track_source(self.user)

        if self.config.combined_processor is not None:
            logger.info("Ordering %r tracks", self.name)
            self.tracks = self.config.combined_processor(self.tracks)

    def build(self):
        if self.tracks is None:
            self.get_tracks()

        if self.id is None:
            self._create()
        else:
            self._recreate()

    def _create(self):
        logger.info("Creating %r", self.name)

        self.id = create_playlist(
            name=self.name,
            description=self.config.description,
            user=self.user,
        )

        add_tracks_to_playlist(self.id, tracks=self.tracks, user=self.user)

    def _recreate(self):
        logger.info("Recreating %r", self.name)

        replace_playlist(
            self.id,
            new_tracks=self.tracks,
            user=self.user,
            new_name=self.name,
            new_description=self.config.description,
        )
