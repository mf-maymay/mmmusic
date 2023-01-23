from lib.playlist_utils import create_playlist
from lib.shuffling import smart_shuffle
from lib.user import User
from lib.utils import no_timeout, take_x_at_a_time

MAX_TRACKS = 11_000


class Playlist:
    def __init__(
        self,
        name,
        *,
        description="",
        track_source=User.all_tracks,
        track_filters=(),
        order_tracks_func=smart_shuffle,
    ):
        self.name = name
        self.description = description

        self.track_source = track_source
        self.track_filters = tuple(track_filters)
        self.order_tracks_func = order_tracks_func

        self.tracks = []  # XXX

    def get_tracks(self, user):
        self.tracks = self.track_source(user)

        for track_filter in self.track_filters:
            self.tracks = track_filter(self.tracks)

    def order_tracks(self):
        if not self.tracks:
            raise ValueError("No tracks to order")

        self.tracks = self.order_tracks_func(self.tracks)

    @no_timeout  # TODO: wrap sp calls, instead
    def create(self, user):
        playlist_id = create_playlist(
            name=self.name, description=self.description, user=user
        )

        if len(self.tracks) > MAX_TRACKS:
            print(
                "Playlist has {:,} tracks. Only adding first {:,} ...".format(
                    len(self.tracks), MAX_TRACKS
                )
            )

        for to_add in take_x_at_a_time(
            [track.id for track in self.tracks[:MAX_TRACKS]], 100
        ):
            user.sp.user_playlist_add_tracks(user.username, playlist_id, to_add)
