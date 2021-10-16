# -*- coding: utf-8 -*-
from base_class import SpotifyObjectBase
from utils import no_timeout


class AudioFeatures(SpotifyObjectBase):
    FIELDS = ("id",)
    __slots__ = (*FIELDS, "info")  # XXX

    def __init__(self, track_id=None, *, info=None):
        if info is not None and "name" not in info:
            info = {"name": info["id"], **info}  # add name

        super().__init__(id=track_id, info=info)

    @classmethod
    @no_timeout
    def full_response(cls, track_id):
        features = cls._sp.audio_features(
            track_id if not isinstance(track_id, SpotifyObjectBase) else track_id.id
        )[0]
        features["name"] = features["id"]
        return features


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
    AudioFeatures.use_json()
    Track.use_json()

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
