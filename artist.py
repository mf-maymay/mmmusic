# -*- coding: utf-8 -*-
from cache import Cache
from base_class import SpotifyObjectBase
from utils import no_timeout


class Artist(SpotifyObjectBase):
    FIELDS = ("id", "name", "genres", "popularity")
    __slots__ = (*FIELDS, "info")

    def __init__(self, artist_id=None, *, info=None):
        super().__init__(id=artist_id, info=info)

        self.genres = tuple(sorted(self.info["genres"]))

        self.popularity = self.info["popularity"]

    @classmethod
    @no_timeout
    def full_response(cls, artist_id):
        return cls._sp.artist(
            artist_id if not isinstance(artist_id, cls) else artist_id.id
        )

    @Cache
    def related(self):
        return set(
            Artist(a["id"]) for a in self._sp.artist_related_artists(self.id)["artists"]
        )


if __name__ == "__main__":
    artist = Artist("0oSGxfWSnnOXhD2fKuz2Gy")
