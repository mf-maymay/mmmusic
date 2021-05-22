# -*- coding: utf-8 -*-
from math import ceil
from utils import no_timeout


class Playlist(object):
    def __init__(self, name, *, pattern, artists_to_exclude=()):
        self.name = name
        self.pattern = pattern
        self.artists_to_exclude = set(artists_to_exclude)

        self.description = self.pattern
        self.tracks = []  # XXX

    @no_timeout
    def create(self, user, confirm=True):
        if not self.tracks:
            raise ValueError("self.tracks is empty")

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
    "ALL": Playlist("ALL", pattern=".*"),
    "american": Playlist("american", pattern=".*(americana|country|cow).*"),
    "black": Playlist("black", pattern=".*black.*"),
    "blues": Playlist("blues", pattern="^(?!.*?punk).*blue.*"),
    "bop": Playlist("bop", pattern=".*bop.*"),
    "classical": Playlist(
        "classical",
        pattern=".*(classical|compositional).*",
        artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"]
    ),
    "emo": Playlist("emo", pattern=".*emo.*"),
    "escape room": Playlist("escape room", pattern=".*escape room.*"),
    "experimental": Playlist("experimental", pattern=".*experimental.*"),
    "folk": Playlist("folk", pattern="^(?!.*?freak).*.*folk.*"),
    "hops": Playlist("hops", pattern=".*hop.*"),
    "indie": Playlist("indie", pattern=".*indie.*"),
    "japan": Playlist("japan", pattern=".*(japan|j-).*"),
    "jazzish": Playlist("jazzish", pattern=".*jazz.*"),
    "metal": Playlist("metal", pattern=".*(doom|metal|zeuhl).*"),
    "noise": Playlist("noise", pattern=".*noise.*"),
    "oblivion": Playlist(
        "oblivion",
        pattern=("^(?!.*?trap).*(ambient|dark|instrumental rock|medieval|"
                 "neofolk|world).*")
    ),
    "punkish": Playlist("punkish", pattern=".*punk.*"),
    "tropical": Playlist("tropical", pattern=".*(brazil|latin|mpb|reggae).*")
}
