from functools import cache, cached_property

from pydantic import BaseModel, computed_field

from mmmusic.external import spotify

TrackID = str

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


class AudioFeatures(BaseModel):
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

    def __getitem__(self, key):
        return getattr(self, key)


class Track(BaseModel):
    name: str
    id: str
    album_id: str
    artist_ids: tuple[str, ...]
    popularity: int

    @computed_field
    @cached_property
    def audio_features(self) -> AudioFeatures | None:
        return get_track_audio_features(self)

    def __getitem__(self, key):
        return self.audio_features[key]

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        return self.name


@cache
def get_track(track_id: TrackID | Track) -> Track:
    if isinstance(track_id, Track):
        return track_id

    track_json = spotify.get_track(track_id)

    return Track(
        name=track_json["name"],
        id=track_json["id"],
        album_id=track_json["album"]["id"],
        artist_ids=tuple(artist["id"] for artist in track_json["artists"]),
        popularity=track_json["popularity"],
    )


@cache
def get_track_audio_features(
    track: TrackID | Track | AudioFeatures,
) -> AudioFeatures | None:
    if isinstance(track, AudioFeatures):
        return track

    if isinstance(track, Track):
        track = track.id

    audio_features_json = spotify.get_track_audio_features(track)

    if audio_features_json is None:
        return None

    return AudioFeatures.parse_obj(audio_features_json)


if __name__ == "__main__":
    track_ids = [
        "0vFabeTqtOtj918sjc5vYo",
        "3HWxpLKnTlz6jE3Vi5dTF2",
        "6PSma9xvYhGabJNrbUAE4e",
        "3qSJD2hjnZ7YDOQx9ieQ0m",
        "09uV1Sli9wapcKQmmyaG4E",
        "5vaCmKjItq2Da5BKNFHlEb",
    ]

    tracks = [get_track(track_id) for track_id in track_ids]

    track = tracks[0]

    features = track.audio_features
