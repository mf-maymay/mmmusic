# -*- coding: utf-8 -*-
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from artist import Artist
from cache import Cache
from user import User
from utils import no_timeout

valid_rating = re.compile("[0-5]\\.[0-9]")

search_str = "http://www.sputnikmusic.com/search_results.php?search_text="


@Cache()
@no_timeout
def sputnik_rating(artist, album):
    search = search_str + artist

    req = requests.get(search)

    soup = BeautifulSoup(req.content, "html.parser")

    album_elem = soup.find("a", text=album)

    if album_elem is None:
        return None  # XXX

    parents = album_elem.parents

    _ = next(parents)
    _ = next(parents)
    td = next(parents)

    rating_elem = td.find("b", text=valid_rating)

    if rating_elem is None:
        return None

    try:
        return float(rating_elem.text)
    except ValueError:
        return None


def get_user_album_ratings(user):
    for album in user.albums():  # TODO: make name URL friendly
        _ = sputnik_rating(Artist(album.artist_ids[0]).name,
                           album.name)

    ratings = sorted(((artist, album, rating)
                      for (artist, album), rating in sputnik_rating.items()
                      if rating is not None),
                     key=lambda x: (x[2], x[0], x[1]))

    return pd.DataFrame(
        ratings,
        columns=["Artist", "Album", "Rating"]
    )


if __name__ == "__main__":
    user = User(input("username: "))

    ratings = get_user_album_ratings(user)
