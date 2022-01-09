# -*- coding: utf-8 -*-
from multiprocessing.connection import Listener
from pathlib import Path
import traceback

import matplotlib

from artist_finder import grow_and_plot
from music_tools.artist import Artist


IMAGES_DIR = Path("output")

workload = set()


def return_artists(conn):
    try:
        while True:
            artist_ids = conn.recv()

            print("received: ", ", ".join(artist_ids))

            artists = tuple(sorted(artist_ids))

            file_path = (IMAGES_DIR / "-".join(artists)).with_suffix(".png")

            if file_path.is_file():
                print("network exists already: ", ", ".join(artist_ids))
                conn.send(file_path)  # XXX
                continue

            conn.send(None)  # XXX

            if artists not in workload:
                workload.add(artists)

                grow_and_plot(*artists, save=file_path)

                workload.remove(artists)

                print("connected: ", ", ".join(artist_ids))

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
