# -*- coding: utf-8 -*-
from playlist import Playlist
from playlist_utils import tracks_by_genre_pattern

playlists = {
    "ALL": Playlist(
        "ALL",
        get_tracks_func=tracks_by_genre_pattern(".*")
    ),
    "black": Playlist(
        "black",
        get_tracks_func=tracks_by_genre_pattern(".*black.*")
    ),
    "blues": Playlist(
        "blues",
        get_tracks_func=tracks_by_genre_pattern("^(?!.*?punk).*blue.*")
    ),
    "bop": Playlist(
        "bop",
        get_tracks_func=tracks_by_genre_pattern(".*bop.*")
    ),
    "classical": Playlist(
        "classical",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(classical|compositional).*"
        ),
        artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"]
    ),
    "countryish": Playlist(
        "countryish",
        get_tracks_func=tracks_by_genre_pattern(".*(americana|country|cow).*")
    ),
    "emo": Playlist(
        "emo",
        get_tracks_func=tracks_by_genre_pattern(".*emo.*")
    ),
    "escape room": Playlist(
        "escape room",
        get_tracks_func=tracks_by_genre_pattern(".*escape room.*")
    ),
    "experimental": Playlist(
        "experimental",
        get_tracks_func=tracks_by_genre_pattern(".*experimental.*")
    ),
    "folk": Playlist(
        "folk",
        get_tracks_func=tracks_by_genre_pattern("^(?!.*?freak).*.*folk.*")
    ),
    "hops": Playlist(
        "hops",
        get_tracks_func=tracks_by_genre_pattern(".*hop.*")
    ),
    "indie": Playlist(
        "indie",
        get_tracks_func=tracks_by_genre_pattern(".*indie.*")
    ),
    "japan": Playlist(
        "japan",
        get_tracks_func=tracks_by_genre_pattern(".*(japan|j-).*")
    ),
    "jazzish": Playlist(
        "jazzish",
        get_tracks_func=tracks_by_genre_pattern(".*jazz.*")
    ),
    "metal": Playlist(
        "metal",
        get_tracks_func=tracks_by_genre_pattern(".*(doom|metal|zeuhl).*")
    ),
    "noise": Playlist(
        "noise",
        get_tracks_func=tracks_by_genre_pattern(".*noise.*")
    ),
    "oblivion": Playlist(
        "oblivion",
        get_tracks_func=tracks_by_genre_pattern(
            "^(?!.*?trap).*(ambient|dark|instrumental rock|medieval|neofolk|"
            "world).*"
        )
    ),
    "punkish": Playlist(
        "punkish",
        get_tracks_func=tracks_by_genre_pattern(".*punk.*")
    ),
    "tropical": Playlist(
        "tropical",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(brazil|latin|mpb|reggae).*"
        )
    )
}


if __name__ == "__main__":
    from user import User

    user = User(input("username: "))

    for playlist in sorted(playlists):
        playlists[playlist].create(user, confirm=False)
