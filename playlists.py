# -*- coding: utf-8 -*-
from playlist import Playlist
from playlist_utils import (
    all_user_tracks,
    tracks_by_album_attribute,
    tracks_by_artist_attribute,
    tracks_by_audio_feature,
    tracks_by_genre_pattern,
)


_playlists = [
    Playlist(
        "1970s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("197")
        ),
    ),
    Playlist(
        "1980s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("198")
        ),
    ),
    Playlist(
        "1990s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("199")
        ),
    ),
    Playlist(
        "2000s",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date"].startswith("200")
        ),
    ),
    Playlist("ALL", get_tracks_func=all_user_tracks),
    Playlist(
        "bad vibes",
        get_tracks_func=tracks_by_audio_feature(
            lambda x: x["valence"] <= 0.10 and x["energy"] > 0.6
        ),
    ),
    Playlist(
        "classical",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(classical|compositional).*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
    ),
    Playlist(
        "countryish",
        get_tracks_func=tracks_by_genre_pattern(".*(americana|country|cow).*"),
    ),
    Playlist("escape room", get_tracks_func=tracks_by_genre_pattern(".*escape room.*")),
    Playlist(
        "good vibes",
        description="high danceability. extreme valence",
        get_tracks_func=tracks_by_audio_feature(
            lambda x: x["danceability"] >= 0.5 and x["valence"] >= 0.9
        ),
    ),
    Playlist("hip hop", get_tracks_func=tracks_by_genre_pattern(".*hip hop.*")),
    Playlist(
        "japan",
        get_tracks_func=tracks_by_genre_pattern(
            ".*(japan|j-).*",
            artists_to_exclude=["3BG0nwVh3Gc7cuT4XdsLtt"],  # joe henderson
        ),
    ),
    Playlist(
        "jazz",
        get_tracks_func=tracks_by_genre_pattern(
            "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica)).*jazz.*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
    ),
    Playlist(
        "metal", get_tracks_func=tracks_by_genre_pattern(".*(doom|metal|zeuhl).*")
    ),
    Playlist(
        "oblivion",
        get_tracks_func=tracks_by_genre_pattern(
            "^(?!.*?trap).*(ambient|dark|instrumental rock|medieval|neofolk|" "world).*"
        ),
    ),
    Playlist("post-rock", get_tracks_func=tracks_by_genre_pattern(".*post-rock.*")),
    Playlist(
        "pre-1970",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: int(x["release_date"].split("-")[0]) < 1970
        ),
    ),
    Playlist("punkish", get_tracks_func=tracks_by_genre_pattern(".*punk.*")),
    Playlist(
        "since 2010",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: int(x["release_date"].split("-")[0]) >= 2010
        ),
    ),
    Playlist(
        "studying",
        get_tracks_func=tracks_by_audio_feature(
            lambda x: x["instrumentalness"] >= 0.8
            and x["energy"] <= 0.5
            and x["tempo"] <= 120
        ),
    ),
    Playlist(
        "tropical",
        get_tracks_func=tracks_by_genre_pattern(".*(brazil|latin|mpb|reggae).*"),
    ),
    Playlist(
        "unpopular artists",
        get_tracks_func=tracks_by_artist_attribute(lambda x: x.popularity <= 25),
    ),
]

playlists = {playlist.name: playlist for playlist in _playlists}


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
        playlist.order_tracks()
        print()

    for key in to_create:
        playlist = playlists[key]
        playlist.create(user, confirm=True)
