from lib.playlist_management import (
    add_tracks_to_playlist,
    create_playlist,
    replace_playlist,
)
from lib.shuffling import smart_shuffle
from lib.user import User

MAX_TRACKS = 11_000


class Playlist:
    def __init__(
        self,
        name,
        *,
        playlist_id=None,
        description="",
        track_source=User.all_tracks,
        track_filters=(),
        order_tracks_func=smart_shuffle,
    ):
        self.id = playlist_id

        self.name = name
        self.description = description

        self.track_source = track_source
        self.track_filters = tuple(track_filters)
        self.order_tracks_func = order_tracks_func

        self.tracks = []

    def get_tracks(self, user):
        self.tracks = self.track_source(user)

        for track_filter in self.track_filters:
            self.tracks = track_filter(self.tracks)

    def order_tracks(self):
        if not self.tracks:
            raise ValueError("No tracks to order")

        self.tracks = self.order_tracks_func(self.tracks)

    def create(self, user):
        self.id = create_playlist(
            name=self.name, description=self.description, user=user
        )

        add_tracks_to_playlist(self.id, tracks=self.tracks, user=user)

    def replace(self, user):
        replace_playlist(self.id, new_tracks=self.tracks, user=user)
