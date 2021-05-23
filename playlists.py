# -*- coding: utf-8 -*-
from playlist import Playlist
from playlist_utils import pattern_matching_tracks

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

    for playlist in playlists.values():
        playlist.create(user, confirm=False)
