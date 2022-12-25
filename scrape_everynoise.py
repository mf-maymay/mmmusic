import json

from bs4 import BeautifulSoup
import cssutils
import requests

response = requests.get("https://everynoise.com/")
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

genre_positions = {
    element.text[:-2]: {  # genre name
        "top": int(style["top"].replace("px", "")),
        "left": int(style["left"].replace("px", "")),
    }
    for element in soup.find_all("div", class_="genre scanme")
    if (style := cssutils.parseStyle(element.attrs["style"]))
    and "top" in style
    and "left" in style
}

with open("genre_positions.json", "w") as f:
    json.dump(genre_positions, f)
