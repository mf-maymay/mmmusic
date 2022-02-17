# -*- coding: utf-8 -*-
from multiprocessing.connection import Client

from music_tools.artist import search_for_artist


input_0 = input("artist #1: ")
input_1 = input("artist #2: ")


artist_ids = [search_for_artist(input_0).id, search_for_artist(input_1).id]


with Client(("localhost", 25000)) as c:
    c.send(artist_ids)

    response = c.recv()

    print(response)
