# -*- coding: utf-8 -*-
from multiprocessing.connection import Listener
import traceback

import matplotlib

from artist_finder import grow_and_plot
from music_tools.artist import Artist


def return_artists(conn):
    try:
        while True:
            artist_ids = conn.recv()
            print("received: {}".format(", ".join(artist_ids)))

            artists = [Artist(artist_id) for artist_id in artist_ids]

            # TODO: check if output already exists

            grow_and_plot(*artists)  # TODO: specify save location

            print("connected: {}".format(", ".join(artist_ids)))

            # conn.send()  # XXX: send response?

    except EOFError:
        print("Connection closed")


def server(address):
    serv = Listener(address)
    while True:
        try:
            client = serv.accept()
            return_artists(client)
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    matplotlib.use("Agg")

    Artist.load_from_json()

    server(("localhost", 25000))
