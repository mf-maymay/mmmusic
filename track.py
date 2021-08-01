# -*- coding: utf-8 -*-
from base_class import SpotifyObjectBase
from cache import Cache
from utils import no_timeout, take_x_at_a_time


class Track(SpotifyObjectBase):
    FIELDS = ("id", "name", "album_id", "artist_ids")
    __slots__ = (*FIELDS, "info")  # XXX

    def __init__(self, track_id=None, *, info=None):
        super().__init__(id=track_id, info=info)

        self.album_id = self.info["album"]["id"]

        self.artist_ids = tuple(artist["id"] for artist in self.info["artists"])

    @classmethod
    @no_timeout
    def full_response(cls, track_id):
        return cls._sp.track(track_id if not isinstance(track_id, cls) else track_id.id)

    @no_timeout
    @Cache()
    def audio_features(self):
        return self._sp.audio_features(self.id)[0]


def get_audio_features(tracks):
    out = []
    for subset in take_x_at_a_time(tracks, 100):
        out += no_timeout(Track._sp.audio_features)(
            tracks=[
                track if not isinstance(track, Track) else track.id for track in subset
            ]
        )
    return out


def get_tracks_from_albums(albums):
    return tuple(track for album in albums for track in album.tracks())
