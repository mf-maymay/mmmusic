from collections import defaultdict

import pandas as pd

from lib.models import sputnik
from lib.user import User


def get_user_album_ratings(user: User) -> pd.DataFrame:
    artist_album_ratings = {  # Artist -> list[SputnikAlbum]
        artist: sputnik.get_artist_albums(artist)
        for artist in user.get_artists_of_saved_albums()
    }

    artist_saved_albums = defaultdict(set)  # artist_id (str) -> set[Album]
    for album in user.get_saved_albums():
        for artist_id in album.artist_ids:
            artist_saved_albums[artist_id].add(album)

    saved_album_ratings = [
        album
        for artist, albums in artist_album_ratings.items()
        for album in albums
        if artist.id in artist_saved_albums
        and any(
            album["name"] == saved_album.name
            for saved_album in artist_saved_albums[artist.id]
        )
    ]  # NOTE: artist is assumed to be an Artist, here

    return pd.DataFrame(saved_album_ratings)


if __name__ == "__main__":
    user = User()

    ratings = get_user_album_ratings(user)

    print(ratings)
