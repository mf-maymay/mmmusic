from mmmusic.data import playlist_ids
from mmmusic.models.playlist_configs import PlaylistConfig
from mmmusic.processors import (
    exclude_artists,
    filter_by_artist_attribute,
    filter_by_audio_feature,
    filter_by_genre_pattern,
    filter_by_mode,
    filter_by_number_of_tracks,
    filter_by_release_year,
    filter_by_similarity_to_track,
    filter_by_track_attribute,
    order_by_popularity,
)
from mmmusic.shuffling import smart_shuffle
from mmmusic.track_sources import from_playlist, from_playlist_config

regular_playlists = [
    PlaylistConfig(
        name="1970s",
        id="42oUtzFrtsjwNrSpNPSK2e",
        processors=[filter_by_release_year(1970, 1980), smart_shuffle],
    ),
    PlaylistConfig(
        name="1980s",
        id="5mvhdxD9cxTbtkSo6GLUBn",
        processors=[filter_by_release_year(1980, 1990), smart_shuffle],
    ),
    PlaylistConfig(
        name="1990s",
        id="5rAX8oIt6bReD50bff1ZoM",
        processors=[filter_by_release_year(1990, 2000), smart_shuffle],
    ),
    PlaylistConfig(
        name="2000s",
        id="3QeKjWyXm7CQmxbI5pLSR6",
        processors=[filter_by_release_year(2000, 2010), smart_shuffle],
    ),
    PlaylistConfig(
        name="2010s",
        id="5LDEewHtIdy3gg4lPReIQW",
        processors=[filter_by_release_year(2010, 2020), smart_shuffle],
    ),
    PlaylistConfig(
        name="2020s",
        id="2mTcMKBO5WZf7OuBGTL9v1",
        processors=[filter_by_release_year(2020, 2030), smart_shuffle],
    ),
    PlaylistConfig(
        name="ALL",
        id="6vgITEENg2J5mJhW9scpns",
        processors=[smart_shuffle],
    ),
    PlaylistConfig(
        name="ALL, sample",
        id="2f8Lu0VER9CrwSqZndysMb",
        processors=[
            filter_by_number_of_tracks(500, randomly_sampled=True),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="ALL, ordered by popularity",
        id="7DpWFkySsh4Jb4RwhsM5HH",
        processors=[order_by_popularity],
    ),
    PlaylistConfig(
        name="Above, From Within",
        id="3OjqZQOnQ35w8ePyelTxA1",
        processors=[
            filter_by_similarity_to_track(
                "0PFUMcpS4oeobzD3Tqre7w",  # Andromeda's Suffering
                number_of_tracks=200,
            ),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="Ankou's Last Stand",
        id="4lyNSFxJIpJBDTP9wUq4C1",
        processors=[
            filter_by_similarity_to_track(
                "1ibHApXtb0pgplmNDRLHrJ",  # Achilles last stand
                number_of_tracks=69,
            ),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="Battle in the Spirit Leech's Dream World",
        id="1YlzmYdLyFFXwclJIWoZB5",
        processors=[
            filter_by_similarity_to_track(
                "4X2xFHqUSRmyH9sQmfwCP2",  # To Never Return
                number_of_tracks=200,
            ),
            smart_shuffle,
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
        processors=[filter_by_genre_pattern(".*ambient.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="bad vibes",
        id="0MkeR6pcbxxHeQAzyftU13",
        processors=[
            filter_by_audio_feature("valence", upper_bound=0.10),
            filter_by_audio_feature("energy", lower_bound=0.6),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="blues",
        id="1PoISoAlzhps4yjoZkL3ma",
        processors=[filter_by_genre_pattern(".*blues.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="classical",
        id="3m6lx4N48ixWU0iyd2kTu6",
        processors=[
            filter_by_genre_pattern(".*(classical|compositional).*"),
            exclude_artists("4aMeIY7MkJoZg7O91cmDDd"),  # adrian younge
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="cool jazz",
        id="5jC4kOjPOUeK9XVh4KoKrQ",
        processors=[filter_by_genre_pattern(".*cool.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="countryish",
        id="4wcgUKYWHab9mXYA2FFIKR",
        processors=[
            filter_by_genre_pattern(".*(americana|country|cow).*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="electronic",
        id="7GMLyaUHYpikBPXA43E0qE",
        processors=[
            filter_by_genre_pattern(".*electronic.*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="emo/math",
        id="5Oue7ZbZPNZVqShDBP0WL5",
        processors=[
            filter_by_genre_pattern(".*(emo|math).*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="escape room",
        id="2mRBO6zOBSRLrUUExsxzHj",
        processors=[
            filter_by_genre_pattern(".*escape room.*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="folk",
        id="0IIasIfYBu5sKpyiQFcijU",
        processors=[
            filter_by_genre_pattern("^(?!.*?(freak)).*folk.*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="good vibes",
        id="38d8bRBySsaf6KxMMUhY7d",
        processors=[
            filter_by_audio_feature("danceability", lower_bound=0.5),
            filter_by_audio_feature("valence", lower_bound=0.9),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="goth, industrial",
        id="1jtOACTCsi2LQQ6qHjC1D3",
        processors=[
            filter_by_genre_pattern("^(?!.*?(gothenburg)).*(goth|industrial).*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="happy minor",
        id="1WbpDe3WzdzW8q2i3KyHxp",
        processors=[
            filter_by_mode("minor"),
            filter_by_audio_feature("valence", lower_bound=0.6),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="hip hop",
        id="4dXcWkz1kfG5Vk5EaJTx1Z",
        processors=[filter_by_genre_pattern(".*hip hop.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="indie",
        id="1gqcFVnh4TT8sHAOgdNm9u",
        processors=[filter_by_genre_pattern(".*indie.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="japan",
        id="69y36IhqWaZHAtuPP8Dda3",
        processors=[
            filter_by_genre_pattern(".*(japan|j-).*"),
            exclude_artists(
                "7C2DSqaNkh0w77O5Jz1FKh",  # archie shepp
                "5jtGuhEEDh07yaFfm8qHg7",  # cecil taylor
                "3uPWecBPNXAChysw1uOJwI",  # don cherry
                "6rxxu32JCGDpKKMPHxnSJp",  # eric dolphy
                "3BG0nwVh3Gc7cuT4XdsLtt",  # joe henderson
                "1EpLpC0tbCla8knfhET78p",  # mccoy tyner trio
                "47odibUtrN3lnWx0p0pk2P",  # ornette coleman
            ),
            smart_shuffle,
        ],
    ),
    (
        jazz_playlist_config := PlaylistConfig(
            name="jazz",
            id="4ZflB2p06iCWXRgU3yeDUb",
            processors=[
                filter_by_genre_pattern(
                    (
                        "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica))"
                        ".*jazz.*"
                    )
                ),
                exclude_artists("4aMeIY7MkJoZg7O91cmDDd"),  # adrian younge
                smart_shuffle,
            ],
        )
    ),
    PlaylistConfig(
        name="bitter jazz",
        id="6NFebq22RoaEuXPk5rwGXL",
        track_source=from_playlist_config(jazz_playlist_config),
        processors=[
            filter_by_audio_feature("valence", upper_bound=0.2),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="metal",
        id="61nupgqsP4SpRPeMOlMfwR",
        processors=[
            filter_by_genre_pattern("^(?!.*?(proto-metal)).*(doom|metal|zeuhl).*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="popular artists",
        id="08pLTWx8LB58syQ8c7lXuW",
        processors=[
            filter_by_artist_attribute("popularity", lower_bound=70),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="popular tracks",
        id="60BlxvTBWRivesoeC2YEWI",
        processors=[
            filter_by_track_attribute("popularity", lower_bound=65),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="post-rock",
        id="3lWRWrH8k7dYevVqURwCaO",
        processors=[filter_by_genre_pattern(".*post-rock.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="pre-1970",
        id="0YgMbK1uwJrTpbUXQclxE4",
        processors=[filter_by_release_year(end_year=1970), smart_shuffle],
    ),
    PlaylistConfig(
        name="punkish",
        id="6EQJo56pBOtFULTOWDBWpr",
        processors=[filter_by_genre_pattern(".*punk.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="studying",
        id="1MNmGQFLADsXyGkjq0Qrj7",
        processors=[
            filter_by_audio_feature("instrumentalness", lower_bound=0.8),
            filter_by_audio_feature("energy", upper_bound=0.5),
            filter_by_audio_feature("tempo", upper_bound=120),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="trip hop",
        id="6bIR1k355xeROBieHFTaMA",
        processors=[filter_by_genre_pattern(".*trip.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="tropical",
        id="0k4erYUPCaR0HEf722oW0v",
        processors=[
            filter_by_genre_pattern(".*(brazil|latin|mpb|reggae).*"),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="unhappy major",
        id="5gHVGnAhUpkxMCpHm4FK2m",
        processors=[
            filter_by_mode("major"),
            filter_by_audio_feature("valence", upper_bound=0.2),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="unpopular artists",
        id="5nF4jX1FpEsBC8r2ie1hPK",
        processors=[
            filter_by_artist_attribute("popularity", upper_bound=25),
            smart_shuffle,
        ],
    ),
]

q_playlists = [
    PlaylistConfig(
        name="q - harder",
        id="5mRa71QUmE6EWavxTA22g6",
        processors=[
            filter_by_genre_pattern("^(?!.*?(hop|rap)).*(core|doom|metal|punk).*"),
            smart_shuffle,
        ],
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - hop",
        id="0sFhYQaTiuZlG1vMDSiFMR",
        track_source=from_playlist(playlist_ids.Q_ALL),
        processors=[filter_by_genre_pattern(".*(hop|rap).*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="q - jazz",
        id="4HQnus8hcLfX5pYtG95pKY",
        track_source=from_playlist(playlist_ids.Q_ALL),
        processors=[filter_by_genre_pattern(".*jazz.*"), smart_shuffle],
    ),
    PlaylistConfig(
        name="q - misc",
        id="7DOqATuWsl640ustK8lhhI",
        track_source=from_playlist(playlist_ids.Q_ALL),
        processors=[
            filter_by_genre_pattern(
                "^(?!.*?(core|doom|hop|jazz|metal|punk|rap|rock)).*"
            ),
            smart_shuffle,
        ],
    ),
    PlaylistConfig(
        name="q - rock",
        id="1tlzpLpRdQXUicLbhIJMcM",
        track_source=from_playlist(playlist_ids.Q_ALL),
        processors=[filter_by_genre_pattern(".*rock.*"), smart_shuffle],
    ),
]
