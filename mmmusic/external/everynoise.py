import json
import re

from bs4 import BeautifulSoup
import cssutils
import requests

_GENRE_CHARS_TO_SQUASH = re.compile("[^a-zA-Z0-9]+")


def _everynoise_name_for_genre(genre: str) -> str:
    return _GENRE_CHARS_TO_SQUASH.sub("", genre)


def get_artists_for_genre(genre: str) -> set:
    """Returns a set of artist names that belong to the genre map."""
    genre = _everynoise_name_for_genre(genre)

    url = f"https://everynoise.com/engenremap-{genre}.html"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    canvas = soup.find(class_="canvas", attrs={"role": "main"})

    if canvas is None:
        raise RuntimeError

    return {
        element.text[:-2] for element in canvas.find_all("div", class_="genre scanme")
    }


def get_genre_positions() -> dict:
    response = requests.get("https://everynoise.com/")
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    return {
        element.text[:-2]: {  # genre name
            "top": int(style["top"].replace("px", "")),
            "left": int(style["left"].replace("px", "")),
        }
        for element in soup.find_all("div", class_="genre scanme")
        if (style := cssutils.parseStyle(element.attrs["style"]))
        and "top" in style
        and "left" in style
    }


def refresh_genre_positions():
    genre_positions = get_genre_positions()

    with open("genre_positions.json", "w") as f:
        json.dump(genre_positions, f)
