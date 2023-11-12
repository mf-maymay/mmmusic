import re
from typing import TypedDict

from bs4 import BeautifulSoup
import requests

valid_rating = re.compile("[0-5](\\.[0-9])?")
valid_vote = re.compile("([0-9]|,)+ Votes")


class ArtistNotFoundError(Exception):
    pass


class SputnikAlbum(TypedDict):
    name: str
    artist: str
    rating: float
    votes: int


def get_artist_albums(artist: str) -> list[SputnikAlbum]:
    search_url = f"http://www.sputnikmusic.com/search_results.php?search_text={artist}"

    response = requests.get(search_url)

    soup = BeautifulSoup(response.content, "html.parser")

    album_name_elements = [
        elem for elem in soup.find_all("a", href=re.compile("/album/.*")) if elem.text
    ]

    return [
        {
            "name": element.text,
            "artist": artist,
            "rating": float(rating_element.text)
            if (
                rating_element := element.parent.parent.parent.find("table").find(
                    "b", text=valid_rating
                )
            )
            is not None
            else None,
            "votes": int(votes_element.text.partition(" Votes")[0].replace(",", ""))
            if (
                votes_element := element.parent.parent.parent.find("table").find(
                    "font", text=valid_vote
                )
            )
            else None,
        }
        for element in album_name_elements
    ]


if __name__ == "__main__":
    albums = get_artist_albums("Ved Buens Ende")
