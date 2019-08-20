# -*- coding: utf-8 -*-
import spotipy
from credentials import token
from utils import get_artist

sp = spotipy.Spotify(auth=token)

saved = set()

offset = 0

while True:
    albums = sp.current_user_saved_albums(limit=50, offset=offset)

    items = albums["items"]

    for item in items:
        saved |= {get_artist(artist["id"])
                  for artist in item["album"]["artists"]}

    offset += len(items)

    if len(items) == 0:
        break
