# -*- coding: utf-8 -*-
from dataclasses import dataclass
from functools import lru_cache

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from music_tools.utils import no_timeout

AUDIO_FEATURE_FIELDS = (
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)


@dataclass(init=False, order=True, frozen=True)  # TODO: add slots=True
class Track:
    __slots__ = ("name", "id", "album_id", "artist_ids", "_audio_features")

    name: str
    id: str
    album_id: str  # TODO: replace with Album instance
    artist_ids: tuple  # TODO: replace with Artist instances

    get_json = lru_cache(maxsize=None)(no_timeout(sp.track))

    def __init__(self, track_id):
        if hasattr(track_id, "id"):
            # Track(Track(track_id)) == Track(track_id)
            track_id = track_id.id
        super().__setattr__("id", track_id)

        info = type(self).get_json(track_id)

        super().__setattr__("name", info["name"])
        super().__setattr__("album_id", info["album"]["id"])
        super().__setattr__(
            "artist_ids", tuple(artist["id"] for artist in info["artists"])
        )

        super().__setattr__("_audio_features", None)

    @property
    def audio_features(self):
        if self._audio_features is None:
            super().__setattr__("_audio_features", AudioFeatures(self))
        return self._audio_features

    def __getitem__(self, key):  # TODO: remove ?
        return self.audio_features[key]


@dataclass(init=False, frozen=True)  # TODO: add slots=True
class AudioFeatures:
    __slots__ = ("id", *AUDIO_FEATURE_FIELDS)

    id: str
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    valence: float

    get_json = lru_cache(maxsize=None)(no_timeout(sp.audio_features))

    def __init__(self, track_id):
        if hasattr(track_id, "id"):
            # AudioFeatures(Track(track_id)) == AudioFeatures(track_id)
            track_id = track_id.id
        super().__setattr__("id", track_id)

        info = type(self).get_json(track_id)[0]

        for field in AUDIO_FEATURE_FIELDS:
            super().__setattr__(field, info[field])

    def __getitem__(self, key):
        return getattr(self, key)


if __name__ == "__main__":
    track_ids = [
        "0vFabeTqtOtj918sjc5vYo",
        "3HWxpLKnTlz6jE3Vi5dTF2",
        "6PSma9xvYhGabJNrbUAE4e",
        "3qSJD2hjnZ7YDOQx9ieQ0m",
        "09uV1Sli9wapcKQmmyaG4E",
        "5vaCmKjItq2Da5BKNFHlEb",
    ]

    tracks = [Track(x) for x in track_ids]

    track = tracks[0]

    features = track.audio_features
