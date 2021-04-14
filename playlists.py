# -*- coding: utf-8 -*-

class Playlist(object):
    def __init__(self, name, *, pattern, artists_to_exclude=()):
        self.name = name
        self.pattern = pattern
        self.artists_to_exclude = set(artists_to_exclude)


def create_playlist(user, tracks, playlist_name, description="", confirm=True):
    if (not confirm or
            input(f"Create playlist '{playlist_name}'? (y/n): ")[0] in "yY"):
        print(f"Creating '{playlist_name}'...")

        user.setup_sp(scope="playlist-modify-private")  # XXX

        playlist = user.sp.user_playlist_create(user._username,
                                                playlist_name,
                                                public=False,
                                                description=description)

        for i in range(0, (l := len(tracks)) // 100 + bool(l % 100)):
            to_add = tracks[(100 * i):(100 * (i + 1))]
            user.sp.user_playlist_add_tracks(user._username,
                                             playlist["id"],
                                             to_add)


playlists = {
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
    "folk": Playlist("folk", pattern="^(?!.*?freak).*.*folk.*"),
    "hops": Playlist("hops", pattern=".*hop.*"),
    "indie": Playlist("indie", pattern=".*indie.*"),
    "japan": Playlist("japan", pattern=".*(japan|j-).*"),
    "jazzistico": Playlist("jazzistico", pattern=".*jazz.*"),
    "metal": Playlist("metal", pattern=".*metal.*"),
    "oblivion": Playlist(
        "oblivion",
        pattern=("^(?!.*?trap).*(ambient|dark|instrumental rock|medieval|"
                 "neofolk|world).*")
    ),
    "punk": Playlist("punk", pattern=".*punk.*")
}
