from lib.filters import (
    by_artist_attribute,
    by_genre_pattern,
    by_release_year,
    by_track_attribute,
)
from lib.playlist import Playlist
from lib.playlist_management import get_tracks_from_playlist
from lib.user import User

_playlists = [
    Playlist(
        "1970s",
        playlist_id="42oUtzFrtsjwNrSpNPSK2e",
        track_filters=[by_release_year(1970, 1979)],
    ),
    Playlist(
        "1980s",
        playlist_id="5mvhdxD9cxTbtkSo6GLUBn",
        track_filters=[by_release_year(1980, 1989)],
    ),
    Playlist(
        "1990s",
        playlist_id="5rAX8oIt6bReD50bff1ZoM",
        track_filters=[by_release_year(1990, 1999)],
    ),
    Playlist(
        "2000s",
        playlist_id="3QeKjWyXm7CQmxbI5pLSR6",
        track_filters=[by_release_year(2000, 2009)],
    ),
    Playlist(
        "2010s",
        playlist_id="5LDEewHtIdy3gg4lPReIQW",
        track_filters=[by_release_year(2010, 2019)],
    ),
    Playlist(
        "2020s",
        playlist_id="2mTcMKBO5WZf7OuBGTL9v1",
        track_filters=[by_release_year(2020, 2029)],
    ),
    Playlist("ALL", playlist_id="6vgITEENg2J5mJhW9scpns"),
    Playlist(
        "ambient",
        playlist_id="1YV73mm0afshcS0dRnUGnA",
        track_filters=[by_genre_pattern(pattern := ".*ambient.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "bad vibes",
        playlist_id="0MkeR6pcbxxHeQAzyftU13",
        description="high energy, low valence",
        track_filters=[
            by_track_attribute(lambda x: x["valence"] <= 0.10 and x["energy"] > 0.6)
        ],
    ),
    Playlist(
        "classical",
        playlist_id="3m6lx4N48ixWU0iyd2kTu6",
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
        playlist_id="5jC4kOjPOUeK9XVh4KoKrQ",
        track_filters=[by_genre_pattern(pattern := ".*cool.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "countryish",
        playlist_id="4wcgUKYWHab9mXYA2FFIKR",
        track_filters=[by_genre_pattern(pattern := ".*(americana|country|cow).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "electronic",
        playlist_id="7GMLyaUHYpikBPXA43E0qE",
        track_filters=[by_genre_pattern(pattern := ".*electronic.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "emo/math",
        playlist_id="5Oue7ZbZPNZVqShDBP0WL5",
        track_filters=[by_genre_pattern(pattern := ".*(emo|math).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "escape room",
        playlist_id="2mRBO6zOBSRLrUUExsxzHj",
        track_filters=[by_genre_pattern(pattern := ".*escape room.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "folk",
        playlist_id="0IIasIfYBu5sKpyiQFcijU",
        track_filters=[by_genre_pattern(pattern := "^(?!.*?(freak)).*folk.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "good vibes",
        playlist_id="38d8bRBySsaf6KxMMUhY7d",
        description="high danceability, high valence",
        track_filters=[
            by_track_attribute(
                lambda x: x["danceability"] >= 0.5 and x["valence"] >= 0.9
            )
        ],
    ),
    Playlist(
        "goth | girl",
        playlist_id="1jtOACTCsi2LQQ6qHjC1D3",
        track_filters=[by_genre_pattern(pattern := ".*(goth|lilith).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "happy minor",
        playlist_id="1WbpDe3WzdzW8q2i3KyHxp",
        track_filters=[
            by_track_attribute(lambda x: x["mode"] == 0),
            by_track_attribute(lambda x: x["valence"] >= 0.6),
        ],
    ),
    Playlist(
        "hip hop",
        playlist_id="4dXcWkz1kfG5Vk5EaJTx1Z",
        track_filters=[by_genre_pattern(pattern := ".*hip hop.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "indie",
        playlist_id="1gqcFVnh4TT8sHAOgdNm9u",
        track_filters=[by_genre_pattern(pattern := ".*indie.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "japan",
        playlist_id="69y36IhqWaZHAtuPP8Dda3",
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
        playlist_id="4ZflB2p06iCWXRgU3yeDUb",
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
        playlist_id="61nupgqsP4SpRPeMOlMfwR",
        track_filters=[
            by_genre_pattern(pattern := "^(?!.*?(proto-metal)).*(doom|metal|zeuhl).*")
        ],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "post-rock",
        playlist_id="3lWRWrH8k7dYevVqURwCaO",
        track_filters=[by_genre_pattern(pattern := ".*post-rock.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "pre-1970",
        playlist_id="0YgMbK1uwJrTpbUXQclxE4",
        track_filters=[by_release_year(None, 1969)],
    ),
    Playlist(
        "punkish",
        playlist_id="6EQJo56pBOtFULTOWDBWpr",
        track_filters=[by_genre_pattern(pattern := ".*punk.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "studying",
        playlist_id="1MNmGQFLADsXyGkjq0Qrj7",
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
        playlist_id="6bIR1k355xeROBieHFTaMA",
        track_filters=[by_genre_pattern(pattern := ".*trip.*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "tropical",
        playlist_id="0k4erYUPCaR0HEf722oW0v",
        track_filters=[by_genre_pattern(pattern := ".*(brazil|latin|mpb|reggae).*")],
        description=f"genre matches '{pattern}'",
    ),
    Playlist(
        "unhappy major",
        playlist_id="5gHVGnAhUpkxMCpHm4FK2m",
        track_filters=[
            by_track_attribute(lambda x: x["mode"] == 1),
            by_track_attribute(lambda x: x["valence"] <= 0.2),
        ],
    ),
    Playlist(
        "unpopular artists",
        playlist_id="5nF4jX1FpEsBC8r2ie1hPK",
        track_filters=[by_artist_attribute(lambda x: x.popularity <= 25)],
    ),
]

playlists = {playlist.name: playlist for playlist in _playlists}


if __name__ == "__main__":
    user = User()

    to_create = sorted(playlists)

    for key in to_create:
        playlist = playlists[key]

        print(f"\nGetting '{playlist.name}' tracks ...")
        playlist.get_tracks(user)

        if playlist.id is not None and set(
            get_tracks_from_playlist(playlist.id, user=user)
        ) == set(playlist.tracks):
            print(
                f"Skipping processing for '{playlist.name}' "
                f"because its tracks have not changed"
            )
            continue

        print(f"Ordering '{playlist.name}' tracks ...")
        playlist.order_tracks()

        if playlist.id is None:
            print(f"Creating '{playlist.name}' ...")
            playlist.create(user)
        else:
            print(f"Recreating '{playlist.name}' ...")
            playlist.recreate(user)
