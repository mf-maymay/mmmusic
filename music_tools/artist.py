# -*- coding: utf-8 -*-
from spotipy.exceptions import SpotifyException

from music_tools.base_class import SpotifyObjectBase
from music_tools.utils import no_timeout


class RelatedArtists(SpotifyObjectBase):
    FIELDS = ("id", "artist_ids")
    __slots__ = (*FIELDS, "info")  # XXX

    def __init__(self, artist_id=None, *, info=None):
        if info is not None and "id" not in info:
            raise ValueError("info is missing required 'id' key")

        super().__init__(id=artist_id, info=info)

        self.artist_ids = tuple(artist["id"] for artist in self.info["artists"])

    @classmethod
    @no_timeout
    def full_response(cls, artist_id):
        response = cls._sp.artist_related_artists(artist_id)
        response["name"] = response["id"] = artist_id
        return response


class Artist(SpotifyObjectBase):
    FIELDS = ("id", "name", "genres", "popularity")
    __slots__ = (*FIELDS, "info")

    def __init__(self, artist_id=None, *, info=None):
        super().__init__(id=artist_id, info=info)

        self.genres = tuple(sorted(self.info["genres"]))

        self.popularity = self.info["popularity"]

        self._related_artists = None

    @classmethod
    @no_timeout
    def full_response(cls, artist_id):
        return cls._sp.artist(
            artist_id if not isinstance(artist_id, cls) else artist_id.id
        )

    def related(self):
        if self._related_artists is None:
            self._related_artists = tuple(
                Artist(artist_id) for artist_id in RelatedArtists(self.id).artist_ids
            )
        return self._related_artists


def search_for_artist(search_text):
    try:
        return Artist(search_text)
    except SpotifyException:
        search_result = no_timeout(Artist._sp.search)(
            search_text, limit=1, type="artist"
        )
        return Artist(info=search_result["artists"]["items"][0])


if __name__ == "__main__":
    Artist.use_json()

    artist = Artist("0oSGxfWSnnOXhD2fKuz2Gy")
