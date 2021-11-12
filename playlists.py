# -*- coding: utf-8 -*-
from calendar import month_name
from datetime import datetime as dt
from functools import partial

from music_tools.playlist import Playlist
from music_tools.playlist_utils import (
    tracks_by_album_attribute,
    tracks_by_artist_attribute,
    tracks_by_genre_pattern,
    tracks_by_release_year,
    tracks_by_track_attribute,
)
from music_tools.shuffling import smart_shuffle
from music_tools.user import User


_playlists = [
    Playlist("1970s", get_tracks_func=tracks_by_release_year(1970, 1979)),
    Playlist("1980s", get_tracks_func=tracks_by_release_year(1980, 1989)),
    Playlist("1990s", get_tracks_func=tracks_by_release_year(1990, 1999)),
    Playlist("2000s", get_tracks_func=tracks_by_release_year(2000, 2009)),
    Playlist("ALL"),
    Playlist(
        "ALL, without smoothing",
        order_tracks_func=partial(smart_shuffle, smooth=False),
    ),
    Playlist(
        "ALL - genre mode", order_tracks_func=partial(smart_shuffle, mode="genre"),
    ),
    Playlist(
        "ALL - radio mode", order_tracks_func=partial(smart_shuffle, mode="radio"),
    ),
    Playlist(
        "ALL - radio mode, without smoothing",
        order_tracks_func=partial(smart_shuffle, mode="radio", smooth=False),
    ),
    Playlist(
        "ALL - smart-story mode",
        order_tracks_func=partial(smart_shuffle, mode="smart-story"),
    ),
    Playlist(
        "ALL - smart-story mode, without smoothing",
        order_tracks_func=partial(smart_shuffle, mode="smart-story", smooth=False),
    ),
    Playlist("ALL - test mode", order_tracks_func=partial(smart_shuffle, mode="test"),),
    Playlist(
        "bad vibes",
        description="high energy, low valence",
        filter_tracks_func=tracks_by_track_attribute(
            lambda x: x["valence"] <= 0.10 and x["energy"] > 0.6
        ),
    ),
    Playlist(
        "classical",
        get_tracks_func=tracks_by_genre_pattern(
            pattern := ".*(classical|compositional).*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "countryish",
        get_tracks_func=tracks_by_genre_pattern(
            pattern := ".*(americana|country|cow).*"
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "emo/math",
        get_tracks_func=tracks_by_genre_pattern(pattern := ".*(emo|math).*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "escape room",
        get_tracks_func=tracks_by_genre_pattern(pattern := ".*escape room.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "good vibes",
        description="high danceability, high valence",
        filter_tracks_func=tracks_by_track_attribute(
            lambda x: x["danceability"] >= 0.5 and x["valence"] >= 0.9
        ),
    ),
    Playlist(
        "hip hop",
        get_tracks_func=tracks_by_genre_pattern(pattern := ".*hip hop.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "japan",
        get_tracks_func=tracks_by_genre_pattern(
            pattern := ".*(japan|j-).*",
            artists_to_exclude=["3BG0nwVh3Gc7cuT4XdsLtt"],  # joe henderson
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "jazz",
        get_tracks_func=tracks_by_genre_pattern(
            pattern := "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica))"
            ".*jazz.*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "metal",
        get_tracks_func=tracks_by_genre_pattern(pattern := ".*(doom|metal|zeuhl).*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "post-rock",
        get_tracks_func=tracks_by_genre_pattern(pattern := ".*post-rock.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist("pre-1970", get_tracks_func=tracks_by_release_year(None, 1969)),
    Playlist(
        "punkish",
        get_tracks_func=tracks_by_genre_pattern(pattern := ".*punk.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist("since 2010", get_tracks_func=tracks_by_release_year(2010, None)),
    Playlist(
        "studying",
        description="instrumental, low energy, tempo <= 120 bpm",
        filter_tracks_func=tracks_by_track_attribute(
            lambda x: x["instrumentalness"] >= 0.8
            and x["energy"] <= 0.5
            and x["tempo"] <= 120
        ),
    ),
    Playlist(
        "tropical",
        get_tracks_func=tracks_by_genre_pattern(
            pattern := ".*(brazil|latin|mpb|reggae).*"
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "unpopular artists",
        get_tracks_func=tracks_by_artist_attribute(lambda x: x.popularity <= 25),
    ),
    Playlist(
        month_name[(month := dt.today().month)],
        description=f"albums released in {month_name[month]}",
        get_tracks_func=tracks_by_album_attribute(
            lambda x: x["release_date_precision"] == "day"
            and dt.strptime(x["release_date"], "%Y-%m-%d").month == month
            or x["release_date_precision"] == "month"
            and dt.strptime(x["release_date"], "%Y-%m").month == month
        ),
    ),
]

playlists = {playlist.name: playlist for playlist in _playlists}


if __name__ == "__main__":
    from music_tools.album import Album
    from music_tools.artist import Artist
    from music_tools.track import AudioFeatures

    Album.use_json(ok_if_missing=True)
    Artist.use_json(ok_if_missing=True)
    AudioFeatures.use_json(ok_if_missing=True)

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
