from concurrent.futures import ThreadPoolExecutor
from datetime import date
from functools import cache

from pydantic import BaseModel, validator

from lib.external import spotify
from lib.models.track import Track, get_track

AlbumID = str


class Album(BaseModel):
    name: str
    id: str
    album_type: str
    release_date: date
    artist_ids: tuple[str, ...]

    @validator("release_date", pre=True)
    def coerce_to_full_date(cls, value):
        if not isinstance(value, str):
            return value

        fields = value.split("-")

        if (num_fields := len(fields)) in {1, 2}:
            return "-".join(fields + ["1"] * (3 - num_fields))

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
    album = get_album(album)

    return tuple(get_track(track["id"]) for track in spotify.get_album_tracks(album.id))


def get_tracks_from_albums(albums: list[Album | AlbumID]) -> tuple[Track, ...]:
    max_workers = 4  # (temp fix) Limit workers to avoid 429s.
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return sum(executor.map(get_album_tracks, albums), start=())


if __name__ == "__main__":
    album = get_album("5Tw0sanofDSd7h44GySmoa")

    tracks_from_album = get_album_tracks(album)

    assert len(tracks_from_album) > 50

    tracks_from_albums = get_tracks_from_albums([album, "3539EbNgIdEDGBKkUf4wno"])
