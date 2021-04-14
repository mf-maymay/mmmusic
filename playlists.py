# -*- coding: utf-8 -*-

class Playlist(object):
    def __init__(self, name, *, pattern, artists_to_exclude=()):
        self.name = name
        self.pattern = pattern
        self.artists_to_exclude = set(artists_to_exclude)


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
