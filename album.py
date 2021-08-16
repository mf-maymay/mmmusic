# -*- coding: utf-8 -*-
from base_class import SpotifyObjectBase
from track import Track
from utils import no_timeout


class Album(SpotifyObjectBase):
    FIELDS = ("id", "name", "artist_ids")
    __slots__ = (*FIELDS, "info")  # XXX

    def __init__(self, album_id=None, *, info=None):
        super().__init__(id=album_id, info=info)

        self.artist_ids = tuple(artist["id"] for artist in self.info["artists"])

    @classmethod
    @no_timeout
    def full_response(cls, album_id):
        return cls._sp.album(album_id if not isinstance(album_id, cls) else album_id.id)

    def tracks(self):
        return [
            Track(info={**item, "album": self.info})
            for item in self.info["tracks"]["items"]
        ]


Album.fetch_from_shelve()

if __name__ == "__main__":
    album = Album("2w1YJXWMIco6EBf0CovvVN")

    tracks = album.tracks()
