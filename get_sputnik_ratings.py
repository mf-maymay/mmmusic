import re

from bs4 import BeautifulSoup
import pandas as pd
import requests

from lib.models.artist import get_artist
from lib.user import User
from lib.utils import no_timeout

valid_rating = re.compile("[0-5]\\.[0-9]")
valid_vote = re.compile("([0-9]|,)+ Votes")

SEARCH_TEMPLATE = "http://www.sputnikmusic.com/search_results.php?search_text={}"


@no_timeout
def sputnik_rating(artist, album):
    search = SEARCH_TEMPLATE.format(artist)

    req = requests.get(search)

    soup = BeautifulSoup(req.content, "html.parser")

    album_elem = soup.find("a", text=album)

    if album_elem is None:
        return None, None  # XXX

    parents = album_elem.parents

    _ = next(parents)
    _ = next(parents)
    td = next(parents)

    rating_elem = td.find("b", text=valid_rating)

    votes_elem = td.find("font", text=valid_vote)

    if votes_elem is None:
        votes = 0
    else:
        votes = int(votes_elem.text.split()[0].replace(",", ""))

    if rating_elem is None:
        return None, None

    try:
        return float(rating_elem.text), votes
    except ValueError:
        return None, None


def _artist_album_pair(album):
    return get_artist(album.artist_ids[0]).name, album.name


def get_user_album_ratings(user):
    ratings_dict = {
        _artist_album_pair(album): sputnik_rating(*_artist_album_pair(album))
        for album in user.albums()
    }

    ratings = [
        (artist, album, rating, votes)
        for (artist, album), (rating, votes) in ratings_dict.items()
        if rating is not None
    ]

    return pd.DataFrame(ratings, columns=["Artist", "Album", "Rating", "Votes"])


if __name__ == "__main__":
    user = User()

    ratings = get_user_album_ratings(user)
