from lib.data import playlist_ids
from lib.filters import (
    by_artist_attribute,
    by_genre_pattern,
    by_number_of_tracks,
    by_release_year,
    by_similarity_to_track,
    by_track_attribute,
)
from lib.models.playlist_configs import PlaylistConfig
from lib.track_sources import from_playlist

regular_playlists = [
    PlaylistConfig(
        name="1970s",
        id="42oUtzFrtsjwNrSpNPSK2e",
        track_filters=[by_release_year(1970, 1979)],
    ),
    PlaylistConfig(
        name="1980s",
        id="5mvhdxD9cxTbtkSo6GLUBn",
        track_filters=[by_release_year(1980, 1989)],
    ),
    PlaylistConfig(
        name="1990s",
        id="5rAX8oIt6bReD50bff1ZoM",
        track_filters=[by_release_year(1990, 1999)],
    ),
    PlaylistConfig(
        name="2000s",
        id="3QeKjWyXm7CQmxbI5pLSR6",
        track_filters=[by_release_year(2000, 2009)],
    ),
    PlaylistConfig(
        name="2010s",
        id="5LDEewHtIdy3gg4lPReIQW",
        track_filters=[by_release_year(2010, 2019)],
    ),
    PlaylistConfig(
        name="2020s",
        id="2mTcMKBO5WZf7OuBGTL9v1",
        track_filters=[by_release_year(2020, 2029)],
    ),
    PlaylistConfig(name="ALL", id="6vgITEENg2J5mJhW9scpns"),
    PlaylistConfig(
        name="ALL, sample",
        id="2f8Lu0VER9CrwSqZndysMb",
        track_filters=[by_number_of_tracks(500, randomly_sampled=True)],
    ),
    PlaylistConfig(
        name="ALL, ordered by popularity",
        id="7DpWFkySsh4Jb4RwhsM5HH",
        order_tracks_func=lambda tracks: sorted(
            tracks,
            key=lambda track: track.popularity,
            reverse=True,
        ),
    ),
    PlaylistConfig(
        name="Ankou's Last Stand",
        id="4lyNSFxJIpJBDTP9wUq4C1",
        track_filters=[
            by_similarity_to_track(
                "1ibHApXtb0pgplmNDRLHrJ",  # Achilles last stand
            ),
            by_number_of_tracks(69),
        ],
    ),
    PlaylistConfig(
        name="Battle in the Spirit Leech's Dream World",
        id="1YlzmYdLyFFXwclJIWoZB5",
        track_filters=[
            by_similarity_to_track(
                "4X2xFHqUSRmyH9sQmfwCP2",  # To Never Return
            ),
            by_number_of_tracks(200),
        ],
    ),
    PlaylistConfig(
        name="Collecting Dust",
        id="5WQsnHNLsZSdqXdM6S63Kr",
        track_source=from_playlist("5WQsnHNLsZSdqXdM6S63Kr"),
    ),
    PlaylistConfig(
        name="Monsters and Trains",
        id="67azW1qgFpSn7MDYO2QTl1",
        track_source=from_playlist("67azW1qgFpSn7MDYO2QTl1"),
    ),
    PlaylistConfig(
        name="ambient",
        id="1YV73mm0afshcS0dRnUGnA",
        track_filters=[by_genre_pattern(pattern := ".*ambient.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="bad vibes",
        id="0MkeR6pcbxxHeQAzyftU13",
        description="high energy, low valence",
        track_filters=[
            by_track_attribute(lambda x: x["valence"] <= 0.10 and x["energy"] > 0.6)
        ],
    ),
    PlaylistConfig(
        name="classical",
        id="3m6lx4N48ixWU0iyd2kTu6",
        track_filters=[
            by_genre_pattern(pattern := ".*(classical|compositional).*"),
            by_artist_attribute(
                lambda x: x.id != "4aMeIY7MkJoZg7O91cmDDd"  # adrian younge
            ),
        ],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="cool jazz",
        id="5jC4kOjPOUeK9XVh4KoKrQ",
        track_filters=[by_genre_pattern(pattern := ".*cool.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="countryish",
        id="4wcgUKYWHab9mXYA2FFIKR",
        track_filters=[by_genre_pattern(pattern := ".*(americana|country|cow).*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="electronic",
        id="7GMLyaUHYpikBPXA43E0qE",
        track_filters=[by_genre_pattern(pattern := ".*electronic.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="emo/math",
        id="5Oue7ZbZPNZVqShDBP0WL5",
        track_filters=[by_genre_pattern(pattern := ".*(emo|math).*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="escape room",
        id="2mRBO6zOBSRLrUUExsxzHj",
        track_filters=[by_genre_pattern(pattern := ".*escape room.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="folk",
        id="0IIasIfYBu5sKpyiQFcijU",
        track_filters=[by_genre_pattern(pattern := "^(?!.*?(freak)).*folk.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="good vibes",
        id="38d8bRBySsaf6KxMMUhY7d",
        description="high danceability, high valence",
        track_filters=[
            by_track_attribute(
                lambda x: x["danceability"] >= 0.5 and x["valence"] >= 0.9
            )
        ],
    ),
    PlaylistConfig(
        name="goth, industrial",
        id="1jtOACTCsi2LQQ6qHjC1D3",
        track_filters=[by_genre_pattern(pattern := ".*(goth|industrial).*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="happy minor",
        id="1WbpDe3WzdzW8q2i3KyHxp",
        track_filters=[
            by_track_attribute(lambda x: x["mode"] == 0),
            by_track_attribute(lambda x: x["valence"] >= 0.6),
        ],
    ),
    PlaylistConfig(
        name="hip hop",
        id="4dXcWkz1kfG5Vk5EaJTx1Z",
        track_filters=[by_genre_pattern(pattern := ".*hip hop.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="incense",
        id="61uEa4n0JSywxfjccpW1fk",
        track_filters=[
            by_track_attribute(lambda x: 60 <= x["tempo"] <= 80),
            by_track_attribute(lambda x: x["acousticness"] >= 0.5),
            by_track_attribute(lambda x: 0.3 <= x["energy"] <= 0.7),
            by_track_attribute(lambda x: x["danceability"] <= 0.5),
            by_track_attribute(lambda x: x["valence"] >= 0.5),
            by_track_attribute(lambda x: x["liveness"] <= 0.5),
        ],
    ),
    PlaylistConfig(
        name="indie",
        id="1gqcFVnh4TT8sHAOgdNm9u",
        track_filters=[by_genre_pattern(pattern := ".*indie.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="japan",
        id="69y36IhqWaZHAtuPP8Dda3",
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
    PlaylistConfig(
        name="jazz",
        id="4ZflB2p06iCWXRgU3yeDUb",
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
    PlaylistConfig(
        name="metal",
        id="61nupgqsP4SpRPeMOlMfwR",
        track_filters=[
            by_genre_pattern(pattern := "^(?!.*?(proto-metal)).*(doom|metal|zeuhl).*")
        ],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="popular artists",
        id="08pLTWx8LB58syQ8c7lXuW",
        track_filters=[by_artist_attribute(lambda x: x.popularity >= 70)],
    ),
    PlaylistConfig(
        name="popular tracks",
        id="60BlxvTBWRivesoeC2YEWI",
        track_filters=[by_track_attribute(lambda x: x.popularity >= 65)],
    ),
    PlaylistConfig(
        name="post-rock",
        id="3lWRWrH8k7dYevVqURwCaO",
        track_filters=[by_genre_pattern(pattern := ".*post-rock.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="pre-1970",
        id="0YgMbK1uwJrTpbUXQclxE4",
        track_filters=[by_release_year(None, 1969)],
    ),
    PlaylistConfig(
        name="punkish",
        id="6EQJo56pBOtFULTOWDBWpr",
        track_filters=[by_genre_pattern(pattern := ".*punk.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="studying",
        id="1MNmGQFLADsXyGkjq0Qrj7",
        description="instrumental, low energy, tempo <= 120 bpm",
        track_filters=[
            by_track_attribute(
                lambda x: x["instrumentalness"] >= 0.8
                and x["energy"] <= 0.5
                and x["tempo"] <= 120
            )
        ],
    ),
    PlaylistConfig(
        name="trip hop",
        id="6bIR1k355xeROBieHFTaMA",
        track_filters=[by_genre_pattern(pattern := ".*trip.*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="tropical",
        id="0k4erYUPCaR0HEf722oW0v",
        track_filters=[by_genre_pattern(pattern := ".*(brazil|latin|mpb|reggae).*")],
        description=f"genre matches '{pattern}'",
    ),
    PlaylistConfig(
        name="unhappy major",
        id="5gHVGnAhUpkxMCpHm4FK2m",
        track_filters=[
            by_track_attribute(lambda x: x["mode"] == 1),
            by_track_attribute(lambda x: x["valence"] <= 0.2),
        ],
    ),
    PlaylistConfig(
        name="unpopular artists",
        id="5nF4jX1FpEsBC8r2ie1hPK",
        track_filters=[by_artist_attribute(lambda x: x.popularity <= 25)],
    ),
]

q_playlists = [
    PlaylistConfig(
        name="q - harder",
        id="5mRa71QUmE6EWavxTA22g6",
        track_filters=[by_genre_pattern("^(?!.*?(hop|rap)).*(core|doom|metal|punk).*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - hop",
        id="0sFhYQaTiuZlG1vMDSiFMR",
        track_filters=[by_genre_pattern(".*(hop|rap).*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - jazz",
        id="4HQnus8hcLfX5pYtG95pKY",
        track_filters=[by_genre_pattern(".*jazz.*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - misc",
        id="7DOqATuWsl640ustK8lhhI",
        track_filters=[
            by_genre_pattern("^(?!.*?(core|doom|hop|jazz|metal|punk|rap|rock)).*")
        ],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - rock",
        id="1tlzpLpRdQXUicLbhIJMcM",
        track_filters=[by_genre_pattern(".*rock.*")],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
]
