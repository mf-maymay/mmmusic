# -*- coding: utf-8 -*-
import json

from bs4 import BeautifulSoup
import cssutils
import requests

url = "https://everynoise.com/"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

genre_elements = soup.find_all("div", class_="genre scanme")

genre_positions = {}

for element in genre_elements:
    genre_name = element.text[:-2]
    genre_positions[genre_name] = {}

    style = cssutils.parseStyle(element.attrs["style"])
    genre_positions[genre_name]["top"] = int(style["top"].replace("px", ""))
    genre_positions[genre_name]["left"] = int(style["left"].replace("px", ""))

with open("genre_positions.json", "w") as f:
    json.dump(genre_positions, f)
