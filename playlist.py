# -*- coding: utf-8 -*-
from math import ceil
from shuffling import order_tracks
from utils import no_timeout


class Playlist(object):
    def __init__(
        self,
        name,
        *,
        get_tracks_func,
        order_tracks_func=order_tracks,
        artists_to_exclude=()
    ):
        self.name = name

        self._get_tracks_func = get_tracks_func
        self._order_tracks_func = order_tracks_func

        self.artists_to_exclude = set(artists_to_exclude)

        self.tracks = []

    def get_tracks(self, user):
        self._get_tracks_func(self, user)

    def order_tracks(self, user):
        if not self.tracks:
            raise ValueError("self.tracks is empty")

        self.tracks = self._order_tracks_func(self.tracks, user)

    @no_timeout
    def create(self, user, confirm=True):
        if not self.tracks:
            self.get_tracks(user)
            self.order_tracks(user)

        if (
            not confirm or
            input(f"Create playlist '{self.name}'? (y/n): ")[0] in "yY"
        ):
            print(f"Creating '{self.name}'...")

            user.setup_sp(scope="playlist-modify-private")  # XXX

            playlist = user.sp.user_playlist_create(
                user._username,
                self.name,
                public=False,
                description=self.description
            )

            for i in range(ceil(len(self.tracks) / 100)):
                to_add = [
                    track.id
                    for track in self.tracks[(100 * i):(100 * (i + 1))]
                ]
                user.sp.user_playlist_add_tracks(
                    user._username,
                    playlist["id"],
                    to_add
                )
