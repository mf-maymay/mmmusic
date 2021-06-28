# -*- coding: utf-8 -*-
from playlist import Playlist
from playlist_utils import (
    all_user_tracks,
    tracks_by_artist_attribute,
    tracks_by_audio_feature,
    tracks_by_genre_pattern
)

playlists = {
    "ALL": Playlist(
        "ALL",
        get_tracks_func=all_user_tracks
    ),
    "black": Playlist(
        "black",
        get_tracks_func=tracks_by_genre_pattern(".*black.*")
    ),
    "blues": Playlist(
        "blues",
        get_tracks_func=tracks_by_genre_pattern("^(?!.*?punk).*blue.*")
    ),
    "classical": Playlist(
        "classical",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(classical|compositional).*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"]  # adrian younge
        )
    ),
    "countryish": Playlist(
        "countryish",
        get_tracks_func=tracks_by_genre_pattern(".*(americana|country|cow).*")
    ),
    "escape room": Playlist(
        "escape room",
        get_tracks_func=tracks_by_genre_pattern(".*escape room.*")
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
    "jazz": Playlist(
        "jazz",
        get_tracks_func=tracks_by_genre_pattern(
            "^(?!.*?(dark|nu|jazz metal|jazz rap|jazztronica)).*jazz.*"
        )
    ),
    "metal": Playlist(
        "metal",
        get_tracks_func=tracks_by_genre_pattern(".*(doom|metal|zeuhl).*")
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
    "slow": Playlist(
        "slow",
        get_tracks_func=tracks_by_genre_pattern(".*slow.*")
    ),
    "tropical": Playlist(
        "tropical",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(brazil|latin|mpb|reggae).*"
        )
    ),
    "high-danceability": Playlist(
        "high-danceability",
        get_tracks_func=tracks_by_audio_feature(
            lambda x: x["danceability"] >= .75
        )
    ),
    "low-valence": Playlist(
        "low-valence",
        get_tracks_func=tracks_by_audio_feature(lambda x: x["valence"] <= .1)
    ),
    "popular": Playlist(
        "popular",
        get_tracks_func=tracks_by_artist_attribute(
            lambda x: x.popularity >= 70
        )
    ),
    "unpopular": Playlist(
        "unpopular",
        get_tracks_func=tracks_by_artist_attribute(
            lambda x: x.popularity <= 30
        )
    )
}


if __name__ == "__main__":
    from user import User

    user = User(input("username: "))

    for playlist in sorted(playlists, reverse=True):
        playlists[playlist].get_tracks(user)
        playlists[playlist].order_tracks(user)
        playlists[playlist].create(user, confirm=False)
        print()
