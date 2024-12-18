from datetime import date
from functools import cache

from pydantic import BaseModel, validator

from mmmusic.external import spotify
from mmmusic.log_utils import get_logger
from mmmusic.models.tracks import Track, get_track

logger = get_logger()

AlbumID = str


class Album(BaseModel):
    name: str
    id: str
    album_type: str
    release_date: date
    artist_ids: tuple[str, ...]

    @validator("release_date", pre=True)
    def coerce_to_full_date(cls, value):  # noqa: N805
        if not isinstance(value, str):
            return value

        fields = value.split("-")

        if (num_fields := len(fields)) in {1, 2}:
            return "-".join(fields + ["01"] * (3 - num_fields))

        return value

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        return self.name


@cache
def get_album(album_id: AlbumID | Album) -> Album:
    if isinstance(album_id, Album):
        return album_id

    album_json = spotify.get_album(album_id)
    artist_ids = tuple(artist["id"] for artist in album_json["artists"])

    return Album.parse_obj({**album_json, "artist_ids": artist_ids})


@cache
def get_album_tracks(album: Album | AlbumID) -> tuple[Track, ...]:
    logger.debug("Getting tracks from album %r", album)

    album = get_album(album)

    return tuple(get_track(track["id"]) for track in spotify.get_album_tracks(album.id))


def get_tracks_from_albums(albums: list[Album | AlbumID]) -> tuple[Track, ...]:
    return tuple(track for album in albums for track in get_album_tracks(album))


if __name__ == "__main__":
    album = get_album("5Tw0sanofDSd7h44GySmoa")

    tracks_from_album = get_album_tracks(album)

    assert len(tracks_from_album) > 50

    tracks_from_albums = get_tracks_from_albums([album, "3539EbNgIdEDGBKkUf4wno"])
