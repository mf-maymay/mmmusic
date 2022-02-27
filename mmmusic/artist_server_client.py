# -*- coding: utf-8 -*-
import requests


def get_artist_json(artist_id):
    response = requests.get(f"http://localhost:8000/artists/{artist_id}")
    response.raise_for_status()
    return response.json()


def get_related_artists_json(artist_id):
    response = requests.get(
        f"http://localhost:8000/artists/{artist_id}/related-artists"
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    from music_tools.artist import Artist, RelatedArtists

    Artist.get_json = get_artist_json
    RelatedArtists.get_json = get_related_artists_json

    artist_id = "0oSGxfWSnnOXhD2fKuz2Gy"

    artist = Artist(artist_id)
    related = artist.related()
