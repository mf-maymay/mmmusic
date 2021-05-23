# -*- coding: utf-8 -*-
from math import ceil
from playlist_utils import pattern_matching_tracks
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


playlists = {
    "ALL": Playlist(
        "ALL",
        get_tracks_func=pattern_matching_tracks(".*")
    ),
    "black": Playlist(
        "black",
        get_tracks_func=pattern_matching_tracks(".*black.*")
    ),
    "blues": Playlist(
        "blues",
        get_tracks_func=pattern_matching_tracks("^(?!.*?punk).*blue.*")
    ),
    "bop": Playlist(
        "bop",
        get_tracks_func=pattern_matching_tracks(".*bop.*")
    ),
    "classical": Playlist(
        "classical",
        get_tracks_func=pattern_matching_tracks(
            ".*(classical|compositional).*"
        ),
        artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"]
    ),
    "countryish": Playlist(
        "countryish",
        get_tracks_func=pattern_matching_tracks(".*(americana|country|cow).*")
    ),
    "emo": Playlist(
        "emo",
        get_tracks_func=pattern_matching_tracks(".*emo.*")
    ),
    "escape room": Playlist(
        "escape room",
        get_tracks_func=pattern_matching_tracks(".*escape room.*")
    ),
    "experimental": Playlist(
        "experimental",
        get_tracks_func=pattern_matching_tracks(".*experimental.*")
    ),
    "folk": Playlist(
        "folk",
        get_tracks_func=pattern_matching_tracks("^(?!.*?freak).*.*folk.*")
    ),
    "hops": Playlist(
        "hops",
        get_tracks_func=pattern_matching_tracks(".*hop.*")
    ),
    "indie": Playlist(
        "indie",
        get_tracks_func=pattern_matching_tracks(".*indie.*")
    ),
    "japan": Playlist(
        "japan",
        get_tracks_func=pattern_matching_tracks(".*(japan|j-).*")
    ),
    "jazzish": Playlist(
        "jazzish",
        get_tracks_func=pattern_matching_tracks(".*jazz.*")
    ),
    "metal": Playlist(
        "metal",
        get_tracks_func=pattern_matching_tracks(".*(doom|metal|zeuhl).*")
    ),
    "noise": Playlist(
        "noise",
        get_tracks_func=pattern_matching_tracks(".*noise.*")
    ),
    "oblivion": Playlist(
        "oblivion",
        get_tracks_func=pattern_matching_tracks(
            "^(?!.*?trap).*(ambient|dark|instrumental rock|medieval|neofolk|"
            "world).*"
        )
    ),
    "punkish": Playlist(
        "punkish",
        get_tracks_func=pattern_matching_tracks(".*punk.*")
    ),
    "tropical": Playlist(
        "tropical",
        get_tracks_func=pattern_matching_tracks(
            ".*(brazil|latin|mpb|reggae).*"
        )
    )
}


if __name__ == "__main__":
    from user import User

    user = User(input("username: "))

    playlists["jazzish"].create(user)
