# -*- coding: utf-8 -*-
from music_tools.shuffling import smart_shuffle
from music_tools.user import User
from music_tools.utils import no_timeout, take_x_at_a_time


class Playlist:
    def __init__(
        self,
        name,
        *,
        description="",
        get_tracks_func=User.all_tracks,
        filter_tracks_func=None,
        order_tracks_func=smart_shuffle,
    ):
        self.name = name
        self.description = description

        self.get_tracks_func = get_tracks_func
        self.filter_tracks_func = filter_tracks_func
        self.order_tracks_func = order_tracks_func

        self.tracks = []

    def get_tracks(self, user):
        self.tracks = self.get_tracks_func(user)

        if self.filter_tracks_func is not None:
            self.tracks = self.filter_tracks_func(self.tracks)

    def order_tracks(self):
        if not self.tracks:
            raise ValueError("No tracks to order")

        self.tracks = self.order_tracks_func(self.tracks)

    @no_timeout
    def create(self, user, confirm=True):
        if not self.tracks:
            self.get_tracks(user)
            self.order_tracks()

        if not confirm or input(f"Create playlist '{self.name}'? (y/n): ")[0] in "yY":
            print(f"Creating '{self.name}' ...")

            playlist = user.sp.user_playlist_create(
                user.username, self.name, public=False, description=self.description
            )

            for to_add in take_x_at_a_time([track.id for track in self.tracks], 100):
                user.sp.user_playlist_add_tracks(user.username, playlist["id"], to_add)
