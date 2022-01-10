# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor  # XXX: threadsafe?
from multiprocessing.connection import Listener
from pathlib import Path
import traceback

import matplotlib

from artist_finder import grow_and_plot
from music_tools.artist import Artist


IMAGES_DIR = Path("output")


def connect_artists(artists, *, save):
    grow_and_plot(*artists, save=save)
    print("connected: ", ", ".join(artists))


def handle_connection(conn, *, executor, in_progress: dict):
    try:
        while True:
            artist_ids = conn.recv()

            print("received: ", ", ".join(artist_ids))

            artists = tuple(sorted(artist_ids))

            file_path = (IMAGES_DIR / "-".join(artists)).with_suffix(".png").absolute()

            if file_path.is_file():
                print("network exists already: ", ", ".join(artists))
                conn.send(file_path)  # XXX
                continue

            if artists in in_progress:
                if in_progress[artists].done():
                    try:
                        in_progress[artists].result()  # raise exceptions ?
                    finally:
                        del in_progress[artists]  # XXX

            else:
                in_progress[artists] = executor.submit(
                    connect_artists, artists, save=file_path
                )

            conn.send(None)  # XXX

    except EOFError:
        print("Connection closed")


def server(address):
    serv = Listener(address)

    in_progress = {}  # artists -> future

    with ThreadPoolExecutor() as executor:
        while True:
            try:
                client = serv.accept()
                handle_connection(client, executor=executor, in_progress=in_progress)

            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    matplotlib.use("Agg")

    Artist.use_json()

    server(("localhost", 25000))
