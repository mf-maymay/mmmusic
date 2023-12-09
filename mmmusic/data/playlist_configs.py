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
from mmmusic.track_sources import from_playlist, from_playlist_config

regular_playlists = [
    PlaylistConfig(
        name="1970s",
        id="42oUtzFrtsjwNrSpNPSK2e",
        track_list_processor=filter_by_release_year(1970, 1980),
    ),
    PlaylistConfig(
        name="1980s",
        id="5mvhdxD9cxTbtkSo6GLUBn",
        track_list_processor=filter_by_release_year(1980, 1990),
    ),
    PlaylistConfig(
        name="1990s",
        id="5rAX8oIt6bReD50bff1ZoM",
        track_list_processor=filter_by_release_year(1990, 2000),
    ),
    PlaylistConfig(
        name="2000s",
        id="3QeKjWyXm7CQmxbI5pLSR6",
        track_list_processor=filter_by_release_year(2000, 2010),
    ),
    PlaylistConfig(
        name="2010s",
        id="5LDEewHtIdy3gg4lPReIQW",
        track_list_processor=filter_by_release_year(2010, 2020),
    ),
    PlaylistConfig(
        name="2020s",
        id="2mTcMKBO5WZf7OuBGTL9v1",
        track_list_processor=filter_by_release_year(2020, 2030),
    ),
    PlaylistConfig(name="ALL", id="6vgITEENg2J5mJhW9scpns"),
    PlaylistConfig(
        name="ALL, sample",
        id="2f8Lu0VER9CrwSqZndysMb",
        track_list_processor=filter_by_number_of_tracks(500, randomly_sampled=True),
    ),
    PlaylistConfig(
        name="ALL, ordered by popularity",
        id="7DpWFkySsh4Jb4RwhsM5HH",
        order_tracks_func=order_by_popularity,
    ),
    PlaylistConfig(
        name="Ankou's Last Stand",
        id="4lyNSFxJIpJBDTP9wUq4C1",
        track_list_processor=filter_by_similarity_to_track(
            "1ibHApXtb0pgplmNDRLHrJ",  # Achilles last stand
        )
        & filter_by_number_of_tracks(69),
    ),
    PlaylistConfig(
        name="Battle in the Spirit Leech's Dream World",
        id="1YlzmYdLyFFXwclJIWoZB5",
        track_list_processor=filter_by_similarity_to_track(
            "4X2xFHqUSRmyH9sQmfwCP2",  # To Never Return
        )
        & filter_by_number_of_tracks(200),
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
        track_list_processor=filter_by_genre_pattern(pattern := ".*ambient.*"),
    ),
    PlaylistConfig(
        name="bad vibes",
        id="0MkeR6pcbxxHeQAzyftU13",
        track_list_processor=filter_by_audio_feature("valence", upper_bound=0.10)
        & filter_by_audio_feature("energy", lower_bound=0.6),
    ),
    PlaylistConfig(
        name="classical",
        id="3m6lx4N48ixWU0iyd2kTu6",
        track_list_processor=filter_by_genre_pattern(
            pattern := ".*(classical|compositional).*"
        )
        & exclude_artists("4aMeIY7MkJoZg7O91cmDDd"),  # adrian younge
    ),
    PlaylistConfig(
        name="cool jazz",
        id="5jC4kOjPOUeK9XVh4KoKrQ",
        track_list_processor=filter_by_genre_pattern(pattern := ".*cool.*"),
    ),
    PlaylistConfig(
        name="countryish",
        id="4wcgUKYWHab9mXYA2FFIKR",
        track_list_processor=filter_by_genre_pattern(
            pattern := ".*(americana|country|cow).*"
        ),
    ),
    PlaylistConfig(
        name="electronic",
        id="7GMLyaUHYpikBPXA43E0qE",
        track_list_processor=filter_by_genre_pattern(pattern := ".*electronic.*"),
    ),
    PlaylistConfig(
        name="emo/math",
        id="5Oue7ZbZPNZVqShDBP0WL5",
        track_list_processor=filter_by_genre_pattern(pattern := ".*(emo|math).*"),
    ),
    PlaylistConfig(
        name="escape room",
        id="2mRBO6zOBSRLrUUExsxzHj",
        track_list_processor=filter_by_genre_pattern(pattern := ".*escape room.*"),
    ),
    PlaylistConfig(
        name="folk",
        id="0IIasIfYBu5sKpyiQFcijU",
        track_list_processor=filter_by_genre_pattern(
            pattern := "^(?!.*?(freak)).*folk.*"
        ),
    ),
    PlaylistConfig(
        name="good vibes",
        id="38d8bRBySsaf6KxMMUhY7d",
        track_list_processor=filter_by_audio_feature("danceability", lower_bound=0.5)
        & filter_by_audio_feature("valence", lower_bound=0.9),
    ),
    PlaylistConfig(
        name="goth, industrial",
        id="1jtOACTCsi2LQQ6qHjC1D3",
        track_list_processor=filter_by_genre_pattern(
            pattern := "^(?!.*?(gothenburg)).*(goth|industrial).*"
        ),
    ),
    PlaylistConfig(
        name="happy minor",
        id="1WbpDe3WzdzW8q2i3KyHxp",
        track_list_processor=filter_by_mode("minor")
        & filter_by_audio_feature("valence", lower_bound=0.6),
    ),
    PlaylistConfig(
        name="hip hop",
        id="4dXcWkz1kfG5Vk5EaJTx1Z",
        track_list_processor=filter_by_genre_pattern(pattern := ".*hip hop.*"),
    ),
    PlaylistConfig(
        name="indie",
        id="1gqcFVnh4TT8sHAOgdNm9u",
        track_list_processor=filter_by_genre_pattern(pattern := ".*indie.*"),
    ),
    PlaylistConfig(
        name="japan",
        id="69y36IhqWaZHAtuPP8Dda3",
        track_list_processor=filter_by_genre_pattern(pattern := ".*(japan|j-).*")
        & exclude_artists(
            "7C2DSqaNkh0w77O5Jz1FKh",  # archie shepp
            "5jtGuhEEDh07yaFfm8qHg7",  # cecil taylor
            "3uPWecBPNXAChysw1uOJwI",  # don cherry
            "6rxxu32JCGDpKKMPHxnSJp",  # eric dolphy
            "3BG0nwVh3Gc7cuT4XdsLtt",  # joe henderson
            "1EpLpC0tbCla8knfhET78p",  # mccoy tyner trio
            "47odibUtrN3lnWx0p0pk2P",  # ornette coleman
        ),
    ),
    (
        jazz_playlist_config := PlaylistConfig(
            name="jazz",
            id="4ZflB2p06iCWXRgU3yeDUb",
            track_list_processor=filter_by_genre_pattern(
                pattern := (
                    "^(?!.*?(core|dark|fusion|nu|jazz metal|jazz rap|jazztronica))"
                    ".*jazz.*"
                )
            )
            & exclude_artists("4aMeIY7MkJoZg7O91cmDDd"),  # adrian younge
        )
    ),
    PlaylistConfig(
        name="bitter jazz",
        id="6NFebq22RoaEuXPk5rwGXL",
        track_source=from_playlist_config(jazz_playlist_config),
        track_list_processor=filter_by_audio_feature("valence", upper_bound=0.2),
    ),
    PlaylistConfig(
        name="metal",
        id="61nupgqsP4SpRPeMOlMfwR",
        track_list_processor=filter_by_genre_pattern(
            pattern := "^(?!.*?(proto-metal)).*(doom|metal|zeuhl).*"
        ),
    ),
    PlaylistConfig(
        name="popular artists",
        id="08pLTWx8LB58syQ8c7lXuW",
        track_list_processor=filter_by_artist_attribute("popularity", lower_bound=70),
    ),
    PlaylistConfig(
        name="popular tracks",
        id="60BlxvTBWRivesoeC2YEWI",
        track_list_processor=filter_by_track_attribute("popularity", lower_bound=65),
    ),
    PlaylistConfig(
        name="post-rock",
        id="3lWRWrH8k7dYevVqURwCaO",
        track_list_processor=filter_by_genre_pattern(pattern := ".*post-rock.*"),
    ),
    PlaylistConfig(
        name="pre-1970",
        id="0YgMbK1uwJrTpbUXQclxE4",
        track_list_processor=filter_by_release_year(end_year=1970),
    ),
    PlaylistConfig(
        name="punkish",
        id="6EQJo56pBOtFULTOWDBWpr",
        track_list_processor=filter_by_genre_pattern(pattern := ".*punk.*"),
    ),
    PlaylistConfig(
        name="studying",
        id="1MNmGQFLADsXyGkjq0Qrj7",
        track_list_processor=filter_by_audio_feature(
            "instrumentalness", lower_bound=0.8
        )
        & filter_by_audio_feature("energy", upper_bound=0.5)
        & filter_by_audio_feature("tempo", upper_bound=120),
    ),
    PlaylistConfig(
        name="trip hop",
        id="6bIR1k355xeROBieHFTaMA",
        track_list_processor=filter_by_genre_pattern(pattern := ".*trip.*"),
    ),
    PlaylistConfig(
        name="tropical",
        id="0k4erYUPCaR0HEf722oW0v",
        track_list_processor=filter_by_genre_pattern(
            pattern := ".*(brazil|latin|mpb|reggae).*"
        ),
    ),
    PlaylistConfig(
        name="unhappy major",
        id="5gHVGnAhUpkxMCpHm4FK2m",
        track_list_processor=filter_by_mode("major")
        & filter_by_audio_feature("valence", upper_bound=0.2),
    ),
    PlaylistConfig(
        name="unpopular artists",
        id="5nF4jX1FpEsBC8r2ie1hPK",
        track_list_processor=filter_by_artist_attribute("popularity", upper_bound=25),
    ),
]

q_playlists = [
    PlaylistConfig(
        name="q - harder",
        id="5mRa71QUmE6EWavxTA22g6",
        track_list_processor=filter_by_genre_pattern(
            "^(?!.*?(hop|rap)).*(core|doom|metal|punk).*"
        ),
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - hop",
        id="0sFhYQaTiuZlG1vMDSiFMR",
        track_list_processor=filter_by_genre_pattern(".*(hop|rap).*"),
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - jazz",
        id="4HQnus8hcLfX5pYtG95pKY",
        track_list_processor=filter_by_genre_pattern(".*jazz.*"),
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - misc",
        id="7DOqATuWsl640ustK8lhhI",
        track_list_processor=filter_by_genre_pattern(
            "^(?!.*?(core|doom|hop|jazz|metal|punk|rap|rock)).*"
        ),
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
    PlaylistConfig(
        name="q - rock",
        id="1tlzpLpRdQXUicLbhIJMcM",
        track_list_processor=filter_by_genre_pattern(".*rock.*"),
        track_source=from_playlist(playlist_ids.Q_ALL),
    ),
]
