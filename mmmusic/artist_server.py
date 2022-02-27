# -*- coding: utf-8 -*-
from fastapi import FastAPI

from music_tools.artist import Artist


app = FastAPI()


@app.get("/artists/{artist_id}")
def artist(artist_id):
    return Artist.get_json(artist_id)
