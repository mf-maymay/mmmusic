# -*- coding: utf-8 -*-
from collections import ChainMap

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


AudioFeatures.fetch_from_shelve()


class Track(SpotifyObjectBase):
    FIELDS = ("id", "name", "album_id", "artist_ids", "_audio_features")
    __slots__ = (*FIELDS, "info")  # XXX

    def __init__(self, track_id=None, *, info=None):
        super().__init__(id=track_id, info=info)

        self.album_id = self.info["album"]["id"]

        self.artist_ids = tuple(artist["id"] for artist in self.info["artists"])

        self._audio_features = None

        self.info = ChainMap(self.info, self.audio_features.info)

    @classmethod
    @no_timeout
    def full_response(cls, track_id):
        return cls._sp.track(track_id if not isinstance(track_id, cls) else track_id.id)

    @property
    def audio_features(self):
        if self._audio_features is None:
            self._audio_features = AudioFeatures(self.id)
        return self._audio_features


# Track.fetch_from_shelve()


def get_audio_features(tracks):
    return [AudioFeatures(track) for track in tracks]


def get_tracks_from_albums(albums):
    return tuple(track for album in albums for track in album.tracks())


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
