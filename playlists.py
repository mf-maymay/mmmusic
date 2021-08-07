# -*- coding: utf-8 -*-
from playlist import Playlist
from playlist_utils import (
    all_user_tracks,
    tracks_by_album_attribute,
    tracks_by_artist_attribute,
    tracks_by_audio_feature,
    tracks_by_genre_pattern,
)

playlists = {
    "ALL": Playlist("ALL", get_tracks_func=all_user_tracks),
    "classical": Playlist(
        "classical",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(classical|compositional).*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
    ),
    "countryish": Playlist(
        "countryish",
        get_tracks_func=tracks_by_genre_pattern(".*(americana|country|cow).*"),
    ),
    "escape room": Playlist(
        "escape room", get_tracks_func=tracks_by_genre_pattern(".*escape room.*")
    ),
    "hip hop": Playlist(
        "hip hop", get_tracks_func=tracks_by_genre_pattern(".*hip hop.*")
    ),
    "japan": Playlist(
        "japan", get_tracks_func=tracks_by_genre_pattern(".*(japan|j-).*")
    ),
    "jazz": Playlist(
        "jazz",
        get_tracks_func=tracks_by_genre_pattern(
            "^(?!.*?(dark|nu|jazz metal|jazz rap|jazztronica)).*jazz.*"
        ),
    ),
    "metal": Playlist(
        "metal", get_tracks_func=tracks_by_genre_pattern(".*(doom|metal|zeuhl).*")
    ),
    "oblivion": Playlist(
        "oblivion",
        get_tracks_func=tracks_by_genre_pattern(
            "^(?!.*?trap).*(ambient|dark|instrumental rock|medieval|neofolk|" "world).*"
        ),
    ),
    "post-rock": Playlist(
        "post-rock", get_tracks_func=tracks_by_genre_pattern(".*post-rock.*")
    ),
    "punkish": Playlist("punkish", get_tracks_func=tracks_by_genre_pattern(".*punk.*")),
    "tropical": Playlist(
        "tropical",
        get_tracks_func=tracks_by_genre_pattern(".*(brazil|latin|mpb|reggae).*"),
    ),
    "good vibes": Playlist(
        "good vibes",
        get_tracks_func=tracks_by_audio_feature(
            lambda x: x["danceability"] >= 0.6 and x["valence"] >= 0.75
        ),
    ),
    "low-valence": Playlist(
        "low-valence",
        get_tracks_func=tracks_by_audio_feature(lambda x: x["valence"] <= 0.04),
    ),
    "studying": Playlist(
        "studying",
        get_tracks_func=tracks_by_audio_feature(
            lambda x: x["instrumentalness"] >= 0.8
            and x["energy"] <= 0.5
            and x["tempo"] <= 120
        ),
    ),
    "popular artists": Playlist(
        "popular artists",
        get_tracks_func=tracks_by_artist_attribute(lambda x: x.popularity >= 75),
    ),
    "unpopular artists": Playlist(
        "unpopular artists",
        get_tracks_func=tracks_by_artist_attribute(lambda x: x.popularity <= 25),
    ),
    "1970s": Playlist(
        "1970s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("197")
        ),
    ),
    "1980s": Playlist(
        "1980s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("198")
        ),
    ),
    "1990s": Playlist(
        "1990s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("199")
        ),
    ),
    "2000s": Playlist(
        "2000s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("200")
        ),
    ),
    "2010s": Playlist(
        "2010s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("201")
        ),
    ),
}


if __name__ == "__main__":
    from user import User

    user = User(input("username: "))
    print()

    to_create = sorted(playlists)

    for key in to_create:
        playlist = playlists[key]
        print(f"Getting '{playlist.name}' tracks ...")
        playlist.get_tracks(user)
        print(f"Ordering '{playlist.name}' tracks ...")
        playlist.order_tracks(user)
        print()

    for key in to_create:
        playlist = playlists[key]
        playlist.create(user, confirm=True)
