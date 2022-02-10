# -*- coding: utf-8 -*-
from multiprocessing.connection import Client

from music_tools.artist import Artist


def get_json_from_server(artist_id):
    with Client(("localhost", 25000)) as c:
        c.send(artist_id)
        return c.recv()


Artist.get_json = get_json_from_server


if __name__ == "__main__":
    artist = Artist("0oSGxfWSnnOXhD2fKuz2Gy")
