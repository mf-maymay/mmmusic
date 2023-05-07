import json

from bs4 import BeautifulSoup
import cssutils
import requests


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
