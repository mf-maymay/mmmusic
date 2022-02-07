# -*- coding: utf-8 -*-
from calendar import month_name
from copy import copy
from datetime import datetime as dt
from functools import partial

from music_tools.playlist import Playlist
from music_tools.playlist_utils import (
    filter_by_album_attribute,
    filter_by_artist_attribute,
    filter_by_release_year,
    filter_by_track_attribute,
    tracks_by_genre_pattern,
    tracks_near_genre_coordinates,
)
from music_tools.shuffling import smart_shuffle
from music_tools.user import User


radio_shuffle = partial(smart_shuffle, mode="radio")

_playlists = [
    Playlist("1970s", track_filters=[filter_by_release_year(1970, 1979)]),
    Playlist("1980s", track_filters=[filter_by_release_year(1980, 1989)]),
    Playlist("1990s", track_filters=[filter_by_release_year(1990, 1999)]),
    Playlist("2000s", track_filters=[filter_by_release_year(2000, 2009)]),
    Playlist("ALL"),
    Playlist(
        "bad vibes",
        description="high energy, low valence",
        track_filters=[
            filter_by_track_attribute(
                lambda x: x["valence"] <= 0.10 and x["energy"] > 0.6
            )
        ],
    ),
    Playlist(
        "classical",
        track_source=tracks_by_genre_pattern(
            pattern := ".*(classical|compositional).*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "countryish",
        track_source=tracks_by_genre_pattern(pattern := ".*(americana|country|cow).*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "emo/math",
        track_source=tracks_by_genre_pattern(pattern := ".*(emo|math).*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "escape room",
        track_source=tracks_by_genre_pattern(pattern := ".*escape room.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "folk",
        track_source=tracks_by_genre_pattern(pattern := "^(?!.*?(freak)).*folk.*",),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "good vibes",
        description="high danceability, high valence",
        track_filters=[
            filter_by_track_attribute(
                lambda x: x["danceability"] >= 0.5 and x["valence"] >= 0.9
            )
        ],
    ),
    Playlist(
        "goth",
        track_source=tracks_by_genre_pattern(pattern := ".*(goth|lilith).*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "hip hop",
        track_source=tracks_by_genre_pattern(pattern := ".*hip hop.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "japan",
        track_source=tracks_by_genre_pattern(
            pattern := ".*(japan|j-).*",
            artists_to_exclude=["3BG0nwVh3Gc7cuT4XdsLtt"],  # joe henderson
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "jazz",
        track_source=tracks_by_genre_pattern(
            pattern := "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica))"
            ".*jazz.*",
            artists_to_exclude=["4aMeIY7MkJoZg7O91cmDDd"],  # adrian younge
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "metal",
        track_source=tracks_by_genre_pattern(pattern := ".*(doom|metal|zeuhl).*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "post-rock",
        track_source=tracks_by_genre_pattern(pattern := ".*post-rock.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist("pre-1970", track_filters=[filter_by_release_year(None, 1969)]),
    Playlist(
        "psych",
        track_source=tracks_by_genre_pattern(pattern := ".*psych.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "punkish",
        track_source=tracks_by_genre_pattern(pattern := ".*punk.*"),
        description=f"genre matches '{pattern}'",
    ),
    Playlist("since 2010", track_filters=[filter_by_release_year(2010, None)]),
    Playlist(
        "studying",
        description="instrumental, low energy, tempo <= 120 bpm",
        track_filters=[
            filter_by_track_attribute(
                lambda x: x["instrumentalness"] >= 0.8
                and x["energy"] <= 0.5
                and x["tempo"] <= 120
            )
        ],
    ),
    Playlist(
        "tropical",
        track_source=tracks_by_genre_pattern(
            pattern := ".*(brazil|latin|mpb|reggae).*"
        ),
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "unpopular artists",
        track_filters=[filter_by_artist_attribute(lambda x: x.popularity <= 25)],
    ),
    Playlist(
        month_name[(month := dt.today().month)],  # current month
        description=f"albums released in {month_name[month]}",
        track_filters=[
            filter_by_album_attribute(
                lambda x: x["release_date_precision"] == "day"
                and dt.strptime(x["release_date"], "%Y-%m-%d").month == month
                or x["release_date_precision"] == "month"
                and dt.strptime(x["release_date"], "%Y-%m").month == month
            )
        ],
    ),
    Playlist(
        "Near Klezmer",
        track_source=tracks_near_genre_coordinates(17042, 938, max_distance=400),
    ),
    Playlist(
        "happy minor",
        track_filters=[
            filter_by_track_attribute(lambda x: x["mode"] == 0),
            filter_by_track_attribute(lambda x: x["valence"] >= 0.6),
        ],  # test filter stacking
    ),
]

_radio_playlists = []
for playlist in _playlists:
    radio_playlist = copy(playlist)
    radio_playlist.name += " - radio mode"
    radio_playlist.order_tracks_func = radio_shuffle
    _radio_playlists.append(radio_playlist)
_playlists.extend(_radio_playlists)

playlists = {playlist.name: playlist for playlist in _playlists}


if __name__ == "__main__":
    from music_tools.album import Album
    from music_tools.artist import Artist
    from music_tools.track import AudioFeatures

    Album.use_json()
    Artist.use_json()
    AudioFeatures.use_json()

    user = User()

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
