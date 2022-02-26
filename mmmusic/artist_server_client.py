# -*- coding: utf-8 -*-
import requests


def get_json_from_server(artist_id):
    response = requests.get(f"http://localhost:8000/artist/{artist_id}")
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    from music_tools.artist import Artist

    Artist.get_json = get_json_from_server

    artist = Artist("0oSGxfWSnnOXhD2fKuz2Gy")
