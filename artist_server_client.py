# -*- coding: utf-8 -*-
from multiprocessing.connection import Client

from music_tools.artist import Artist


def get_json_from_server(artist_id):
    with Client(("localhost", 25000)) as c:
        c.send(artist_id)
        response = c.recv()

        if isinstance(response, Exception):
            raise response
        return response


if __name__ == "__main__":
    Artist.get_json = get_json_from_server

    artist = Artist("0oSGxfWSnnOXhD2fKuz2Gy")
