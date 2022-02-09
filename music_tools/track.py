# -*- coding: utf-8 -*-
from dataclasses import dataclass
from functools import lru_cache

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from music_tools.base_class import SpotifyObjectBase
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


class Track(SpotifyObjectBase):
    FIELDS = ("id", "name", "album_id", "artist_ids")
    __slots__ = (*FIELDS, "info")  # XXX

    def __init__(self, track_id=None, *, info=None):
        super().__init__(id=track_id, info=info)

        self.album_id = self.info["album"]["id"]

        self.artist_ids = tuple(artist["id"] for artist in self.info["artists"])

        self._audio_features = None

    @classmethod
    @no_timeout
    def full_response(cls, track_id):
        return cls._sp.track(track_id if not isinstance(track_id, cls) else track_id.id)

    @property
    def audio_features(self):
        if self._audio_features is None:
            self._audio_features = AudioFeatures(self.id)
        return self._audio_features

    def __getitem__(self, key):
        if key in self.info:
            return self.info[key]
        return self.audio_features[key]


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
