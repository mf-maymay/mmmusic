# -*- coding: utf-8 -*-
from music_tools.playlist import Playlist
from music_tools.playlist_utils import (
    filter_by_artist_attribute,
    filter_by_genre_coordinates,
    filter_by_genre_pattern,
    filter_by_release_year,
    filter_by_track_attribute,
)
from music_tools.user import User

_playlists = [
    Playlist("1970s", track_filters=[filter_by_release_year(1970, 1979)]),
    Playlist("1980s", track_filters=[filter_by_release_year(1980, 1989)]),
    Playlist("1990s", track_filters=[filter_by_release_year(1990, 1999)]),
    Playlist("2000s", track_filters=[filter_by_release_year(2000, 2009)]),
    Playlist("2010s", track_filters=[filter_by_release_year(2010, 2019)]),
    Playlist("2020s", track_filters=[filter_by_release_year(2020, 2029)]),
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
        track_filters=[
            filter_by_genre_pattern(pattern := ".*(classical|compositional).*"),
            filter_by_artist_attribute(
                lambda x: x.id != "4aMeIY7MkJoZg7O91cmDDd"  # adrian younge
            ),
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "cool",
        track_filters=[
            filter_by_genre_pattern(pattern := ".*cool.*")
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "countryish",
        track_filters=[
            filter_by_genre_pattern(pattern := ".*(americana|country|cow).*")
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "emo/math",
        track_filters=[filter_by_genre_pattern(pattern := ".*(emo|math).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "escape room",
        track_filters=[filter_by_genre_pattern(pattern := ".*escape room.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "folk",
        track_filters=[filter_by_genre_pattern(pattern := "^(?!.*?(freak)).*folk.*")],
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
        track_filters=[filter_by_genre_pattern(pattern := ".*(goth|lilith).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "happy minor",
        track_filters=[
            filter_by_track_attribute(lambda x: x["mode"] == 0),
            filter_by_track_attribute(lambda x: x["valence"] >= 0.6),
        ],
    ),
    Playlist(
        "hip hop",
        track_filters=[filter_by_genre_pattern(pattern := ".*hip hop.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "indie",
        track_filters=[filter_by_genre_pattern(pattern := ".*indie.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "japan",
        track_filters=[
            filter_by_genre_pattern(pattern := ".*(japan|j-).*"),
            filter_by_artist_attribute(
                lambda x: x.id not in {
                    "7C2DSqaNkh0w77O5Jz1FKh",  # archie shepp
                    "5jtGuhEEDh07yaFfm8qHg7",  # cecil taylor
                    "3uPWecBPNXAChysw1uOJwI",  # don cherry
                    "6rxxu32JCGDpKKMPHxnSJp",  # eric dolphy
                    "3BG0nwVh3Gc7cuT4XdsLtt",  # joe henderson
                    "1EpLpC0tbCla8knfhET78p",  # mccoy tyner trio
                    "47odibUtrN3lnWx0p0pk2P",  # ornette coleman
                }
            ),
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "jazz",
        track_filters=[
            filter_by_genre_pattern(
                pattern := "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica"
                ")).*jazz.*"
            ),
            filter_by_artist_attribute(
                lambda x: x.id != "4aMeIY7MkJoZg7O91cmDDd"  # adrian younge
            ),
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "metal",
        track_filters=[
            filter_by_genre_pattern(
                pattern := "^(?!.*?(proto-metal)).*(doom|metal|zeuhl).*"
            )
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "post-rock",
        track_filters=[filter_by_genre_pattern(pattern := ".*post-rock.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist("pre-1970", track_filters=[filter_by_release_year(None, 1969)]),
    Playlist(
        "punkish",
        track_filters=[filter_by_genre_pattern(pattern := ".*punk.*")],
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
        track_filters=[
            filter_by_genre_pattern(pattern := ".*(brazil|latin|mpb|reggae).*")
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "unhappy major",
        track_filters=[
            filter_by_track_attribute(lambda x: x["mode"] == 1),
            filter_by_track_attribute(lambda x: x["valence"] <= 0.2),
        ],
    ),
    Playlist(
        "unpopular artists",
        track_filters=[filter_by_artist_attribute(lambda x: x.popularity <= 25)],
    ),
    # ------- experimental -------
    Playlist(
        "near Hailu Mergia",
        track_filters=[filter_by_genre_coordinates(11841, 780, max_distance=350)],
    ),
    Playlist(
        "near Mamaleek",
        track_filters=[filter_by_genre_coordinates(10067, 146, max_distance=250)],
    ),
    Playlist(
        "near Nick Cave & The Bad Seeds",
        track_filters=[filter_by_genre_coordinates(8399, 489, max_distance=200)],
    ),
]

playlists = {playlist.name: playlist for playlist in _playlists}


if __name__ == "__main__":
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
