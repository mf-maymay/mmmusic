# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cache import Cache
from utils import no_timeout, take_x_at_a_time


TRACK_FIELDS = ("id", "name", "album_id", "artist_ids")


def _cache_key(cls, id=None, *, info=None):
    if isinstance(id, cls):
        return id
    if info is None:
        return id
    return info["id"]


class Track(object):
    __slots__ = (*TRACK_FIELDS, "info")

    _sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials()
    )

    _use_name_for_repr = False  # Use to replace default repr with name.

    def __init__(self, track_id=None, *, info=None):
        self.info = info if info else self.full_response(track_id)

        self.id = self.info["id"]

        self.name = self.info["name"]

        self.album_id = self.info["album"]["id"]

        self.artist_ids = tuple(
            artist["id"] for artist in self.info["artists"]
        )

    @Cache(key_func=_cache_key)
    def __new__(cls, track_id=None, *, info=None):  # TODO: kwargs
        if track_id is None and info is None:
            raise ValueError("Must supply either track_id or info")
        return super().__new__(cls)

    @classmethod
    @no_timeout
    def full_response(cls, track_id):
        return cls._sp.track(
            track_id if not isinstance(track_id, cls) else track_id.id
        )

    @no_timeout
    @Cache()
    def audio_features(self):
        return self._sp.audio_features(self.id)[0]

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name < str(other)

    def __repr__(self):
        return (
            self.name if self._use_name_for_repr
            else "Track({})".format(
                ", ".join(
                    "{}={}".format(field, repr(getattr(self, field)))
                    for field in TRACK_FIELDS
                )
            )
        )

    def __str__(self):
        return self.name


def get_audio_features(tracks):
    out = []
    for subset in take_x_at_a_time(tracks, 100):
        out += no_timeout(Track._sp.audio_features)(
            tracks=[track if not isinstance(track, Track) else track.id
                    for track in subset]
        )
    return out


def get_tracks_from_albums(albums):
    return tuple(track for album in albums for track in album.tracks())
