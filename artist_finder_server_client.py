# -*- coding: utf-8 -*-
from multiprocessing.connection import Client

from music_tools.artist import search_for_artist

artist_ids = [search_for_artist("alice coltrane").id, search_for_artist("sun ra").id]


with Client(("localhost", 25000)) as c:
    c.send(artist_ids)

    response = c.recv()

    print(response)
