from lib.filter import (
    by_artist_attribute,
    by_genre_pattern,
    by_release_year,
    by_track_attribute,
)
from lib.playlist import Playlist
from lib.user import User

_playlists = [
    Playlist("1970s", track_filters=[by_release_year(1970, 1979)]),
    Playlist("1980s", track_filters=[by_release_year(1980, 1989)]),
    Playlist("1990s", track_filters=[by_release_year(1990, 1999)]),
    Playlist("2000s", track_filters=[by_release_year(2000, 2009)]),
    Playlist("2010s", track_filters=[by_release_year(2010, 2019)]),
    Playlist("2020s", track_filters=[by_release_year(2020, 2029)]),
    Playlist("ALL"),
    Playlist(
        "ambient",
        track_filters=[by_genre_pattern(pattern := ".*ambient.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "bad vibes",
        description="high energy, low valence",
        track_filters=[
            by_track_attribute(lambda x: x["valence"] <= 0.10 and x["energy"] > 0.6)
        ],
    ),
    Playlist(
        "classical",
        track_filters=[
            by_genre_pattern(pattern := ".*(classical|compositional).*"),
            by_artist_attribute(
                lambda x: x.id != "4aMeIY7MkJoZg7O91cmDDd"  # adrian younge
            ),
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "cool jazz",
        track_filters=[by_genre_pattern(pattern := ".*cool.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "countryish",
        track_filters=[by_genre_pattern(pattern := ".*(americana|country|cow).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "electronic",
        track_filters=[by_genre_pattern(pattern := ".*electronic.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "emo/math",
        track_filters=[by_genre_pattern(pattern := ".*(emo|math).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "escape room",
        track_filters=[by_genre_pattern(pattern := ".*escape room.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "folk",
        track_filters=[by_genre_pattern(pattern := "^(?!.*?(freak)).*folk.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "good vibes",
        description="high danceability, high valence",
        track_filters=[
            by_track_attribute(
                lambda x: x["danceability"] >= 0.5 and x["valence"] >= 0.9
            )
        ],
    ),
    Playlist(
        "goth | girl",
        track_filters=[by_genre_pattern(pattern := ".*(goth|lilith).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "happy minor",
        track_filters=[
            by_track_attribute(lambda x: x["mode"] == 0),
            by_track_attribute(lambda x: x["valence"] >= 0.6),
        ],
    ),
    Playlist(
        "hip hop",
        track_filters=[by_genre_pattern(pattern := ".*hip hop.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "indie",
        track_filters=[by_genre_pattern(pattern := ".*indie.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "japan",
        track_filters=[
            by_genre_pattern(pattern := ".*(japan|j-).*"),
            by_artist_attribute(
                lambda x: x.id
                not in {
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
            by_genre_pattern(
                pattern := "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica"
                ")).*jazz.*"
            ),
            by_artist_attribute(
                lambda x: x.id != "4aMeIY7MkJoZg7O91cmDDd"  # adrian younge
            ),
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "metal",
        track_filters=[
            by_genre_pattern(pattern := "^(?!.*?(proto-metal)).*(doom|metal|zeuhl).*")
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "post-rock",
        track_filters=[by_genre_pattern(pattern := ".*post-rock.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist("pre-1970", track_filters=[by_release_year(None, 1969)]),
    Playlist(
        "punkish",
        track_filters=[by_genre_pattern(pattern := ".*punk.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "studying",
        description="instrumental, low energy, tempo <= 120 bpm",
        track_filters=[
            by_track_attribute(
                lambda x: x["instrumentalness"] >= 0.8
                and x["energy"] <= 0.5
                and x["tempo"] <= 120
            )
        ],
    ),
    Playlist(
        "trip hop",
        track_filters=[by_genre_pattern(pattern := ".*trip.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "tropical",
        track_filters=[by_genre_pattern(pattern := ".*(brazil|latin|mpb|reggae).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "unhappy major",
        track_filters=[
            by_track_attribute(lambda x: x["mode"] == 1),
            by_track_attribute(lambda x: x["valence"] <= 0.2),
        ],
    ),
    Playlist(
        "unpopular artists",
        track_filters=[by_artist_attribute(lambda x: x.popularity <= 25)],
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
        print(f"Creating '{playlist.name}' ...")
        playlist.create(user)
