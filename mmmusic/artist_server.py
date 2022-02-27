# -*- coding: utf-8 -*-
from fastapi import FastAPI

from music_tools.artist import Artist, RelatedArtists


app = FastAPI()


@app.get("/artists/{artist_id}")
def artist(artist_id):
    return Artist.get_json(artist_id)


@app.get("/artists/{artist_id}/related-artists")
def related_artists(artist_id):
    return RelatedArtists.get_json(artist_id)
